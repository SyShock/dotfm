#!/bin/sh
proj=".dotfm"

if [ ! -e "$proj" ] && [ ! -e "../$proj" ]; then
    mkdir $proj
    cd $proj
    mv ../* .
    cd ..
    cp ./$proj/install.sh ./
    cp ./$proj/sample/dotfiles.json ./
    cp ./$proj/sample/DEPENDENCIES.md ./
    mkdir dotfiles
    echo "Installed. You can now place your dotfiles in the ./dotfiles folder."
else
    if [ -e "../$proj" ]; then
        cd ..
    fi
    if [ ! -e "./$proj/src/setup_dotfiles.py" ]; then
        git submodule update --init --recursive
    fi
    python ./$proj/src/setup_dotfiles.py
fi
