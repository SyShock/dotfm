'''
Author: SyShock
Description: this script installs the dotfiles on your system, it has two options: install or recover
Additional: this script does not install the missing dependencies that the dotfiles' programs will use, yet...
'''
# CONFIG
logfile = "setup.log"
dotfile = "dotfiles.json"
backup_suffix = "__backup"
preset="default"
#------------------------------------------

import json
import logger
import dep_installer as dep
import link_installer as link
import argparse

def print_notifier():
    print("----------------------------------------------------------------")
    print("Script output will be logged in "+logfile+" for future reference")
    print("----------------------------------------------------------------")

def read_config():
    with open(dotfile) as json_data:
        data = json.load(json_data)

    return data

def main():
    print("Dotfiles script:")
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename", action="store",
                  help="write report to FILE", metavar="FILE")
    dotfile = parser.parse_args().filename
    link.init(log, backup_suffix)
    data = read_config()
    links = data[preset]['links']
    option = input("[i]nstall or [r]ecover or [e]xit:\n")
    if option == "i":
        log("# INSTALLING")
        print_notifier()
        #dep.init(log)
        #dep.install(data[preset]['dependencies'])
        link.install(links)
        log("----------------------------------------------------------------")  
        log("Installation complete!\n")
    if option == "r":
        log("# REMOVING")
        print_notifier()
        link.recover(links)
        log("----------------------------------------------------------------")  
        log("Removal complete!\n")
    if option == "e":
        return

log = logger.create(logfile)
main()
logger.destroy()