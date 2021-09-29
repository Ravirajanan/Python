import os
import subprocess
from numpy.lib.index_tricks import fill_diagonal
import pandas as pd
import magic

images = []
global file_paths_before_organizing


def get_path():
    print(r"""Enter the specific path which you want to organize Example - C:\Users\RAVIRAJA\OneDrive\Documents""")
    path = input()
    print(path)
    path = r"C:\Users\RAVIRAJA\Downloads\testing"
    return path


def file_identification(directory, files, df, df2):
    file_paths_before_organizing = pd.DataFrame(columns=['File Name','Old Path','New Path'])
    for i in  files:
        file = directory +'\\' + i
        filename, filepath = os.path.splitext(file)
        x= df[df['extensions'] == filepath]
        if x.size>0:
            filetype = x['name'].values[0]
            if (x['type'].values[0]) == 'programming' or (x['type'].values[0] == 'markup'):
                file_category = x['type'].values[0]
                old_directory, new_directory = moving_files(True,filepath,filetype,directory,i,file_category)
            else:
                filepath = filepath.upper()
                x = df2[df2['extensions'] == filepath]['name'].values
                filetype = (x[0])
                old_directory, new_directory = moving_files(False,filepath,filetype,directory,i)
        else:
            filepath = filepath.upper()
            x = df2[df2['extensions'] == filepath]['name'].values
            filetype = (x[0])
            old_directory, new_directory = moving_files(False,filepath,filetype,directory,i)
        file_paths_before_organizing = file_paths_before_organizing.append({'File Name':i,'Old Path':old_directory,'New Path':new_directory},ignore_index = True)
    file_paths_before_organizing.to_csv(directory+'\Change_details.csv')


def validateANDcreate_folder(new_path):
    if(os.path.isdir(new_path) == False):
        os.mkdir(new_path)

def moving_to_newpath(old_directory,new_directory):
    os.rename(old_directory,new_directory)

def moving_files(flag,filepath,filetype,directory,filename,file_category = None ):
    if flag:
        filepath = filepath.upper()+' FILES'
        filetype = filetype.upper()+' FILES'
        file_category = file_category.upper()
        old_directory = directory + '\\' + filename
        new_directory = directory+'\\'+file_category+'\\'+filetype+'\\'+filename
        new_path = directory+'\\'+file_category
        validateANDcreate_folder(new_path)
        new_path = directory+'\\'+file_category+'\\'+filetype+'\\'
        validateANDcreate_folder(new_path)
        moving_to_newpath(old_directory,new_directory)
        
    else:
        filepath = filepath.upper()
        filepath = filepath[1:]+' FILES'
        filetype = filetype.upper()+' FILES'
        old_directory = directory + '\\' + filename
        new_directory = directory+'\\'+filetype+'\\'+filepath+'\\'+filename
        new_path = directory+'\\'+filetype
        validateANDcreate_folder(new_path)
        new_path = directory+'\\'+filetype+'\\'+filepath+'\\'
        validateANDcreate_folder(new_path)
        moving_to_newpath(old_directory,new_directory)
    
    return old_directory,new_directory
        
        

def get_files(directory):
    Files = []
    allfiles = os.listdir(directory)
    for i in allfiles:
        x = directory + '\\' + i
        if os.path.isdir(x) == False:
            Files.append(i)
    return Files
            
            
def fun(x):
    x = set(x)
    x = list(x)
    return(x)

def reading_extension_data():
    programming_extensions = pd.read_json('programming_extensions.json')
    programming_extensions.dropna(subset=['extensions'], inplace=True)
    programming_extensions['extensions']  = programming_extensions['extensions'].apply(lambda x: fun(x))
    programming_extensions = programming_extensions.explode('extensions',ignore_index = True)
    programming_extensions.name = programming_extensions.name.astype('str')
    extension_by_type = pd.read_json('extensions_by_type.json')
    extension_by_type.dropna(subset=['extensions'], inplace=True)
    extension_by_type['extensions']  = extension_by_type['extensions'].apply(lambda x: fun(x))
    extension_by_type = extension_by_type.explode('extensions',ignore_index = True)
    return programming_extensions,extension_by_type



def main ():
    print('File organizing or undo')
    if input() == 'undo':
        df = pd.read_csv(r"C:\Users\RAVIRAJA\Downloads\testing\Change_details.csv")
        old_directory = list(df['Old Path'])
        new_directory = list(df['New Path'])
        
        for i in range(0,len(old_directory)):
            print(i)
            moving_to_newpath(new_directory[i],old_directory[i])
        print('completed')
    else:
        directory = get_path()
        #reading extension data
        programming_extensions,extension_by_type = reading_extension_data()
        #get all the files in path
        files = get_files(directory)
        #files = get_files(directory,programming_extensions,extension_by_type,file_paths_before_organizing)
        file_identification(directory,files,programming_extensions,extension_by_type)
    
if __name__ == "__main__":
    main()