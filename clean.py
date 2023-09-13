import subprocess
import shutil


home_directory = "/home/pimania"  # specify your custom home directory here


commands = [
    ["Clearing apt cache", "sudo apt clean"],
    ["Clearing old downloaded archive files", "sudo apt-get autoclean"],
    ["Clearing old unused kernel and dependencies", "sudo apt autoremove --purge"],
    (
        "Clearing systemd journal logs older than 1 day",
        "sudo journalctl --vacuum-time=5h",
    ),
    ["Clearing user-specific cache", "rm -rf ~/.cache/*"],
    (
        "Clearing Brave browser cache",
        "rm -rf ~/.config/BraveSoftware/Brave-Browser/Default/Cache/*",
    ),
    ["Clearing Thumbnail cache", "rm -rf ~/.cache/thumbnails/*"],
    ["Clearing CUPS print jobs", "cancel -a"],
    (
        "Deleting old configuration files",
        "sudo dpkg -l | grep '^rc' | awk '{print $2}' | xargs sudo dpkg --purge",
    ),
    (
        "Deleting old Linux Headers",
        "sudo apt autoremove --purge -y $(dpkg --list | grep linux-image | awk '{ print $2 }' | sort -V | sed -n '/'`uname -r`'/q;p')",
    ),
    ["Deleting unused Flatpak packages", "flatpak uninstall --unused"],
    ["Deleting Signal Attachments", "rm -rf ~/.config/Signal/attachments.noindex/*"],
    ["Deleting Zoom cache", "rm -rf ~/.zoom/*"],
    ["Deleting Node Modules cache", "npm cache clean --force"],
    ["Deleting local Python packages cache", "pip cache purge"],
    (
        "Clearing Brave Service Worker cache",
        "rm -rf ~/.config/BraveSoftware/Brave-Browser/Default/Service\\ Worker/*",
    ),
    ["Clearing npm cache", "rm -rf ~/.npm/_cacache/content-v2/sha512/*"],
    ["Clearing VS Code cache", "rm -rf ~/.config/Code/CachedData/*"],
    (
        "Clearing VS Code Extensions cache",
        "rm -rf ~/.config/Code/CachedExtensionVSIXs/*",
    ),
    (
        "Clearing Brave Browser Metrics",
        "rm -rf /home/pimania/.config/BraveSoftware/Brave-Browser/BrowserMetrics/*",
    ),
    ["Purging autoremovable packages", "apt --purge autoremove"],
    ["Clearing syslog", "cat /dev/null > /var/log/syslog"],
    ["Removing syslog.1", "rm /var/log/syslog.1"],
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
    print_and_execute_command(
        "Deleting Snap cache", "sudo rm -rf /var/lib/snapd/cache/*"
    )


def replace_tilde_with_home_directory(command):
    return command.replace("~", home_directory)


def print_and_execute_command(description, command):
    print(f"\n{description}\n")
    command = replace_tilde_with_home_directory(command)
    result = subprocess.run(
        command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE
    )
    if result.returncode != 0:
        print(f"Error: {result.stderr.decode()}")


def executeCommands():
    for command in commands:
        print_and_execute_command(command[0], command[1])


if __name__ == "__main__":
    print("\nPerforming safe delete operations...\n")
    executeCommands()
    remove_disabled_snaps()
