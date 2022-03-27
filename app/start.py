#its a new version

from machine import ADC, Pin
import time, utime
import machine
import urequests

import network

import ujson

file = open('config.json')
config_datas = ujson.load(file)
import app.secrets as secrets

uId = config_datas['sensors']['id']
url = secrets.URL
adc = ADC(Pin(39))
adc.atten(ADC.ATTN_11DB)
imp = Pin(26, Pin.OUT)
imp.off()
rev = Pin(4, Pin.OUT)
rev.off()


def average(data_list):
    try:
        for i in range(len(data_list) - 1):
            for j in range(len(data_list) - i - 1):
                if data_list[j] > data_list[j + 1]:
                    data_list[j], data_list[j + 1] = data_list[j + 1], data_list[j]

        result = []
        med = len(data_list) // 2
        zero_delta = abs(data_list[med] - data_list[med + 1])
        for i in range(med, len(data_list) - 1):
            if data_list[i + 1] - data_list[i] <= zero_delta:
                result.append(data_list[i])

        for i in range(1, med):
            if data_list[i] - data_list[i - 1] <= zero_delta:
                result.append(data_list[i])
        if sum(result) != 0:
            avg_result = sum(result) / len(result)
        else:
            avg_result = 0
        print('average result is ', avg_result)
        return avg_result
    except:
        return data_list[0]


def sendData(data):
    response_data = urequests.post(url, json={"value": data, "sensor": uId})
    if response_data.status_code != 201:
        print(response_data.status_code)
        machine.reset()


def measure(adc, imp, rev):
    dataList = []

    imp.on()
    time.sleep(0.1)
    for _ in range(50):
        dataList.append(adc.read_u16())
        time.sleep(0.1)

    val = average(dataList)
    imp.off()
    time.sleep(0.5)
    reverse(rev)
    print('measure result is ', val)
    return round(val, 0)


def reverse(rev):
    rev.on()
    time.sleep(0.2)
    rev.off()
    time.sleep(0.5)


def connect():
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(config_datas['wifi']['ssid'], config_datas['wifi']['password'])
    while not sta_if.isconnected():
        pass
    print('OK - network config:', sta_if.ifconfig())


def main():
    print('main start')
    print('main while True')
    while True:
        try:
            # print('main try connect')
            # connect()
            print('main for i in range 100')
            for i in range(5):
                print('main measure ', i)
                data = measure(adc, imp, rev)
                print('main measure OK', i)
                print('main send data ', i, data)
                sendData(data)
                print('data send complete ', i)
                time.sleep(5)
                gc.collect()
            machine.reset()

        except:
            print('main error')
            time.sleep(1)
            machine.reset()


main()
