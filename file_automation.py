#packages
import os
import filetype
#filetype is a python package which will identify the type of the file.

Files = []
#Path of the directory.
directory = 'C:\\Users\\RAVIRAJA\\Downloads\\Testing'
#Here you can provide the directory where you to perform the automatic allocation of folders.

#Function to create Folders based on the file type and will return the creted directory.
def validatefolder(directory2):
    #kind will provide the media type of the file, in some cases like pdf it will identify as appliation
    #so if  you  want to seperte them also then ignore the kind and the followed if and use only else.
    #which will crete folders based on each file type you have.
    kind = filetype.guess(directory2)
    if(kind != None):
        string = list(map(str, kind.mime.split('/')))
        data_type = string[0]
        data = data_type +'_files'
        data = data.upper()
    else:
        #The following else code will take the type of the file from the extinsion of the file and will create folders.
        extension = list(os.path.splitext(directory2))
        data = extension[1][1:]+'_Files'
        data = data.upper()
    new_Dire = directory + '\\' + data + '\\'
    if(os.path.isdir(new_Dire) == False):
        os.mkdir(new_Dire)
    return (new_Dire)

#This below Function will move the files.
def changing_files(lis):
    for filename in lis:
        old_dire = directory+'\\'+filename
        new_Dire = validatefolder(old_dire)
        destination_dire = new_Dire + '\\' + filename
        os.rename(old_dire, destination_dire)
        
#command to find all the files and folders present in the function.
allfiles =  os.listdir(directory)

#code to remove the folders and provide only the files.
for i in allfiles:
    x = directory + '\\' + i
    if os.path.isdir(x) == False:
        Files.append(i)

#Calling the function.
changing_files(Files)

