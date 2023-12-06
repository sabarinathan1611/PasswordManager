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

if __name__ == "__main__":
    print_storage_info()
