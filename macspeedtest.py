import rumps
import speedtest as st
from AppKit import NSAttributedString
from PyObjCTools.Conversion import propertyListFromPythonCollection
from Cocoa import (NSFont, NSFontAttributeName,
                   NSColor, NSForegroundColorAttributeName)

font = NSFont.fontWithName_size_("Monaco", 11.0)
red = NSColor.redColor()
yellow = NSColor.yellowColor()
green = NSColor.greenColor()

class SpeedTestApp(object):
    def __init__(self):
        self.config = {
            "app_name": "SpeedTest",
            "start": "Check Speed",
            "interval": 1500
        }
        self.app = rumps.App(self.config["app_name"])
        self.timer = rumps.Timer(self.on_tick, 60)
        self.interval = self.config["interval"]
        self.set_up_menu()
        self.update_button = rumps.MenuItem(
            title=self.config["start"], callback=self.check_speed)
        self.app.menu = [self.update_button]

    def set_up_menu(self):
        self.timer.stop()
        self.timer.count = 0
        self.app.title = "🖲"

    def on_tick(self, sender):
        speed_test = st.Speedtest()
        speed_test.get_best_server()
        download = speed_test.download()
        upload = speed_test.upload()
        ping = speed_test.results.ping
        download_mbs = round(download / (10**6), 2)
        upload_mbs = round(upload / (10**6), 2)
        self.app.title = f"⇩{download_mbs} ⇧{upload_mbs} ⟳{ping}"

    def check_speed(self, sender):
        if sender.title.lower().startswith(("check")):
            if sender.title == self.config["start"]:
                self.timer.count = 0
                self.timer.end = self.interval
            self.timer.start()

    def run(self):
        self.app.run()


if __name__ == '__main__':
    app = SpeedTestApp()
    app.run()

