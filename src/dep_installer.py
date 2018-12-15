import subprocess

def exec(commands):
    return subprocess.check_output(commands)

def _iterate(list, cmd):
    for item in list:
        try:
            exec([cmd, list[item]])
            log("Performed: " + list[item])
        except TypeError:
            exec([cmd, item])
            log("Instelled: " + item)

def init(logger):
    global log
    log = logger
    # print("This preset has dependencies how do you want to handle this?")
    # option = input("[m]anually or [a]uto ")
    # if option == "a":
        #exec(["wget", "https://github.com/icy/pacapt/raw/ng/pacapt", "-O", "./pacapt"])
        #exec(["chmod", "755", "./pacapt"])

def list(deps):
     for item in deps:
        print(item+": "+deps[item])


def install(deps):
    packages = deps['package']
    for item in packages:
        # query = exec(["./pacapt", "-Q", item]) 
        # exec(["./pacapt", "-Q", "-s", item])
        exec(["./pacapt", "-S", item])

    # scripts/other (wget and shit)
    _iterate(deps['other'], '')

    # python
    _iterate(deps['python'], ['pip', 'install'])

    # pip_list = exec(["pip", "list"])
    #     # startloop
    # if not pip_list.find(item):
    #     exec(["pip", "install", item])

    # npm
    _iterate(deps['node'], ['npm', 'install' '-g'])
    # exec(["npm", "list", "-g", item]) # tree
