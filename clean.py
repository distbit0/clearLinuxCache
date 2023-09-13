import subprocess
import shutil
import argparse
import os

# Parsing command-line arguments
parser = argparse.ArgumentParser(description="Clean-up script")
parser.add_argument("--extreme", action="store_true", help="Perform extreme clean")


commands = [
    ["Clearing apt cache", "apt clean -y"],
    ["Clearing old downloaded archive files", "apt-get autoclean -y"],
    [
        "Clearing systemd journal logs older than 1 day",
        "journalctl --vacuum-time=5h",
    ],
    ["Clearing user-specific cache", "rm -rf ~/.cache/*"],
    ["Clearing Thumbnail cache", "rm -rf ~/.cache/thumbnails/*"],
    ["Clearing CUPS print jobs", "cancel -a"],
    [
        "Deleting old configuration files",
        "dpkg -l | grep '^rc' | awk '{print $2}' | xargs dpkg --purge",
    ],
    [
        "Deleting old Linux Headers",
        "apt autoremove --purge -y $(dpkg --list | grep linux-image | awk '{ print $2 }' | sort -V | sed -n '/'`uname -r`'/q;p')",
    ],
    ["Deleting unused Flatpak packages", "flatpak uninstall --unused"],
    ["Deleting Node Modules cache", "npm cache clean --force"],
    ["Deleting local Python packages cache", "pip cache purge"],
    ["Clearing npm cache", "rm -rf ~/.npm/_cacache/content-v2/sha512/*"],
    ["Clearing VS Code cache", "rm -rf ~/.config/Code/CachedData/*"],
    [
        "Clearing VS Code Extensions cache",
        "rm -rf ~/.config/Code/CachedExtensionVSIXs/*",
    ],
    [
        "Clearing Brave Browser Metrics",
        "rm -rf ~/.config/BraveSoftware/Brave-Browser/BrowserMetrics/*",
    ],
    ["Purging autoremovable packages", "apt autoremove -y --purge"],
    ["Clearing syslog", "cat /dev/null > /var/log/syslog"],
    ["Removing syslog.1", "rm /var/log/syslog.1"],
    ["Clearing VS Code cache", "rm -rf ~/.config/Code/Cache/Cache_Data/*"],
    ["Clearing VS Code cache", "rm -rf ~/.config/Obsidian/Cache/Cache_Data/*"],
]

extremeCleanCommands = [
    [
        "Clearing Brave Service Worker cache",
        "rm -rf ~/.config/BraveSoftware/Brave-Browser/Default/Service\\ Worker/*",
    ],
    ["Deleting Signal Attachments", "rm -rf ~/.config/Signal/attachments.noindex/*"],
    ["Deleting Screenshots", "rm -rf ~/Pictures/Screenshots/*"],
    ["Deleting Screencasts", "rm -rf ~/Pictures/Casts/*"],
]


def remove_disabled_snaps():
    # Check if Snap is installed
    if shutil.which("snap") is None:
        print("Snap is not installed. Exiting function.")
        return

    print("\nRemoving disabled Snap packages\n")
    snap_list_output = subprocess.check_output("snap list --all", shell=True, text=True)
    for line in snap_list_output.split("\n"):
        if "disabled" in line:
            _, snapname, _, revision = line.split()[:4]
            subprocess.run(f"snap remove {snapname} --revision={revision}", shell=True)

    # Assuming print_and_execute_command is defined elsewhere in your code
    print_and_execute_command(
        "Setting Snap refresh retain limit", "snap set system refresh.retain=2"
    )
    print_and_execute_command("Deleting Snap cache", "rm -rf /var/lib/snapd/cache/*")


def replace_tilde_with_home_directory(command):
    home_directory = os.path.expanduser("~")
    return command.replace("~", home_directory)


def print_and_execute_command(description, command):
    print(f"\n{description}\n")
    command = replace_tilde_with_home_directory(command)
    return_code = os.system(command)

    if return_code != 0:
        print(f"Error: Command returned with code {return_code}")


def executeCommands(extremeClean=False):
    if extremeClean:
        print("\nPerforming extreme clean...\n")
        for command in extremeCleanCommands:
            print_and_execute_command(command[0], command[1])
    else:
        print("\nPerforming safe clean...\n")
    for command in commands:
        print_and_execute_command(command[0], command[1])


if __name__ == "__main__":
    args = parser.parse_args()
    extremeClean = args.extreme
    executeCommands(extremeClean)
    remove_disabled_snaps()
