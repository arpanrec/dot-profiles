"""
Default ``conf.yaml`` contents written on first run.
"""

from __future__ import annotations

CONF_KDE = """---
# This is the configuration file for dot-profiles.
# This file is pre-configured for KDE Plasma users.
# This will backup all the important files for your Plasma customizations.
# Please make sure it follows the correct format for proper working of dot-profiles.
# The format should be:
# ---
# save:
#     name:
#         location: "path/to/parent/directory"
#         entries:
#         # these are files which will be backed up.
#         # They should be present in the specified location.
#             - file1
#             - file2
# export:
#     # This includes files which will be exported with your profile.
#     # They will not be saved but only be exported and imported.
#     # These may include files like complete icon packs and themes..
#     name:
#         location: "path/to/parent/directory"
#         entries:
#             - file1
#             - file2
# ...
# You can use these placeholders in the "location" of each item:
# $HOME: the home directory
# $CONFIG_DIR: refers to "$HOME/.config/"
# $SHARE_DIR: refers to "$HOME/.local/share"
# $BIN_DIR: refers to "$HOME/.local/bin"
# ${ENDS_WITH="text"}: for folders with different names on different computers whose names end with the same thing.
# The best example for this is the "*.default-release" folder of firefox.
# ${BEGINS_WITH="text"}: for folders with different names on different computers whose names start with the same thing.

save:
    configs:
        location: "$CONFIG_DIR"
        entries:
            - gtk-2.0
            - gtk-3.0
            - gtk-4.0
            - kate
            - Kvantum
            - latte
            - dolphinrc
            - katerc
            - konsolerc
            - kcminputrc
            - kdeglobals
            - kglobalshortcutsrc
            - klipperrc
            - krunnerrc
            - kscreenlockerrc
            - ksmserverrc
            - kwinrc
            - kwinrulesrc
            - plasma-org.kde.plasma.desktop-appletsrc
            - plasmarc
            - plasmashellrc
            - gtkrc
            - gtkrc-2.0
            - lattedockrc
            - breezerc
            - oxygenrc
            - lightlyrc
            - ksplashrc
            - khotkeysrc
            # Added for Plasma 6.x compatibility (optional/extra configs)
            - systemsettingsrc
            - kded5rc # renamed from kdedrc (Plasma 6)
            - kconf_updaterc
            - kscreenrc # include if persistent on your system
            - plasma-systemmonitorrc
            - spectaclerc
            - plasmanotifyrc
            - plasma-localerc
            - plasma_calendar_holiday_regions
            - xdg-desktop-portal-kderc
            - kwinoutputconfig.json

    app_layouts:
        location: "$HOME/.local/share/kxmlgui5"
        entries:
            - dolphin
            - konsole
            - yakuakerc
            # Optional application GUI layout overrides (add if present)
            - systemsettings
            - spectacle
            - plasma-systemmonitor

    # Autostart user .desktop entries (do NOT include distro defaults)
    autostart:
        location: "$CONFIG_DIR/autostart"
        entries:
            # Add/remove entries above if your autostart changes.

    # Here are a few examples of how you can add more stuff to back up.
    # Uncomment these lines if you want.
    # firefox:
    #     location: "$HOME/.mozilla/firefox/${ENDS_WITH='.default-release'}"
    #     entries:
    #         - chrome # for firefox customizations

    # code oss:
    #     location: "$CONFIG_DIR/Code - OSS/User/"
    #     entries:
    #         - settings.json

# The following files will only be used for exporting and importing.
export:
    share_folder:
        location: "$SHARE_DIR"
        entries:
            - plasma
            - kwin
            - konsole
            - fonts
            - color-schemes
            - aurorae
            - icons
            - wallpapers
            - yakuake

    home_folder:
        location: "$HOME/"
        entries:
            - .fonts
            - .themes
            - .icons

    # You can add more files to export like this
    # name:
    #     location: "path/to/parent/directory"
    #     entries:
    #         - file1
    #         - file2
    #         - folder1
    #         - folder2
...
"""

CONF_OTHER = """---
# This is the configuration file for dot-profiles.
# Please make sure it follows the correct format for proper working of dot-profiles.
# The format should be:
# ---
# save:
#     name:
#         location: "path/to/parent/directory"
#         entries:
#         # these are files to be backed up. They should be present in the specified location.
#             - file1
#             - file2
# export:
#     # This includes files which will be exported with your profile.
#     # They will not be saved but only be exported and imported.
#     # These may include files like complete icon packs and themes..
#     name:
#         location: "path/to/parent/directory"
#         entries:
#             - file1
#             - file2
# ...
# You can use these variables and functions in the locations of different entries:
# $HOME: the home directory
# $PROFILES_DIR: directory where all profiles are saved
# $CONFIG_DIR: refers to "$HOME/.config/"
# $DOT_PROFILES_DIR: the location where all dot-profiles files are stored ("$CONFIG_DIR/dot-profiles").
# ${ENDS_WITH="text"}: for folders with different names on different computers but their names end with the same thing.
# The best example for this is the ".default-release" folder for firefox.
# ${BEGINS_WITH="text"}: for folders with different names on different computers but their names start with the same
# thing.

# The following files will be saved in your profiles
save:
    configs:
        location: "$HOME/.config"
        entries:
            # add config files and folders to backup here like this
            # - file1
            # - file2
            # - folder1

    # Here are a few examples of how you can add more stuff to back up
    # firefox:
    #     location: "$HOME/.mozilla/firefox/${ENDS_WITH='.default-release'}"
    #     entries:
    #         - chrome # for firefox customizations

    # oss:
    #     location: "$HOME/.config/Code - OSS/User/"
    #     entries:
    #         - settings.json

# The following files will only be used for exporting and importing.
export:
    share_folder:
        location: "$HOME/.local/share"
        entries:
            # add files/folders to export from "~/.local/share" here
    home_folder:
        location: "$HOME/"
        entries:
            # add files/folders to export from the home directory here

    # You can add more files to export like this
    # name:
    # location: "path"
    # entries:
    # - file1
    # - file2
    # - folder1
    # - folder2
...
"""
