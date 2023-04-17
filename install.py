#!/bin/python3
import os
import sys
import argparse
import time
import datetime
import json

# DEFAULT CONFIG
LOG_FILE = "setup.log"
DOTFILE = "default.json"
BACKUP_SUFFIX = "__backup"
PRESET = "default"
home = os.path.expanduser("~")
# ------------------------------------------

# CLI Args
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", dest="filename", default=DOTFILE,
                    help="read from FILE", metavar="FILE")
parser.add_argument("-o", "--option", dest="option", required=False,
                    help="set OPTION without propting for one", metavar="OPTION")
args = parser.parse_args()
# ------------------------------------------


def correct_path(key, value):
    path = key.replace("~", home)
    return path, value


def source_correction(value: str, dotfiles_path: str):
    path = value
    if path.split('/')[0] == ".":
        base_array = dotfiles_path.split("/")
        base_array.pop()
        base = "/".join(base_array)
        path = value.replace(".", base)

    return path


def read_config(dotfile: str):
    with open(dotfile) as json_data:
        data = json.load(json_data)
    return data


def print_notifier():
    print("----------------------------------------------------------------")
    print(
        f"Script output will be logged in {LOG_FILE} for future reference")
    print("----------------------------------------------------------------")


class Logger():
    def __init__(self, filename=LOG_FILE):
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
    def __init__(self, backup_suffix=BACKUP_SUFFIX, logger: Logger = None):
        self.logger = logger
        self.dotfile = args.filename

        option = args.option
        if option is None:
            option = input("[i]nstall [r]ecover [e]xit:\n")

        data = read_config(self.dotfile)
        try:
            links = data['links']
            deps = data['dependencies']
        except:
            print('Did you specify an existing preset?')
            sys.exit()

        if option == "i":
            self.logger.log("# INSTALLING")
            print_notifier()
            self.install(links)
            self.logger.log(
                "----------------------------------------------------------------")
            self.logger.log("Installation complete!\n")
        if option == "r":
            self.logger.log("# REMOVING")
            print_notifier()
            self.uninstall(links)
            self.logger.log(
                "----------------------------------------------------------------")
            self.logger.log("Removal complete!\n")
        if option == "e":
            sys.exit()

    def install(self, list: []):
        # Get name to folder to look at
        dotfile = self.dotfile.split('/')[-1]
        for item in list:
            path, source = correct_path(item, list[item])
            if os.path.exists(path+BACKUP_SUFFIX):
                self.logger.log(
                    f"{path}{BACKUP_SUFFIX} exists, script will stop to prevent file mangling")
                exit('Script Exited!')

            if os.path.exists(path) and not os.path.islink(path):
                self.logger.log(f"{path} - Path exists!")
                self.logger.log(f"Renaming: {path} to {path}{BACKUP_SUFFIX}")
                os.rename(path, path+BACKUP_SUFFIX)
            try:
                source = source_correction(source, self.dotfile)
                self.logger.log(f"Linking: {dotfile} | {source} to {path}")
                os.symlink(source, path)
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
            if os.path.exists(path+BACKUP_SUFFIX):
                if os.path.islink(path):
                    self.logger.log(f"Removing: {path}")
                    os.remove(path)
                    try:
                        self.logger.log(
                            f"Renaming: {path}{BACKUP_SUFFIX} to {path}")
                        os.rename(path+BACKUP_SUFFIX, path)
                    except FileNotFoundError:
                        self.logger.log(
                            f"{path}{BACKUP_SUFFIX} not found, likely deleted")
                else:
                    self.logger.log("Not a link or missing, skipping!")
            else:
                self.logger.log(f"Removing: {path}")
                os.remove(path)


Installer(logger=Logger())
