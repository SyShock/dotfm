#!/bin/sh

# Default config
proj=".dotfm"
file="dotfiles.json"
option="None"
################

usage() {
  cat << EOF >&2
    Usage: $PROGNAME [-f <file>] [-i <install>] [-r <remove>] [-l <list>] 
    -f <file>: config file you'd like to use
    -i <install> -r <remove> -l <list>: option you'd like to use without being prompted
EOF
  exit 1
}

init() {
    mkdir $proj
    cd $proj
    mv ../* .
    cd ..
    cp ./$proj/install.sh ./
    cp ./$proj/sample/dotfiles.json ./
    cp ./$proj/sample/DEPENDENCIES.md ./
    mkdir dotfiles
    echo "Installed. You can now place your dotfiles in the ./dotfiles folder."
}

install() {
    while getopts "f:ilr" opt; do
        case $opt in
            (f) file=$OPTARG;;
            (i) option="i";;
            (l) option="l";;
            (r) option="r";;
            (*) usage
        esac
    done

    if [ -e "../$proj" ]; then
        cd ..
    fi

    if [ ! -e "./$proj/src/setup_dotfiles.py" ]; then
        git submodule update --init --recursive
    fi

    err_message=$(python ./$proj/src/setup_dotfiles.py -f $file -o $option 1>/dev/stdin 2>&1)
    echo $err_message
}

if [ ! -e "$proj" ] && [ ! -e "../$proj" ]; then
    init
else
    install $*

    if [[ option == "i" ]] && [[ -z err_message ]]; then
        # post-install 
        source ./preprocessor.sh
    fi
fi

