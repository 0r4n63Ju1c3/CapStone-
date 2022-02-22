import psutil as ps
import time
from datetime import datetime as dt

algo_name = "Ascon Hash and Encryption"

def get_cpu_usage_pct():
    return ps.cpu_percent(interval=0.5)

def get_ram_usage():
    return int(ps.virtual_memory().total - ps.virtual_memory().available)

def get_ram_usage_pct():
    return ps.virtual_memory().percent

def main():
    print('Testing {} algorithm\n'.format(algo_name))
    start_time = time.time()
    while True:
        print(dt.now(),",", get_cpu_usage_pct(), ",", int(get_ram_usage() / 1024 / 1024), ",",get_ram_usage_pct())
        #print('Current Time: {} '.format(dt.now()))
        #print('CPU usage is {} %'.format(get_cpu_usage_pct()))
        #print('RAM usage is {} MB'.format(int(get_ram_usage() / 1024 / 1024)))
        #print('RAM usage is {} %'.format(get_ram_usage_pct()))
if __name__ == "__main__":
    main()