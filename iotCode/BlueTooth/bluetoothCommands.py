import os

os.popen('sudo bluetoothctl')
os.popen('agent on')
os.popen('default-agent')
os.popen('scan on')