###############################################################################
# setup.sh
# Author: C1C Lauren Humpherys
# Purpose: Turn fresh raspbian image into gold image usable within IOT Capstone
# - Pull latest code from GitHub
# - Write cron jobs to run eInk updater, update bluetooth ID and location data, update weather data, watchdog scropt fo C2 server, and software update
# - Automate language, timezone, location and network setup for raspi-config
################################################################################
#!/bin/bash

# Run git pull
echo "Running git pull"
/bin/bash /home/pi/Desktop/IOT_Capstone/Code/iot_capstone22/gitPull.sh
echo "Git pull successful!"

# Initialize cron jobs
echo "Initializing cron jobs"

sudo echo '@reboot python3 /home/pi/Desktop/IOT_Capstone/Code/iot_capstone22/eInk/eInk_Updater.py' >> /etc/crontab

sudo echo '@reboot python3 /home/pi/Desktop/IOT_Capstone/Code/iot_capstone22/BlueTooth/uploadBTData.py' >> /etc/crontab

sudo echo '@reboot python3 /home/pi/Desktop/IOT_Capstone/Code/iot_capstone22/Weather/uploadWeatherData.py' >> /etc/crontab

sudo echo '*/5 * * * * python3 /home/pi/Desktop/IOT_Capstone/Watchdog/Watchdog.py' >> /etc/crontab

sudo echo '0 1 * * * /home/pi/Desktop/IOT_Capstone/Code/iot_capstone22/update.sh' >> /etc/crontab

echo "Cron job initializatio complete!"

# Automated Raspberry Pi configuration
echo "Now running through raspi-config"

/bin/bash /home/pi/Desktop/IOT_Capstone/Code/iot_capstone22/raspiconfig.sh

echo "Rasi-config complete!"

# Initialize C2 server backend
echo "Initializing C2 server backend"

#TODO: Initialize C2 server

echo "C2 server backend initialized!"
echo "Initialization script complete!"



