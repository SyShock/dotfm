FROM python:alpine
RUN mkdir /dotfiles
WORKDIR /dotfiles
ARG folderVariable="./"
COPY ${folderVariable} /dotfiles
RUN python ./install.py -f "./sample/test.json" -o i
RUN python ./install.py -f "./sample/test.json" -o r