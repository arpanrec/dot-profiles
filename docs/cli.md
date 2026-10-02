# `dpf`

A simple and powerful utility for managing your dotfiles.

**Usage**:

```console
$ dpf [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-v, --version`: Display the current version of dot-profiles
* `--help`: Show this message and exit.

Please report bugs at https://github.com/arpanrec/dot-profiles/issues

**Commands**:

* `list`: List all saved profiles.
* `save`: Save the current configuration as a profile.
* `apply`: Apply a saved profile to restore its...
* `remove`: Delete a saved profile permanently.
* `wipe`: Delete all saved profiles (use with...
* `export`: Export a profile as a shareable .dpf...
* `import`: Import a profile from a .dpf archive file.

## `dpf list`

List all saved profiles.

**Usage**:

```console
$ dpf list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `dpf save`

Save the current configuration as a profile.

**Usage**:

```console
$ dpf save [OPTIONS] {name}
```

**Arguments**:

* `name`: Name of the profile  [required]

**Options**:

* `-f, --force`: Overwrite the profile if it already exists
* `--help`: Show this message and exit.

## `dpf apply`

Apply a saved profile to restore its configuration.

**Usage**:

```console
$ dpf apply [OPTIONS] {name}
```

**Arguments**:

* `name`: Name of the profile  [required]

**Options**:

* `--help`: Show this message and exit.

## `dpf remove`

Delete a saved profile permanently.

**Usage**:

```console
$ dpf remove [OPTIONS] {name}
```

**Arguments**:

* `name`: Name of the profile  [required]

**Options**:

* `--help`: Show this message and exit.

## `dpf wipe`

Delete all saved profiles (use with caution!).

**Usage**:

```console
$ dpf wipe [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `dpf export`

Export a profile as a shareable .dpf archive file.

**Usage**:

```console
$ dpf export [OPTIONS] {name}
```

**Arguments**:

* `name`: Name of the profile  [required]

**Options**:

* `-d, --directory <directory>`: Directory for the archive (default: current)
* `-n, --name <archive-name>`: Filename for the exported archive
* `-f, --force`: Overwrite the archive if it already exists
* `--help`: Show this message and exit.

## `dpf import`

Import a profile from a .dpf archive file.

**Usage**:

```console
$ dpf import [OPTIONS] {path}
```

**Arguments**:

* `path`: Path to the .dpf archive file  [required]

**Options**:

* `--help`: Show this message and exit.
