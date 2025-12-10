import network, socket
from machine import Pin, PWM
import time

# ---------- WiFi ----------
SSID = "Leanders Hytte"
PASSWORD = "Bingbong32"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    time.sleep(0.2)

ip = wlan.ifconfig()[0]
print("ESP IP:", ip)

# ---------- Motors ----------
DIR1 = Pin(17, Pin.OUT)
DIR2 = Pin(20, Pin.OUT)
PWM1 = PWM(Pin(16), freq=1000)
PWM2 = PWM(Pin(19), freq=1000)

def drive(d1, d2, p1, p2):
    DIR1.value(d1)
    DIR2.value(d2)
    PWM1.duty_u16(min(max(p1,0),65535))
    PWM2.duty_u16(min(max(p2,0),65535))

def stop():
    PWM1.duty_u16(0)
    PWM2.duty_u16(0)

# ---------- UDP ----------
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(('', 4210))
print("🚗 UDP server ready")

while True:
    try:
        data, addr = udp.recvfrom(1024)
        msg = data.decode()
        # forventer: d1,d2,p1,p2
        parts = msg.split(",")
        d1 = int(parts[0])
        d2 = int(parts[1])
        p1 = int(parts[2])
        p2 = int(parts[3])
        drive(d1,d2,p1,p2)
    except:
        stop()


