#import mraa
import time
import string
import os
import subprocess
import paho.mqtt.publish as publish
from datetime import datetime

import Temp_Project_config as Conf

fields = Conf.fields
values = Conf.values

def upload_data():
    # CSV_items = ['device_id','date','time','s_t0','s_h0','s_d0','s_d1','s_d2','s_lr','s_lg','s_lb','s_lc', 's_l0', 's_g8','s_gg']
    pairs = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S").split(" ")
    values["device_id"] = Conf.DEVICE_ID
    values["ver_app"] = Conf.Version
    values["date"] = pairs[0]
    values["time"] = pairs[1]

    # values["tick"] = 0
    # try:
    #     with open('/proc/uptime', 'r') as f:
    #         values["tick"] = float(f.readline().split()[0])
    # except:
    #     print "Error: reading /proc/uptime"

    msg = ""
    for item in values:
        if Conf.num_re_pattern.match(str(values[item])):
            msg = msg + "|" + item + "=" + str(values[item]) + ""
        else:
            tq = values[item]
            tq = tq.replace('"','')
            msg = msg + "|" + item + "=" + tq

    # restful_str = "wget -O /tmp/last_upload.log \"" + Conf.Restful_URL + "topic=" + Conf.APP_ID + "&device_id=" + Conf.DEVICE_ID + "&key=" + Conf.SecureKey + "&msg=" + msg + "\""
    # os.system(restful_str)

    #publish
    push_items = ["ver_format","FAKE_GPS","app","ver_app","device_id","date","time","s_d0","s_d1","s_t0","s_h0","gps_lon","gps_lat"]
    msg = ""
    for item in push_items:
        if item in values:
            if Conf.num_re_pattern.match(str(values[item])):
                msg = msg + "|" + item + "=" + str(values[item]) + ""
            else:
                tq = values[item]
                tq = tq.replace('"','')
                msg = msg + "|" + item + "=" + tq
    publish.single(Conf.MQTT_topic, msg, hostname=Conf.MQTT_broker, port = Conf.MQTT_port)
    print "---###"
    print msg
    print "###"
    print values
    print "###---"
    # msg = ""
    # for item in CSV_items:
    #     if item in values:
    #         msg = msg + str(values[item]) + '\t'
    #     else:
    #         msg = msg + "N/A" + '\t'



    #
    # try:
    #     with open(Conf.FS_SD + "/" + values["date"] + ".txt", "a") as f:
    #         f.write(msg + "\n")
    # except:
    #     print "Error: writing to SD"

def display_data(disp):
    global connection_flag
    pairs = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S").split(" ")
    disp.setCursor(0,0)
    disp.write('{:16}'.format("ID: " + Conf.DEVICE_ID))
    disp.setCursor(1,0)
    disp.write('{:16}'.format("Date: " + pairs[0]))
    disp.setCursor(2,0)
    disp.write('{:16}'.format("Time: " + pairs[1]))

    #original display
    #
    #disp.setCursor(3,0)
    #disp.write('{:16}'.format('Temp: %.2fF' % ((values["s_t0"]*1.8)+32)))
    #disp.setCursor(4,0)
    #disp.write('{:16}'.format('  RH: %.2f%%' % values["s_h0"]))
    #

    #change Temperature and Humidity display to > [T: 23C / RH: 75%]
    disp.setCursor(3,0)
    disp.write('{:16}'.format('T: %dC / RH: %d%%' % (values["s_t0"],values["s_h0"])))
    #

    #PM2.5 display [PM2.5: 13ug/m3]
    disp.setCursor(4,0)
    disp.write('{:16}'.format('PM2.5: %dug/m3' % values["s_d0"]))


    #add CO2 display
    disp.setCursor(5,0)
    disp.write('{:16}'.format('CO2: %dppm' % values["s_g8"]))
    #

    #change Light to TVOC display
    #disp.setCursor(5,0)
    #disp.write('{:16}'.format('Light: %dLux' % values["s_l0"]))
    if(values["s_gg"] == 65535):
        disp.setCursor(6,0)
        temp = '{:16}'.format('                ')
        disp.write(temp)

    else:
        disp.setCursor(6,0)
        temp = '{:16}'.format('TVOC: %dppb' % values["s_gg"])
        disp.write(temp)
    #

    disp.setCursor(7,0)
    temp = '{:16}'.format(Conf.DEVICE_IP)
    disp.write(temp)

    disp.setCursor(7,15)
    temp = connection_flag
    disp.write(temp)

