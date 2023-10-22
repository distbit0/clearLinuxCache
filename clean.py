import subprocess
import shutil
import argparse
import os


def get_free_space():
    df_output = subprocess.check_output("df /", shell=True, text=True)
    lines = df_output.strip().split("\n")
    headers = lines[0].split()
    values = lines[1].split()
    free_space_index = headers.index("Used")
    free_space_value = int(values[free_space_index]) / 1000000
    return round(free_space_value, 2)


# Parsing command-line arguments
parser = argparse.ArgumentParser(description="Clean-up script")
parser.add_argument("--extreme", action="store_true", help="Perform extreme clean")
parser.add_argument(
    "--username", default=None, help="Specify username to construct home directory path"
)


commands = [
    ["Clearing DNF cache", "dnf clean all"],
    ["Clearing DNF cache", "dnf clean expire-cache"],
    ["Clearing DNF cache", "dnf autoremove -y"],
    ["Clearing systemd journal logs older than 2 days", "journalctl --vacuum-time=2d"],
    # ["Clearing user-specific cache", "rm -rf ~/.cache/*"],  # Note: This affects keepassxc
    ["Clearing Thumbnail cache", "rm -rf ~/.cache/thumbnails/*"],
    ["Clearing CUPS print jobs", "cancel -a"],
    # [
    #     "Deleting old Linux Headers",
    #     "dnf remove --oldinstallonly --setopt installonly_limit=2 kernel"
    # ],
    ["Deleting unused Flatpak packages", "flatpak uninstall --unused"],
    ["Deleting Node Modules cache", "npm cache clean --force"],
    ["Deleting local Python packages cache", "pip cache purge"],
    ["Clearing npm cache", "rm -rf ~/.npm/_cacache/content-v2/sha512/*"],
    ["Clearing VS Code cache", "rm -rf ~/.config/Code/CachedData/*"],
    [
        "Clearing VS Code Extensions cache",
        "rm -rf ~/.config/Code/CachedExtensionVSIXs/*",
    ],
    # ["Clearing Brave Browser Metrics", "rm -rf ~/.config/BraveSoftware/Brave-Browser/BrowserMetrics/*"],
    ["Clearing syslog", "journalctl --vacuum-time=2d"],
    ["Removing syslog.1", "# This would also be covered under journalctl"],
    ["Clearing VS Code cache", "rm -rf ~/.config/Code/Cache/Cache_Data/*"],
    ["Clearing Obsidian cache", "rm -rf ~/.config/obsidian/Cache/Cache_Data/*"],
]

extremeCleanCommands = [
    [
        "Clearing Brave Service Worker cache",
        "rm -rf ~/.config/BraveSoftware/Brave-Browser/Default/Service\\ Worker/*",
    ],
    ["Deleting Signal Attachments", "rm -rf ~/.config/Signal/attachments.noindex/*"],
    ["Deleting Screenshots", "rm -rf ~/Pictures/Screenshots/*"],
    ["Deleting Screencasts", "rm -rf ~/Pictures/Casts/*"],
    ["Empty trash", "rm -rf ~/.local/share/Trash/*"],
    ["Delete misc images in Pictures folder", "rm -rf ~/Pictures/*.png"],
]


def remove_disabled_snaps(home_directory):
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
        "Setting Snap refresh retain limit",
        "snap set system refresh.retain=2",
        home_directory,
    )
    print_and_execute_command(
        "Deleting Snap cache",
        "rm -rf /var/lib/snapd/cache/*",
        home_directory,
    )


def replace_tilde_with_home_directory(command, home_directory):
    return command.replace("~", home_directory)


def print_and_execute_command(description, command, home_directory):
    command = replace_tilde_with_home_directory(command, home_directory)
    print("\n" + description, ":", command + "\n")
    return_code = os.system(command)
    if return_code != 0:
        print(f"Error: Command returned with code {return_code}")


def executeCommands(extremeClean, home_directory):
    if extremeClean:
        print("\nPerforming extreme clean...\n")
        for command in extremeCleanCommands:
            print_and_execute_command(command[0], command[1], home_directory)
    else:
        print("\nPerforming safe clean...\n")
    for command in commands:
        print_and_execute_command(command[0], command[1], home_directory)


if __name__ == "__main__":
    args = parser.parse_args()
    extremeClean = args.extreme

    # abort if not run with sudo
    if not os.geteuid() == 0:
        print("This script must be run as root")
        exit(1)

    if args.username:
        home_directory = f"/home/{args.username}"
    else:
        home_directory = os.path.expanduser("~")

    initial_free_space = get_free_space()
    print("Initial disk usage:", initial_free_space, "GB")
    executeCommands(extremeClean, home_directory)
    remove_disabled_snaps(home_directory)

    final_free_space = get_free_space()
    print("Initial disk usage:", initial_free_space, "GB")
    print("Final disk usage:", final_free_space, "GB")
    print("Freed up:", round(initial_free_space - final_free_space, 3), "GB")
