import psutil

def print_storage_info():
    # Get disk partitions
    partitions = psutil.disk_partitions()

    print("Storage Information:")
    for partition in partitions:
        print(f"Mount Point: {partition.mountpoint}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            print(f"Total: {convert_bytes(partition_usage.total)}")
            print(f"Used: {convert_bytes(partition_usage.used)}")
            print(f"Free: {convert_bytes(partition_usage.free)}")
            print(f"Percentage Used: {partition_usage.percent}%")
            print("-" * 30)
        except Exception as e:
            print(f"Error reading {partition.mountpoint} information: {e}")

def convert_bytes(bytes):
    # Convert bytes to a human-readable format
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            break
        bytes /= 1024.0
    return f"{bytes:.2f} {unit}"


import platform
import os

def print_system_info():
    print("System Information:")
    print(f"OS: {platform.system()} {platform.version()}")
    print(f"OS Type: {platform.system()} {platform.architecture()}")
    print(f"Python Version: {platform.python_version()}")
    print("-" * 30)

def print_user_info():
    print("User Information:")
    print(f"Current User: {os.getlogin()}")
    try:
        import pwd
        user_info = pwd.getpwnam(os.getlogin())
        print(f"User ID: {user_info.pw_uid}")
        print(f"Group ID: {user_info.pw_gid}")
        print(f"Home Directory: {user_info.pw_dir}")
    except (ImportError, KeyError):
        pass
    print("-" * 30)

def print_directory_list():
    print("Directory List:")
    current_directory = os.getcwd()
    print(f"Current Directory: {current_directory}")
    print("Contents:")
    try:
        with os.scandir(current_directory) as entries:
            for entry in entries:
                print(entry.name)
    except Exception as e:
        print(f"Error reading directory information: {e}")


if __name__ == "__main__":
    print_storage_info()
    print_system_info()
    print_user_info()
    print_directory_list()
