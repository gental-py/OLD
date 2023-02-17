import platform
import psutil
import GPUtil

def pcinfo(_Command):

    BROWN = "\033[0;33m"
    PURPLE = "\033[0;35m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BLUE = "\033[0;34m"
    CYAN = "\033[0;36m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    BLINK = "\033[5m"
    END = "\033[0m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"

    class PreMessage:
        error = f"{LIGHT_BLUE}[{RED}!{LIGHT_BLUE}]{END}"
        notification = f"{LIGHT_BLUE}[{LIGHT_RED}*{LIGHT_BLUE}]{END}"
        column = f"{LIGHT_BLUE}[{LIGHT_RED}-{LIGHT_BLUE}]{END}"

    pcinfo_toShow_cpu = False
    pcinfo_toShow_gpu = False
    pcinfo_toShow_ram = False
    pcinfo_toShow_net = False
    pcinfo_toShow_disk = False

    if "-all" in _Command.lower():
        pcinfo_toShow_cpu = True
        pcinfo_toShow_gpu = True
        pcinfo_toShow_ram = True
        pcinfo_toShow_net = True
        pcinfo_toShow_disk = True

    else:
        if "-cpu" in _Command.lower():
            pcinfo_toShow_cpu = True

        if "-gpu" in _Command.lower():
            pcinfo_toShow_gpu = True

        if "-ram" in _Command.lower():
            pcinfo_toShow_ram = True

        if "-net" in _Command.lower():
            pcinfo_toShow_net = True

        if "-disk" in _Command.lower():
            pcinfo_toShow_disk = True


    def get_size(bytes, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor


    uname = platform.uname()
    cpufreq = psutil.cpu_freq()
    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    if pcinfo_toShow_cpu:
        print(f"{BLUE}=== {LIGHT_RED}CPU {BLUE}===")
        print(f"{LIGHT_BLUE}Physical Cores:{LIGHT_RED}", psutil.cpu_count(logical=False))
        print(f"{LIGHT_BLUE}Total cores:{LIGHT_RED}", psutil.cpu_count(logical=True))
        print(f"{LIGHT_BLUE}Frequency:{LIGHT_RED} {cpufreq.max:.2f}Mhz")
        print(f"{LIGHT_BLUE}Total CPU Usage:{LIGHT_RED} {psutil.cpu_percent()}%\n")

    if pcinfo_toShow_gpu:
        print(f"{BLUE}=== {LIGHT_RED}GPU {BLUE}===")
        gpus = GPUtil.getGPUs()
        list_gpus = []
        for gpu in gpus:
            print(f"{LIGHT_BLUE}Name:{LIGHT_RED}", gpu.name)
            gpu_load = f"{gpu.load * 100}%"
            print(f"{LIGHT_BLUE}Usage:{LIGHT_RED}", gpu_load)
            gpu_total_memory = f"{gpu.memoryTotal}MB"
            print(f"{LIGHT_BLUE}Memory:{LIGHT_RED}", gpu_total_memory)
            gpu_temperature = f"{gpu.temperature} °C"
            print(f"{LIGHT_BLUE}Temperature:{LIGHT_RED}", gpu_temperature)
            print(f"{LIGHT_BLUE}UUID:{LIGHT_RED}", gpu.uuid, "\n")

    if pcinfo_toShow_ram:
        print(f"{BLUE}=== {LIGHT_RED}RAM {BLUE}===")
        print(f"{LIGHT_BLUE}Total:{LIGHT_RED} {get_size(svmem.total)}")
        print(f"{LIGHT_BLUE}Available:{LIGHT_RED} {get_size(svmem.available)}")
        print(f"{LIGHT_BLUE}Used:{LIGHT_RED} {get_size(svmem.used)}")
        print(f"{LIGHT_BLUE}Percentage:{LIGHT_RED} {svmem.percent}%\n")

    if pcinfo_toShow_net:
        print(f"{BLUE}=== {LIGHT_RED}NET {BLUE}===")
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    print(f"{LIGHT_BLUE}IP Address:{LIGHT_RED} {address.address}")
                    print(f"{LIGHT_BLUE}Netmask:{LIGHT_RED} {address.netmask}")
                    print(f"{LIGHT_BLUE}Broadcast IP:{LIGHT_RED} {address.broadcast}")
                    print("     --------    ")
        net_io = psutil.net_io_counters()
        print(f"{LIGHT_BLUE}Total Bytes Sent:{LIGHT_RED} {get_size(net_io.bytes_sent)}")
        print(f"{LIGHT_BLUE}Total Bytes Received:{LIGHT_RED} {get_size(net_io.bytes_recv)}\n")

    if pcinfo_toShow_disk:
        print(f"{BLUE}=== {LIGHT_RED}DISK {BLUE}===")
        partitions = psutil.disk_partitions()
        for partition in partitions:
            print(f"{BLUE}Device:{LIGHT_RED} {partition.device}")
            print(f"  {LIGHT_BLUE}Mountpoint:{LIGHT_RED} {partition.mountpoint}")
            print(f"  {LIGHT_BLUE}File type:{LIGHT_RED} {partition.fstype}")
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                continue
            print(f"  {LIGHT_BLUE}Total Size:{LIGHT_RED} {get_size(partition_usage.total)}")
            print(f"  {LIGHT_BLUE}Used:{LIGHT_RED} {get_size(partition_usage.used)}")
            print(f"  {LIGHT_BLUE}Free:{LIGHT_RED} {get_size(partition_usage.free)}")
            print(f"  {LIGHT_BLUE}Percentage:{LIGHT_RED} {partition_usage.percent}%")
        disk_io = psutil.disk_io_counters()
        print(f"\n{LIGHT_BLUE}Total read:{LIGHT_RED} {get_size(disk_io.read_bytes)}")
        print(f"{LIGHT_BLUE}Total write:{LIGHT_RED} {get_size(disk_io.write_bytes)}\n")

    if pcinfo_toShow_cpu == False and pcinfo_toShow_gpu == False and pcinfo_toShow_ram == False and pcinfo_toShow_net == False and pcinfo_toShow_disk == False:
        print(f"{PreMessage.error} {RED}To show more info type {LIGHT_RED}[ -cpu / -gpu / -ram / -net / -disk or -all ]{RED} in command. You can type more than one!")
