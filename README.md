<h1 align=center> dot-profiles </h1>
<p align=center>A command-line tool that saves and applies your Linux desktop customizations as named profiles. You can export a profile as an archive and import it on another machine. KDE Plasma works out of the box, and the configuration file lets you use any other desktop environment.</p>

---

## Installation

Install from PyPI using pip  
`python -m pip install dot-profiles`

Install from PyPI using pipx  
`pipx install dot-profiles`

## Usage

### Get Help

`dpf -h` or `dpf --help`

### Save current configuration as a profile

`dpf -s <profile name>` or `dpf --save <profile name>`

### Overwrite an already saved profile

`dpf -s <profile name> -f` or `dpf -s <profile name> --force `

### List all profiles

`dpf -l` or `dpf --list`

### Remove a profile

`dpf -r <profile name>` or `dpf --remove <profile name>`

### Apply a profile

`dpf -a <profile name>` or `dpf --apply <profile name>`
You may need to log out and log in to see all the changes.

### Export a profile as a ".dpf" file to share it with your friends!

`dpf -e <profile name>` or `dpf --export-profile <profile name>`

### Export a profile, setting the output dir and archive name

`dpf -e <profile name> -d <archive directory> -n <archive name>`
or
`dpf --export-profile <profile name> --archive-directory <archive directory> --export-name <export name>`

### Export a profile, overwrite files if they already exist

`dpf -e <profile name> -f` or `dpf --export-profile <profile name> --force`
*note: without --force, the export will be appended with the date and time to ensure unique naming and no data is overwritten

### Import a ".dpf" file

`dpf -i <path to the file>` or `dpf --import-profile <path to the file>`

### Show current version

`dpf -v` or `dpf --version`

### Wipe all profiles

`dpf -w` or `dpf --wipe`

---

## Editing the configuration file

You can make changes to the configuration file according to your needs. The configuration file is located in `~/.config/dot-profiles/conf.yaml`.
On first run, dot-profiles writes a KDE Plasma configuration when `$XDG_CURRENT_DESKTOP` is `KDE`, and a minimal generic one otherwise.

### Format

The configuration file should be formatted in the following way:

```yaml
---
save:
    name:
        location: 'path/to/parent/directory'
        entries:
            # These are files to be backed up.
            # They should be present in the specified location.
            - file1
            - file2
export:
    # This includes files which will be exported with your profile.
    # They will not be saved but only be exported and imported.
    # These may include files like complete icon packs and themes..
    name:
        location: 'path/to/parent/directory'
        entries:
            - file1
            - file2
...
```

### Adding more files/folders to backup

You can add more files/folders in the configuration file like this:

```yaml
save:
    name:
        location: 'path/to/parent/directory'
        entries:
            - file1
            - file2
            - folder1
            - folder2
export:
    anotherName:
        location: 'another/path/to/parent/directory'
        entries:
            - file1
            - file2
            - folder1
            - folder2
```

### Using placeholders

You can use a few placeholders in the `location` of each entry in the configuration file. These are:  
`$HOME`: the home directory  
`$CONFIG_DIR`: refers to "$HOME/.config/"  
`$SHARE_DIR`: refers to "$HOME/.local/share"  
`$BIN_DIR`: refers to "$HOME/.local/bin"  
`$DOT_PROFILES_DIR`: refers to "$HOME/.config/dot-profiles"  
`$PROFILES_DIR`: refers to "$HOME/.config/dot-profiles/profiles"  
`${ENDS_WITH="text"}`: for folders with different names on different computers whose names end with the same thing.  
The best example for this is the ".default-release" folder of firefox.  
`${BEGINS_WITH="text"}`: for folders with different names on different computers whose names start with the same thing.

```yaml
save:
    firefox:
        location: "$HOME/.mozilla/firefox/${ENDS_WITH='.default-release'}"
        entries:
            - chrome
```

---

## Contributing

Please read [CONTRIBUTION.md](https://github.com/arpanrec/dot-profiles/blob/master/CONTRIBUTION.md) for info about contributing.

## AI disclosure

AI tools helped write parts of this project's code and documentation. The maintainer reviews the changes before they are merged.

## Acknowledgements

dot-profiles started as a fork of [Konsave](https://github.com/Prayag2/konsave) by Prayag Jain.

## License

This project uses GNU General Public License 3.0
