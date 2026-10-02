"""dot-profiles entry point."""

from __future__ import annotations

import os
from typing import Annotated

import typer

from .consts import CONFIG_FILE, VERSION, length_of_lop, list_of_profiles
from .default_configs import CONF_KDE, CONF_OTHER
from .funcs import (
    apply_profile,
    export,
    import_profile,
    list_profiles,
    remove_profile,
    save_profile,
    wipe,
)

app = typer.Typer(
    name="dpf",
    help="A simple and powerful utility for managing your dotfiles.",
    epilog="Please report bugs at https://github.com/arpanrec/dot-profiles/issues",
    no_args_is_help=True,
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)

ProfileName = Annotated[str, typer.Argument(help="Name of the profile")]


def _show_version(value: bool) -> None:
    """Prints the version and exits when `--version` is passed.

    Args:
        value (bool): Whether `--version` was passed.
    """
    if value:
        print(f"dot-profiles: {VERSION}")
        raise typer.Exit()


@app.callback()
def init(
        version: Annotated[
            bool,
            typer.Option(
                "--version",
                "-v",
                help="Display the current version of dot-profiles",
                callback=_show_version,
                is_eager=True,
            ),
        ] = False,
) -> None:
    """Writes the default configuration file on first run."""
    del version
    if not os.path.exists(CONFIG_FILE):
        default_config = CONF_KDE if os.path.expandvars("$XDG_CURRENT_DESKTOP") == "KDE" else CONF_OTHER
        with open(CONFIG_FILE, "w", encoding="utf-8") as config_file:
            config_file.write(default_config)


@app.command("list")
def list_command() -> None:
    """List all saved profiles."""
    list_profiles(list_of_profiles, length_of_lop)


@app.command("save")
def save_command(
        name: ProfileName,
        force: Annotated[
            bool, typer.Option("--force", "-f", help="Overwrite the profile if it already exists")] = False,
) -> None:
    """Save the current configuration as a profile."""
    save_profile(name, list_of_profiles, force=force)


@app.command("apply")
def apply_command(name: ProfileName) -> None:
    """Apply a saved profile to restore its configuration."""
    apply_profile(name, list_of_profiles, length_of_lop)


@app.command("remove")
def remove_command(name: ProfileName) -> None:
    """Delete a saved profile permanently."""
    remove_profile(name, list_of_profiles, length_of_lop)


@app.command("wipe")
def wipe_command() -> None:
    """Delete all saved profiles (use with caution!)."""
    wipe()


@app.command("export")
def export_command(
        name: ProfileName,
        directory: Annotated[
            str | None,
            typer.Option("--directory", "-d", metavar="<directory>",
                         help="Directory for the archive (default: current)"),
        ] = None,
        archive_name: Annotated[
            str | None,
            typer.Option("--name", "-n", metavar="<archive-name>", help="Filename for the exported archive"),
        ] = None,
        force: Annotated[
            bool, typer.Option("--force", "-f", help="Overwrite the archive if it already exists")] = False,
) -> None:
    """Export a profile as a shareable .dpf archive file."""
    export(name, list_of_profiles, length_of_lop, directory, archive_name, force)


@app.command("import")
def import_command(
        path: Annotated[str, typer.Argument(help="Path to the .dpf archive file")],
) -> None:
    """Import a profile from a .dpf archive file."""
    import_profile(path)


def main() -> None:
    """The `dpf` script entry point."""
    app()


if __name__ == "__main__":
    main()
