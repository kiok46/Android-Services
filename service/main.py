from time import sleep
from kivy.lib import osc

serviceport = 3001
activityport = 3002

# str(asctime(localtime()))
def service_callback(message, *args):
    #print("got a message! %s" % message)
    osc.sendMsg('/some_api', [str(message[2])], port=activityport)


if __name__ == '__main__':
    osc.init()
    oscid = osc.listen(ipAddr='127.0.0.1', port=serviceport)
    osc.sendMsg('/some_api', ['Init'], port=activityport)
    try:
        osc.bind(oscid, service_callback, '/some_api')

        while True:
            osc.readQueue(oscid)
            sleep(.3)
    except:
        osc.sendMsg('/some_api', ['error'], port=activityport)