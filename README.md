# DotFM

## Dotfiles Manager

A script to manage your unix dotfiles.

- links all the files and folders given in config.json
- keeps the old files
- logs the changes made
- integration  testing with docker

## Motivation

Wanted to make own script for managing dotfiles

### Parameters

```text
optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  read from FILE
  -o OPTION, --option OPTION
                        set OPTION without propting for one
  -p PRESET, --preset PRESET
                        specify preset
```

The format for dotfiles.json is the following:

```JSON
{
    "default": {
        "dependencies": {
            "example": "github.com/example.git"
        },
        "links": {
            "<Destination>": "<Source>"
        }
    }
}
```

You use different presets like this:

```JSON
    ...
    "custom": {
        "links": {
            "<Destination>": "<Source>"
        }
    }
```

Just remember to specify this preset on execution

## Testing

```bash
# from project root
bash ./test/test.sh
```
