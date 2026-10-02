"""
This module contains all the functions for dot-profiles.
"""

from __future__ import annotations

import functools
import os
import shutil
import traceback
from collections.abc import Callable
from datetime import datetime
from typing import Any
from zipfile import ZipFile, is_zipfile

import yaml

from .consts import CONFIG_FILE, DOT_PROFILES_DIR, EXPORT_EXTENSION, HOME, PROFILES_DIR
from .parse import TOKEN_SYMBOL, parse_functions, parse_keywords, tokens


def exception_handler[**P, R](func: Callable[P, R]) -> Callable[P, R | None]:
    """Handles errors and prints nicely.

    Args:
        func: any function

    Returns:
        Returns function
    """

    @functools.wraps(func)
    def inner_func(*args: P.args, **kwargs: P.kwargs) -> R | None:
        try:
            function = func(*args, **kwargs)
        except Exception as err:  # pylint: disable=broad-exception-caught
            dateandtime = datetime.now().strftime("[%d/%m/%Y %H:%M:%S]")
            log_file = os.path.join(HOME, ".cache/dot-profiles.log")

            with open(log_file, "a", encoding="utf-8") as file:
                file.write(dateandtime + "\n")
                traceback.print_exc(file=file)
                file.write("\n")

            print(f"dot-profiles: {err}\nPlease check the log at {log_file} for more details.")
            return None

        return function

    return inner_func


def mkdir(path: str) -> str:
    """Creates directory if it doesn't exist.

    Args:
        path: path to the new directory

    Returns:
        path: the same path
    """
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def log(msg: str, *args: Any, **kwargs: Any) -> None:
    """Logs text.

    Args:
        msg: the text to be printed
        *args: any arguments for the function print()
        **kwargs: any keyword arguments for the function print()
    """
    print(f"dot-profiles: {msg}", *args, **kwargs)


@exception_handler
def copy(source: str, dest: str) -> None:
    """
    This function was created because shutil.copytree gives error if the destination folder
    exists and the argument "dirs_exist_ok" was introduced only after python 3.8.
    This restricts people with python 3.7 or less from using dot-profiles.
    This function will let people with python 3.7 or less use dot-profiles without any issues.
    It uses recursion to copy files and folders from "source" to "dest"

    Args:
        source: the source destination
        dest: the destination to copy the file/folder to
    """
    assert isinstance(source, str) and isinstance(dest, str), "Invalid path"
    assert source != dest, "Source and destination can't be same"
    assert os.path.exists(source), "Source path doesn't exist"

    if not os.path.exists(dest):
        os.mkdir(dest)

    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        dest_path = os.path.join(dest, item)

        if os.path.isdir(source_path):
            copy(source_path, dest_path)
        else:
            if os.path.exists(dest_path):
                os.remove(dest_path)
            if os.path.exists(source_path):
                shutil.copy(source_path, dest)


def copy_entry(source: str, dest: str) -> None:
    """Copies a file or folder to "dest" if "source" exists.

    Args:
        source: the file or folder to copy
        dest: the destination of the copy
    """
    if os.path.exists(source):
        if os.path.isdir(source):
            copy(source, dest)
        else:
            shutil.copy(source, dest)


def section_entries(section: dict[str, Any]) -> tuple[str, list[str]]:
    """Returns the location and the entries of a "conf.yaml" section.

    Args:
        section: one named section of "save" or "export"
    """
    location: str = section["location"]
    entries: list[str] = section["entries"]
    return location, entries


