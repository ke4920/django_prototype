import os
import builtins
import argparse
import torch
import torch.distributed as dist
import socket

WORLD_SIZE = int(os.environ["SLURM_NTASKS"])
WORLD_RANK = int(os.environ['SLURM_PROCID'])
LOCAL_RANK = int(os.environ['SLURM_LOCALID'])
NODELIST = os.environ['SLURM_NODELIST']
NGPUS_PER_NODE = torch.cuda.device_count()
HOSTNAME = socket.gethostname()


def run(backend):
    tensor = torch.zeros(1)
    if WORLD_RANK == 0:
        print("torch version:", torch.__version__)
        print("torch distributed available?", torch.distributed.is_available())
        print("NCCL available?", torch.distributed.is_nccl_available())
        print("NCCL version: ", torch.cuda.nccl.version())
        print("WORLD_SIZE:", WORLD_SIZE)
        print("NODELIST:", NODELIST)
        print("NGPUS_PER_NODE:", NGPUS_PER_NODE)
        print("")
        print("")

    torch.distributed.barrier()
    # Need to put tensor on a GPU device for nccl backend
    if backend == 'nccl':
        device = torch.device("cuda:{}".format(LOCAL_RANK))
        tensor = tensor.to(device)

    print("Rank", WORLD_RANK, " runs on node" ,HOSTNAME, " and uses GPU", LOCAL_RANK)

    if WORLD_RANK == 0:
        for rank_recv in range(1, WORLD_SIZE):
            dist.send(tensor=tensor, dst=rank_recv)
            print('Rank {} sent data to rank {}'.format(0, rank_recv))
    else:
        dist.recv(tensor=tensor, src=0)
        print('Rank {} has received data from rank {}'.format(WORLD_RANK, 0))

    
def init_processes(backend):
    dist.init_process_group(backend, rank=WORLD_RANK, world_size=WORLD_SIZE)
    run(backend)


if __name__ == "__main__":
    

    init_processes("nccl")


