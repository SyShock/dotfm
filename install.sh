#!/bin/sh
proj=".dotfm"
file="dotfiles.json"

usage() {
  cat << EOF >&2
    Usage: $PROGNAME [-f <file>]
    -f <file>: config file you'd like to use
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
    while getopts "f:" opt; do
        case $opt in
            (f) file=$OPTARG;;
            (*) usage
        esac
    done
    if [ -e "../$proj" ]; then
        cd ..
    fi
    if [ ! -e "./$proj/src/setup_dotfiles.py" ]; then
        git submodule update --init --recursive
    fi
    python ./$proj/src/setup_dotfiles.py -f $file
}

if [ ! -e "$proj" ] && [ ! -e "../$proj" ]; then
    init
else
    install $*

    # post-install 
    
fi

