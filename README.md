This is the AnySense project for MediaTek LinkIt 7688 board. The project conducts sensing tasks and reports the results to the LASS backend database via either MQTT or Restful API. The project are based on MRAA library in Python, and hopefully it shall run smoothly on the other MRAA-supported platforms.

## Sensors supported (till 2018/1/7)
* Temperature and Humidity Sensor
  * HTU21d (I2C)
  * SHT2x (I2C)
* Light Sensor
  * BH1750FVI (I2C)
  * TCS34725 (I2C)
* Particulate Matter Sensor
  * Plantower PMS3003 (UART0)
  * Plantower PMS5003 (UART0)
  * Plantower PMS5003T (UART0)
  * Plantower PMS7003 (UART0)
  * Plantower PMSA003 (UART0)
* Gas Sensor
  * SenseAir S8 (UART1)
  * Sensirion SGP30 (I2C)
* RTC: real time clock
  * DS3231 (I2C)

## How to run this program?
Please login you development board, and change to your working directory. Then, please follow the following steps:

1. Use the coommand to get the latest version of the codes:
   ```
   git clone https://github.com/winshareinc/AnySense_7688
   ```

2. Edit the file AnySense_config.py and change the configureations
   * GPS coordinates: including GPS_LAT and GPS_LON
   * Push Body settings: including APP_ID, Version and DEVICE_PREFIX
   * MQTT settings: including MQTT_broker, MQTT_port and MQTT_topic

  
3. Run the main program by
   ```
   /root/AnySense_7688/APP/Temp_Project/setup.sh
   ```

4. You can check the results on the console printouts or on the MQTT broker.

## Applications

The existing applications (so far) are listed on the [wiki](https://github.com/winshareinc/AnySense_7688/wiki) page

## Acknowledgement

The project was inspired by Spark Lee's Linkit7688_PM2.5 project (https://github.com/future/Linkit7688_PM2.5). We also thank Ming-Wei Cheng (a.k.a. A-Hai) for his technical advices and anonymous users for their valueable feedbacks.
