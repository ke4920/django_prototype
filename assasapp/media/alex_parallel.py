import os
#os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3"
import torch
import torchvision
import torch.distributed as dist

from torch.nn.parallel import DistributedDataParallel as DDP
from model import AlexNet
from helper_dataset import get_dataloaders_cifar10_ddp
from helper_train import train_model_ddp
from helper_evaluation import set_all_seeds, get_right_ddp, compute_accuracy_ddp

def main():
    world_size = int(os.getenv("SLURM_NPROCS")) # Get overall number of processes.
    rank = int(os.getenv("SLURM_PROCID"))       # Get individual process ID.
    cuda_vis_dev = os.getenv("CUDA_VISIBLE_DEVICES")
    slurm_job_gpus = os.getenv("SLURM_JOB_GPUS")
    slurm_localid = int(os.getenv("SLURM_LOCALID"))
    #device = f"cuda:{slurm_localid}"
    #torch.cuda.set_device(device)
    gpus_per_node = torch.cuda.device_count()
    print(f"Rank {rank}/{world_size}: CUDA_VISIBLE_DEVICES is {cuda_vis_dev}.")
    print(f"Rank {rank}/{world_size}: SLURM_JOB_GPUS is {slurm_job_gpus}.")
    print(f"Rank {rank}/{world_size}: SLURM_LOCALID is {slurm_localid}.")
    print(f"Rank {rank}/{world_size}: CUDA available {torch.cuda.is_available()}")
    print(f"Rank {rank}/{world_size}: CUDA device count is {gpus_per_node}")
    #print(f"Rank {rank}/{world_size}: C CUDA device count is {torch._C._cuda_getDeviceCount()}")
    #print(f"Rank {rank}/{world_size}: Current device is {torch.cuda.current_device()}")
    print(f"Rank {rank}/{world_size}: CUDA initialized {torch.cuda.is_initialized()}...")
    
    gpu = rank % gpus_per_node
    
    if gpu == slurm_localid:
        print(f"SLURM LOCALID {slurm_localid} and GPU {gpu} match.")
    else:
        print(f"SLURM LOCALID {slurm_localid} and GPU {gpu} do NOT match.")
    device = f"cuda:{slurm_localid}"
    torch.cuda.set_device(device)
    print(f"Rank {rank}/{world_size}: Current device is {torch.cuda.current_device()}")
    
    if dist.is_available(): 
        print(f"Rank {rank}/{world_size}: Distributed package available...[OK]") # Check if distributed package available.
    if dist.is_nccl_available(): 
        print(f"Rank {rank}/{world_size}: NCCL backend available...[OK]")   # Check if NCCL backend available.
    
    # Initialize DDP.
    dist.init_process_group(backend="nccl", rank=rank, world_size=world_size, init_method="env://")
    if dist.is_initialized(): 
        print(f"Rank {rank}/{world_size}: Process group initialized successfully...[OK]") # Check initialization.
    
    # Check used backend.
    print(dist.get_backend(), "backend used...[OK]")
    print(f"Torch rank is {torch.distributed.get_rank()}, torch world size is {torch.distributed.get_world_size()}.")
    
    seed = 99  # Set random seed.
    b    = 256 # Set batch size.
    e    = 100 # Set number of epochs to be trained.
    
    set_all_seeds(seed)    
    
    train_transforms = torchvision.transforms.Compose([
    torchvision.transforms.Resize((70, 70)),
    torchvision.transforms.RandomCrop((64, 64)),
    torchvision.transforms.ToTensor(),
    torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    
    test_transforms = torchvision.transforms.Compose([
    torchvision.transforms.Resize((70, 70)),        
    torchvision.transforms.CenterCrop((64, 64)),            
    torchvision.transforms.ToTensor(),                
    torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    
    # Get distributed dataloaders for training and validation data on all ranks.
    train_loader, valid_loader = get_dataloaders_cifar10_ddp(
        batch_size=b, 
        root='/scratch/hpc-prf-nhrgs/mweiel/data', 
        train_transforms=train_transforms,
        test_transforms=test_transforms)
    
    # Get dataloader for test data. 
    # Final testing is only done on root.
    if dist.get_rank() == 0:
        test_dataset = torchvision.datasets.CIFAR10(root="/scratch/hpc-prf-nhrgs/mweiel/data",
                                                    train=False,
                                                    transform=test_transforms
                                                   )
        test_loader = torch.utils.data.DataLoader(dataset=test_dataset,
                                                  batch_size=b,
                                                  shuffle=False
                                                 )
    
    model = AlexNet(num_classes=10)#.cuda() # Create model and move it to GPU with id rank.
    model.to(device)
    ddp_model = DDP(model, device_ids=[slurm_localid], output_device=slurm_localid) # Wrap model with DDP.
    
    optimizer = torch.optim.SGD(ddp_model.parameters(), momentum=0.9, lr=0.1) 
    
    # Train model.
    train_model_ddp(
        model=ddp_model,
        num_epochs=e,
        train_loader=train_loader,
        valid_loader=valid_loader,
        optimizer=optimizer)
    
    # Test final model on root.
    if dist.get_rank() == 0:
        test_acc = compute_accuracy_ddp(ddp_model, test_loader) # Compute accuracy on test data.
        # Model or ddp model here?
        print(f'Test accuracy {test_acc :.2f}%')
        
    dist.destroy_process_group()

# MAIN STARTS HERE.    
if __name__ == '__main__':
    main()
