from kivy.app import App
from kivy.lang import Builder
from kivy.lib import osc
from kivy.utils import platform
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout


activityport = 3001
serviceport = 3000


def some_api_callback(self, message, *args):
    print("got a message! %s" % message)

Builder.load_string('''
<ServiceInterface>:
    BoxLayout:
        orientation: "vertical"
        Button:
            text: 'ping!'
            on_press: app.ping()
        BoxLayout:
            Button:
                text: "stop service"
                on_press: app.stop_service()
            Button:
                text: 'start service'
                on_press: app.start_service()
''')

class ServiceInterface(BoxLayout):
    pass

class ServiceApp(App):
    def build(self):
        self.start_service()

        osc.init()
        oscid = osc.listen(ipAddr='127.0.0.1', port=activityport)
        osc.bind(oscid, some_api_callback, '/some_api')
        Clock.schedule_interval(lambda *x: osc.readQueue(oscid), 0)

        return ServiceInterface()

    def start_service(self):
        if platform == 'android':
            from android import AndroidService
            service = AndroidService('my pong service', 'running')
            service.start('service started')
            self.service = service

    def ping(self):
        osc.sendMsg('/some_api', ['ping', ], port=serviceport)

    def stop_service(self):
        if self.service:
            self.service.stop()
        self.service = None

    def some_api_callback(self, message, *args):
        print("got a message! %s" % message)
        self.root.text += '\n%s' % message[2]

if __name__ == '__main__':
    ServiceApp().run()