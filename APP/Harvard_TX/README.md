# Harvard_TX Project

This is the main page for the Harvard_TX project. The development of this project is based on the AnySense_7688 project. However, we are sorry that we cannot release further information because most of the details are remaining confidental. We will make that public once we are authorized to do so.

## Hardware

* MediaTek LinkIt Smart 7688
* MediaTek LinkIt Smart 7688 Breakout v2.0
* TVOC sensor: Sensirion SGP30
* T/H/PM sensor: Plantower PMS5003T
* RTC: DS3231
* 0.96" LCD
* SD card

## How to re-install the codes?

Please use the designated account/password to login the system, and remove the existing project source codes:

## How to install the codes (for new LinkIt Smart 7688 boards)?

Please login you 7688 board, and change the working directory to /root. Then, please follow the following steps:

1. Use the coommand to get the latest version of the codes: 
   ```
   git clone https://github.com/winshareinc/AnySense_7688
   ```
2. update the values of GPS_LAT and GPS_LON with your GPS coordinates in the file /root/AnySense_7688/APP_Harvard_TX_config.py

3. Run the setup script:
   ```
   /root/AnySense_7688/APP/Harvard_TX/setup.sh KEY
   ```

Then, the script will install and configure everything. The system will reboot after the installation is done, and hopefully the system will start to upload data to the backend database.
