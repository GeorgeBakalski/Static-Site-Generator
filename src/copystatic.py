import os, shutil

def copy_files_recursive(sourse, destination):
    os.mkdir(destination)
    for file in os.listdir(sourse):
        if os.path.isfile(os.path.join(sourse, file)):
            shutil.copy(os.path.join(sourse, file), destination)
        else:
            copy_files_recursive(os.path.join(sourse, file),os.path.join(destination, file))