def read_config(config_file: str) -> dict[str, Any]:
    """Reads "conf.yaml" and parses it.

    Args:
        config_file: path to the config file
    """
    with open(config_file, encoding="utf-8") as text:
        config: dict[str, Any] = yaml.safe_load(text.read())
    parse_keywords(tokens, TOKEN_SYMBOL, config)
    parse_functions(tokens, TOKEN_SYMBOL, config)

    # in some cases conf.yaml may contain nothing in "entries". Yaml parses
    # these as NoneType which are not iterable which throws an exception
    # we can convert all None-Entries into empty lists recursively so they
    # are simply skipped in loops later on
    def convert_none_to_empty_list(data: Any) -> Any:
        if data is None:
            return []
        if isinstance(data, list):
            return [convert_none_to_empty_list(item) for item in data]  # pyright: ignore[reportUnknownVariableType]
        if isinstance(data, dict):
            return {  # pyright: ignore[reportUnknownVariableType]
                key: convert_none_to_empty_list(value)
                for key, value in data.items()  # pyright: ignore[reportUnknownVariableType]
            }
        return data

    return convert_none_to_empty_list(config)


@exception_handler
def list_profiles(profile_list: list[str], profile_count: int) -> None:
    """Lists all the created profiles.

    Args:
        profile_list: the list of all created profiles
        profile_count: number of profiles created
    """

    # assert
    assert os.path.exists(PROFILES_DIR) and profile_count != 0, "No profile found."

    # sort in alphabetical order
    profile_list.sort()

    # run
    print("dot-profiles profiles:")
    print("ID\tNAME")
    for i, item in enumerate(profile_list):
        print(f"{i + 1}\t{item}")


@exception_handler
def save_profile(name: str, profile_list: list[str], force: bool = False) -> None:
    """Saves necessary config files in ~/.config/dot-profiles/profiles/<name>.

    Args:
        name: name of the profile
        profile_list: the list of all created profiles
        force: force overwrite already created profile, optional
    """

    # assert
    assert name not in profile_list or force, "Profile with this name already exists"

    # run
    log("saving profile...")
    profile_dir = os.path.join(PROFILES_DIR, name)
    mkdir(profile_dir)

    config = read_config(CONFIG_FILE)["save"]

    for section in config:
        location, entries = section_entries(config[section])
        folder = os.path.join(profile_dir, section)
        mkdir(folder)
        for entry in entries:
            source = os.path.join(location, entry)
            dest = os.path.join(folder, entry)
            copy_entry(source, dest)

    shutil.copy(CONFIG_FILE, profile_dir)

    log("Profile saved successfully!")


@exception_handler
def apply_profile(profile_name: str, profile_list: list[str], profile_count: int) -> None:
    """Applies profile of the given id.

    Args:
        profile_name: name of the profile to be applied
        profile_list: the list of all created profiles
        profile_count: number of profiles created
    """

    # assert
    assert profile_count != 0, "No profile saved yet."
    assert profile_name in profile_list, "Profile not found :("

    # run
    profile_dir = os.path.join(PROFILES_DIR, profile_name)

    log("copying files...")

    config_location = os.path.join(profile_dir, "conf.yaml")
    profile_config = read_config(config_location)["save"]
    for name in profile_config:
        location = os.path.join(profile_dir, name)
        copy(location, profile_config[name]["location"])

    log("Profile applied successfully! Please log-out and log-in to see the changes completely!")


@exception_handler
def remove_profile(profile_name: str, profile_list: list[str], profile_count: int) -> None:
    """Removes the specified profile.

    Args:
        profile_name: name of the profile to be removed
        profile_list: the list of all created profiles
        profile_count: number of profiles created
    """

    # assert
    assert profile_count != 0, "No profile saved yet."
    assert profile_name in profile_list, "Profile not found."

    # run
    log("removing profile...")
    shutil.rmtree(os.path.join(PROFILES_DIR, profile_name))
    log("removed profile successfully")


def stage_export(profile_dir: str, export_path: str) -> None:
    """Copies the saved and exportable files of a profile into the "export_path" folder.

    Args:
        profile_dir: directory of the saved profile
        export_path: the folder that is later archived
    """
    profile_config_file = os.path.join(profile_dir, "conf.yaml")
    config = read_config(profile_config_file)

    export_path_save = mkdir(os.path.join(export_path, "save"))
    for name in config["save"]:
        location = os.path.join(profile_dir, name)
        log(f'Exporting "{name}"...')
        copy(location, os.path.join(export_path_save, name))

    config_export = config["export"]
    export_path_export = mkdir(os.path.join(export_path, "export"))
    for name in config_export:
        location, entries = section_entries(config_export[name])
        path = mkdir(os.path.join(export_path_export, name))
        for entry in entries:
            source = os.path.join(location, entry)
            dest = os.path.join(path, entry)
            log(f'Exporting "{entry}"...')
            copy_entry(source, dest)


