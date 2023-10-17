#import smbclient
import time
import shutil
import h5py
import numpy as np


class DatabaseManager:

    def __init__(self) -> None:
        pass

    def upload():
        return True
    
    def view():
        return True

class AssasFile:
    
    def __init__(self):
        
        name = 'test.h5'
        variables = ["var1", "var2"] 
        channels = 4
        meshes = 16
        time = 1000
        
        with h5py.File(name, 'w') as h5f:

            h5f.create_group('metadata')
            h5f['metadata'].attrs['upload_time'] = 0

            h5f.create_group('input')
            h5f['input'].attrs['debris'] = 0

            data_group = h5f.create_group('data')

            for variable in variables:
                variable_group = data_group.create_group(variable)
                array = np.random.rand(channels, meshes, time, 1).reshape(channels, meshes, time)
                variable_group.create_dataset(variable, data = array)

        h5f.close()

class Hdf5Handler:

    def __init__(self) -> None:
        pass

    def create_hdf5(self):

        return 

class DatabaseHandler:

    def __init__(self) -> None:
        pass

class StorageHandler:

    def __init__(self):
        
        self.tmp_dir = "./tmp"
        self.mount_point = "/mnt/ASSAS"
        self.archvie_dir = "archive"

    def store_datset(self, file):

        upload_time = time.time()
        
        source = file
        dest = "/mnt/lsdf/" + str(upload_time)
        print(dest)
        shutil.copy("/home/jonas/django_prototype/assas_data/test.h5", dest)

    def mount_lsdf():
        return True
    
    def is_mounted():
        return True


import shutil
shutil.copy2("/home/jonas/django_prototype/assas_data/test.h5", "/mnt/ASSAS/test/test.h5")