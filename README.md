### Dotfiles Manager

A script to manage your unix dotfiles.

- links all the files and folders given in config.json
- keeps the old files
- logs the changes made

Motivation:
A quick shot attempt at making own script for managing dotfiles,
and testing with docker.

The format for dotfiles.json is the following:
```
{
    "default": {
        "links": {
            "<Destination>": "<Source>"
        }
    }
}
```
