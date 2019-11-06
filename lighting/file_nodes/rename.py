import pymel.core as pm
import random 
import datetime


fln = pm.ls(type='file')

def rename_texture_files(list_of_file_nodes):
    current_time = datetime.datetime.now()
    random.seed(current_time.second)
    
    
    def get_random_id():
        current_time = datetime.datetime.now()
        random.seed(current_time.second)
        return random.randint(10000, 99999)
        
        
    for each in fln:
        my_id = get_random_id()
        filename = each.fileTextureName.get()
        
        if filename == '':
            pass
        else:
            fln[0].listAttr()
            filename = filename.replace('//', '/')
            filename = filename.split('/')[-1]
            filename = filename.split('.')[0]
            formated_name = ''
            for i, element in enumerate(filename.split('_')):
                if i == 0:
                    formated_name += element.lower()
                else:
                    formated_name += element.title() 
            each.rename('{0}_{1}_FLE'.format(formated_name, my_id))
            
rename_texture_files(fln)