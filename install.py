#!/bin/python3
import subprocess
import os
import argparse
import time
import datetime
import json

# DEFAULT CONFIG
logfile = "setup.log"
dotfile = "dotfiles.json"
backup_suffix = "__backup"
preset = "default"
home = os.path.expanduser("~")
#------------------------------------------

# CLI Args
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", dest="filename", default=dotfile,
                    help="read from FILE", metavar="FILE")
parser.add_argument("-o", "--option", dest="option", required=False,
                    help="set OPTION without propting for one", metavar="OPTION")
parser.add_argument("-p", "--preset", dest="preset", required=False, default=preset,
                    help="specify preset", metavar="PRESET")
args = parser.parse_args()
#------------------------------------------

def correct_path(key, value):
    path = key.replace("~", home)
    return path, value

def read_config(dotfile: str):
    with open(dotfile) as json_data:
        data = json.load(json_data)
    return data

def print_notifier():
    print("----------------------------------------------------------------")
    print(
        f"Script output will be logged in {logfile} for future reference")
    print("----------------------------------------------------------------")


class Logger():
    def __init__(self, filename=logfile):
        self.file = open(filename, 'a')
        
    def log(self, string: str):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print(string)
        string = "["+st+"] "+string+"\n"
        self.file.write(string)

    def destroy(self):
        self.file.close()


class Installer():
    def __init__(self, backup_suffix=backup_suffix, logger: Logger=None):
        self.logger = logger
        self.dotfile = args.filename
        preset = args.preset
        
        option = args.option
        if option is None:
            option = input("[i]nstall [r]ecover [e]xit:\n")

        data = read_config(self.dotfile)
        try:
            links = data[preset]['links']
            deps = data[preset]['dependencies']
        except:
            print('Did you specify an existing preset?')
            exit()

        if option == "i":
            self.logger.log("# INSTALLING")
            print_notifier()
            self.install(links)
            self.logger.log("----------------------------------------------------------------")  
            self.logger.log("Installation complete!\n")
        if option == "r":
            self.logger.log("# REMOVING")
            print_notifier()
            self.uninstall(links)
            self.logger.log("----------------------------------------------------------------")  
            self.logger.log("Removal complete!\n")
        if option == "e":
            exit()
    
    def install(self, list: []):
        dotfile = '/'.join(self.dotfile.split('/')[0:-1])
        for item in list:
            path, source = correct_path(item, list[item])
            if os.path.exists(path+backup_suffix):
                self.logger.log(f"{path}{backup_suffix} exists, script will stop to prevent file mangling")
                exit('Script Exited!')

            if os.path.exists(path) and not os.path.islink(path):
                self.logger.log(f"{path} - Path exists!")
                self.logger.log(f"Renaming: {path} to {path}{backup_suffix}")
                os.rename(path, path+backup_suffix)
            try:
                self.logger.log(f"Linking: {dotfile}/{source} to {path}")
                os.symlink(f"{dotfile}/{source}", path)
            except FileExistsError:
                self.logger.log("Link already exists!")
            except FileNotFoundError:
                if not os.path.exists(path):
                    pwd = path.split('/')
                    pwd.pop()
                    pwd = '/'.join(pwd)
                    print(f"Creating path: {pwd}")
                    os.makedirs(pwd)
                    os.symlink(source, path)

    def uninstall(self, list: []):
        for item in list:
            path, source = correct_path(item, list[item])
            if os.path.exists(path+backup_suffix):
                if os.path.islink(path):
                    self.logger.log(f"Removing: {path}")
                    os.remove(path)
                    try:
                        self.logger.log(f"Renaming: {path}{backup_suffix} to {path}")
                        os.rename(path+backup_suffix, path)
                    except FileNotFoundError:
                        self.logger.log(f"{path}{backup_suffix} not found, likely deleted")
                else:
                    self.logger.log("Not a link or missing, skipping!")
            else:
                self.logger.log(f"Removing: {path}")
                os.remove(path)

Installer(logger=Logger())