@exception_handler
def export(
    profile_name: str,
    profile_list: list[str],
    profile_count: int,
    archive_dir: str | None,
    archive_name: str | None,
    force: bool,
) -> None:
    """It will export the specified profile as a ".dpf" to the specified directory.
       If there is no specified directory, the directory is set to the current working directory.

    Args:
        profile_name: name of the profile to be exported
        profile_list: the list of all created profiles
        profile_count: number of profiles created
        archive_dir: output directory for the export
        archive_name: the name of the resulting archive
        force: force the overwrite of existing export file
    """

    # assert
    assert profile_count != 0, "No profile saved yet."
    assert profile_name in profile_list, "Profile not found."

    # run
    profile_dir = os.path.join(PROFILES_DIR, profile_name)

    if archive_name:
        profile_name = archive_name

    export_path = os.path.join(archive_dir or os.getcwd(), profile_name)

    # Only continue if export_path, export_path.ksnv and export_path.zip don't exist
    # Appends date and time to create a unique file name
    if not force:
        while True:
            paths = [f"{export_path}", f"{export_path}.dpf", f"{export_path}.zip"]
            if any(os.path.exists(path) for path in paths):
                time = f"f{datetime.now():%d-%m-%Y:%H-%M-%S}"
                export_path = f"{export_path}_{time}"
            else:
                break

    # compressing the files as zip
    log("Exporting profile. It might take a minute or two...")

    stage_export(profile_dir, export_path)

    shutil.copy(CONFIG_FILE, export_path)

    log("Creating archive")
    shutil.make_archive(export_path, "zip", export_path)

    shutil.rmtree(export_path)
    shutil.move(export_path + ".zip", export_path + EXPORT_EXTENSION)

    log(f"Successfully exported to {export_path}{EXPORT_EXTENSION}")


@exception_handler
def import_profile(path: str) -> None:
    """This will import an exported profile.

    Args:
        path: path of the `.dpf` file
    """

    # assert
    assert is_zipfile(path) and path[-5:] == EXPORT_EXTENSION, "Not a valid dot-profiles file"
    item = os.path.basename(path)[:-5]
    assert not os.path.exists(os.path.join(PROFILES_DIR, item)), "A profile with this name already exists"

    # run
    log("Importing profile. It might take a minute or two...")

    item = os.path.basename(path).replace(EXPORT_EXTENSION, "")

    temp_path = os.path.join(DOT_PROFILES_DIR, "temp", item)

    with ZipFile(path, "r") as zip_file:
        zip_file.extractall(temp_path)

    config_file_location = os.path.join(temp_path, "conf.yaml")
    config = read_config(config_file_location)

    profile_dir = os.path.join(PROFILES_DIR, item)
    copy(os.path.join(temp_path, "save"), profile_dir)
    shutil.copy(os.path.join(temp_path, "conf.yaml"), profile_dir)

    for section in config["export"]:
        location, entries = section_entries(config["export"][section])
        path = os.path.join(temp_path, "export", section)
        mkdir(path)
        for entry in entries:
            source = os.path.join(path, entry)
            dest = os.path.join(location, entry)
            log(f'Importing "{entry}"...')
            copy_entry(source, dest)

    shutil.rmtree(temp_path)

    log("Profile successfully imported!")


@exception_handler
def wipe() -> None:
    """Wipes all profiles."""
    confirm = input('This will wipe all your profiles. Enter "WIPE" To continue: ')
    if confirm == "WIPE":
        shutil.rmtree(PROFILES_DIR)
        log("Removed all profiles!")
    else:
        log("Aborting...")
