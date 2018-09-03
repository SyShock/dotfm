FROM python:alpine
RUN mkdir /dotfiles
WORKDIR /dotfiles
ARG folderVariable="./"
COPY ${folderVariable} /dotfiles
RUN sh ./install.sh
RUN echo "i" | sh ./install.sh
RUN echo "r" | sh ./install.sh