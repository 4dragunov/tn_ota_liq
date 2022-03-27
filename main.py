import ujson
from app.ota_updater import OTAUpdater
from machine import Pin
from time import sleep


def connectToWifiAndUpdate():
    f = open('config.json')
    config_data = ujson.load(f)
    import time, machine, network, gc, app.secrets as secrets
    time.sleep(1)
    print('Memory free', gc.mem_free())

    from app.ota_updater import OTAUpdater

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(config_data['wifi']['ssid'], config_data['wifi']['password'])

        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    otaUpdater = OTAUpdater('https://github.com/4dragunov/tn_ota_liq_MSCW', main_dir='app')
    hasUpdated = otaUpdater.install_update_if_available()

    if hasUpdated:
        machine.reset()
    else:
        del (otaUpdater)


def startApp():
    import app.start


connectToWifiAndUpdate()
startApp()



