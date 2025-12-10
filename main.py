from machine import Pin, PWM
import network
import socket
import time

# MOTOR SETUP
DIR1 = Pin(17, Pin.OUT)
PWM1 = PWM(Pin(16), freq=1000)

DIR2 = Pin(20, Pin.OUT)
PWM2 = PWM(Pin(19), freq=1000)

# STOP MOTORS ON BOOT
PWM1.duty(0)
PWM2.duty(0)
DIR1.off()
DIR2.off()

# MOTOR SETTINGS
SPEED = 600
M2_OFFSET = 80

def stop():
    PWM1.duty(0)
    PWM2.duty(0)

def forward():
    DIR1.on()
    DIR2.on()
    PWM1.duty(SPEED)
    PWM2.duty(min(1023, SPEED + M2_OFFSET))

def backward():
    DIR1.off()
    DIR2.off()
    PWM1.duty(SPEED)
    PWM2.duty(min(1023, SPEED + M2_OFFSET))

def left():
    DIR1.off()
    DIR2.on()
    PWM1.duty(SPEED)
    PWM2.duty(SPEED)

def right():
    DIR1.on()
    DIR2.off()
    PWM1.duty(SPEED)
    PWM2.duty(SPEED)

# WIFI
SSID = "x"
PASSWORD = "x"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connecting to WiFi...")
while not wlan.isconnected():
    time.sleep(0.5)

ip = wlan.ifconfig()[0]
print("Connected, IP:", ip)

# TCP SERVER
PORT = 1234
addr = socket.getaddrinfo("0.0.0.0", PORT)[0][-1]

server = socket.socket()
server.bind(addr)
server.listen(1)

print("Waiting for client...")
conn, addr = server.accept()
print("Client connected:", addr)

# MAIN LOOP
try:
    while True:
        data = conn.recv(1)
        if not data:
            break

        cmd = data.decode()

        if cmd == "F":
            forward()
        elif cmd == "B":
            backward()
        elif cmd == "L":
            left()
        elif cmd == "R":
            right()
        elif cmd == "S":
            stop()

except Exception as e:
    print("Error:", e)

finally:
    stop()
    conn.close()
    server.close()

