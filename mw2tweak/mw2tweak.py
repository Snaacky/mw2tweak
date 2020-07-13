# Add checker to close the program when MW2 closes after running.
import configparser
import os
import pymem
import pymem.process
import sys
import time

from win32gui import GetWindowText, GetForegroundWindow

# Memory addresses used in MW2 v1.2.211
FOV_ADDRESS = (0x0639322C)  # float
FPS_ADDRESS = (0x638152C)   # int32

# Base configuration parser
config = configparser.RawConfigParser()

# Attempts to load MW2 into Pymem, closes if game not open.
try:
    pm = pymem.Pymem("iw4mp.exe")
except pymem.exception.ProcessNotFound:
    print("MW2 needs to be running first. Exiting...")
    sys.exit(1)


def main():
    # Checks to see if mw2tweak.ini exists, if not, creates default config.
    if not os.path.exists(os.getcwd() + "\mw2tweak.ini"):
        print("Config not found. Creating config with default values.")
        create_config()
        # By default both tweaks are disabled so the user must configure them.
        print("You must configure mw2tweak.ini before continuing. Exiting...")
        sys.exit(0)
    else:
        # Config exists so we can read values from it.
        config.read("mw2tweak.ini")

    # Grabbing the values to see if FPS or FOV tweaks are enabled.
    fps_enabled = config.get("mw2tweak", "fps_enabled")
    fov_enabled = config.get("mw2tweak", "fov_enabled")

    # If both tweaks are disabled, MW2Tweak has nothing to do.
    if "false" in fps_enabled and "false" in fov_enabled:
        print("You have both tweaks disabled. Exiting...")
        sys.exit(1)

    # Passes enabled tweaks to the main tweak_loop.
    tweaks = []

    if "true" in fps_enabled:
        tweaks.append("fps")

    if "true" in fov_enabled:
        tweaks.append("fov")

    tweak_loop(tweaks)


def tweak_loop(tweaks):
    # Loads welcome text and lists off loaded tweaks.
    print("MW2Tweak v1.0 loaded. You have the following tweaks loaded:")
    for tweak in tweaks:
        print("\t-> {}".format(tweak))

    # Grabs values for tweaks if they are enabled.
    if "fov" in tweaks:
        fov_value = config.get("mw2tweak", "fov_value")

    if "fps" in tweaks:
        fps_value = config.get("mw2tweak", "fps_value")

    while True:
        # We only want to write to the game when alt-tabbed in.
        if "Modern Warfare 2" in GetWindowText(GetForegroundWindow()):
            # If tweak is enabled, we will write values to addresses.
            if "fps" in tweaks:
                pm.write_int(FPS_ADDRESS, int(fps_value))

            if "fov" in tweaks:
                pm.write_float(FOV_ADDRESS, float(fov_value))

            # Sleep to save some extra CPU cycles.
            time.sleep(0.1)


def create_config():
    # Creates the default config for MW2Tweak.
    config.add_section("mw2tweak")
    config.set("mw2tweak", "fps_enabled", "false")
    config.set("mw2tweak", "fov_enabled", "false")
    config.set("mw2tweak", "fps_value", "333")
    config.set("mw2tweak", "fov_value", "90")

    with open("mw2tweak.ini", "w") as config_file:
        config.write(config_file)


if __name__ == '__main__':
    main()
