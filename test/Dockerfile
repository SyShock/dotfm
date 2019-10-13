FROM python:alpine
RUN mkdir /dotfiles
WORKDIR /dotfiles
ARG folderVariable="./"
COPY ${folderVariable} /dotfiles
RUN python ./install.py -f "./sample/dotfiles.json" -p whatever -o i
RUN python ./install.py -f "./sample/dotfiles.json" -p custom -o i
RUN python ./install.py -f "./sample/dotfiles.json" -o r