'''
Author: SyShock
Description: this script installs the dotfiles on your system, it has two options: install or recover
Additional: this script does not install the missing dependencies that the dotfiles' programs will use, yet...
'''
# DEFAULT CONFIG
logfile = "setup.log"
dotfile = "dotfiles.json"
backup_suffix = "__backup"
preset = "default"
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
    parser.add_argument("-f", "--file", dest="filename",
                        help="read from FILE", metavar="FILE")
    parser.add_argument("-o", "--option", dest="option", required=False,
                        help="set OPTION without propting for one", metavar="OPTION")
    args = parser.parse_args()
    dotfile = args.filename
    option = args.option

    link.init(log, backup_suffix)
    data = read_config()

    links = data[preset]['links']
    deps = data[preset]['dependencies']
    if option=="None":
        option = input("[i]nstall [r]ecover [l]ist-deps [e]xit:\n")
    if option == "i":
        log("# INSTALLING")
        print_notifier()
        dep.init(log)
        #dep.install(deps)
        link.install(links)
        dep.list(deps)
        log("----------------------------------------------------------------")  
        log("Installation complete!\n")
    if option == "r":
        log("# REMOVING")
        print_notifier()
        link.recover(links)
        log("----------------------------------------------------------------")  
        log("Removal complete!\n")
    if option == "l":
        print("----------------------------------------------------------------")
        dep.init(log)
        dep.list(deps)
        print("----------------------------------------------------------------")
    if option == "e":
        return

log = logger.create(logfile)
main()
logger.destroy()