def reboot_system():
    process = subprocess.Popen(['uptime'], stdout = subprocess.PIPE)
    k = process.communicate()[0]

    items = k.split(",")
    k = items[-3]
    items = k.split(" ")
    k = float(items[-1])

    if k>1.5:
        os.system("echo b > /proc/sysrq-trigger")

def check_connection():
    global connection_flag
    if(os.system('ping www.google.com -q -c 1  > /dev/null')):
        connection_flag = "X"
    else:
        connection_flag = "@"

if __name__ == '__main__':
    if Conf.Sense_PM==1:
        pm_data = '1'
        pm = Conf.pm_sensor.sensor(Conf.pm_q)
        pm.start()
    if Conf.Sense_Tmp==1:
        tmp_data = '2'
        tmp = Conf.tmp_sensor.sensor(Conf.tmp_q)
        tmp.start()
        tmp_data = {'Tmp':0.0, 'RH':0}
    if Conf.Sense_Light==1:
        light_data = '3'
        light = Conf.light_sensor.sensor(Conf.light_q)
        light.start()
    if Conf.Sense_Gas==1:
        gas_data = '4'
        gas = Conf.gas_sensor.sensor(Conf.gas_q)
        gas.start()
    #add for TVOC
    if Conf.Sense_TVOC==1:
        TVOC_data = '5'
        TVOC = Conf.TVOC_sensor.sensor(Conf.tvoc_q)
        TVOC.start()

    disp = Conf.upmLCD.SSD1306(0, 0x3C)
    disp.clear()

    count = 0

    values["s_d0"] = 0
    values["s_d1"] = 0

    values["s_t0"] = 0
    values["s_h0"] = 0
    values["s_lr"] = -1
    values["s_lg"] = -1
    values["s_lb"] = -1
    values["s_lc"] = -1
    values["s_l0"] = -1
    values["s_g8"] = 0
    values["s_gg"] = 0
    while True:
        reboot_system()
        check_connection()

        if Conf.Sense_PM==1 and not Conf.pm_q.empty():
            while not Conf.pm_q.empty():
                pm_data = Conf.pm_q.get()
            for item in pm_data:
                if item in fields:
                    values[fields[item]] = pm_data[item]
                    if Conf.float_re_pattern.match(str(values[fields[item]])):
                        values[fields[item]] = round(float(values[fields[item]]),2)
                else:
                    values[item] = pm_data[item]
        if Conf.Sense_Tmp==1 and not Conf.tmp_q.empty():
            while not Conf.tmp_q.empty():
                tmp_data = Conf.tmp_q.get()
                        for item in tmp_data:
                                if item in fields:
                                        values[fields[item]] = tmp_data[item]
                    if Conf.float_re_pattern.match(str(values[fields[item]])):
                        values[fields[item]] = round(float(values[fields[item]]),2)
                                else:
                                        values[item] = tmp_data[item]
        if Conf.Sense_Light==1 and not Conf.light_q.empty():
            while not Conf.light_q.empty():
                light_data = Conf.light_q.get()
                        for item in light_data:
                                if item in fields:
                                        values[fields[item]] = light_data[item]
                    if Conf.float_re_pattern.match(str(values[fields[item]])):
                        values[fields[item]] = round(float(values[fields[item]]),2)
                                else:
                                        values[item] = light_data[item]
        if Conf.Sense_Gas==1 and not Conf.gas_q.empty():
            while not Conf.gas_q.empty():
                gas_data = Conf.gas_q.get()
                        for item in gas_data:
                                if item in fields:
                                        values[fields[item]] = gas_data[item]
                    if Conf.float_re_pattern.match(str(values[fields[item]])):
                        values[fields[item]] = round(float(values[fields[item]]),2)
                                else:
                                        values[item] = gas_data[item]

        if Conf.Sense_TVOC==1 and not Conf.tvoc_q.empty():
            while not Conf.tvoc_q.empty():
                TVOC_data = Conf.tvoc_q.get()
                        for item in TVOC_data:
                                if item in fields:
                                        values[fields[item]] = TVOC_data[item]
                    if Conf.float_re_pattern.match(str(values[fields[item]])):
                        values[fields[item]] = round(float(values[fields[item]]),2)
                                else:
                                        values[item] = TVOC_data[item]
        display_data(disp)
        if count == 0:
            upload_data()

        count = count + 1
        count = count % (Conf.Restful_interval / Conf.Interval_LCD)
        time.sleep(Conf.Interval_LCD)
