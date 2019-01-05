import os

home = os.path.expanduser("~")

def init(logger, backup_suffix_):
    global log
    log = logger
    global backup_suffix
    backup_suffix = backup_suffix_

def _correct_path(key, value):
    path = key.replace("~", home)
    source = os.getcwd()+"/"+value
    return path, source

def install(list):
    for item in list:
        path, source = _correct_path(item, list[item])
        if os.path.exists(path+backup_suffix):
            log(path+backup_suffix+" exists, script will stop to prevent file mangling")
            exit('Script Exited!')
            # option = input("[s]kip, [o]verwrite, [a]bort")
            # if option == 's':
            #     continue
            # elif option == 'a':

        if os.path.exists(path) and not os.path.islink(path):
            log(path+" - "+"Path exists!")
            log("Renaming: "+path+" to "+path+backup_suffix)
            os.rename(path, path+backup_suffix)
        try:
            log("Linking: " + source+" to " + path)
            os.symlink(source, path)
        except FileExistsError:
            log("Link already exists!")
        except FileNotFoundError:
            if not os.path.exists(path):
                pwd = path.split('/')
                pwd.pop()
                pwd = '/'.join(pwd)
                print("Creating path: "+pwd)
                os.makedirs(pwd)
                os.symlink(source, path)

def recover(list):
    for item in list:
        path, source = _correct_path(item, list[item])
        if os.path.exists(path+backup_suffix):
            if os.path.islink(path):
                log("Removing: "+path)
                os.remove(path)
                try:
                    log("Renaming: "+path+backup_suffix+" to " + path)
                    os.rename(path+backup_suffix, path)
                except FileNotFoundError:
                    log(path+backup_suffix+" not found, likely deleted")
            else:
                log("Not a link or missing, skipping!")
        else:
            log("Removing: "+path)
            os.remove(path)
