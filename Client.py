import pygame
import socket
import sys

ESP_IP = "192.168.0.100"   
PORT = 1234

# Socket forbindelse
sock = socket.socket()
sock.connect((ESP_IP, PORT))

pygame.init()
screen = pygame.display.set_mode((420, 240))
pygame.display.set_caption("Rover Control")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

def send(cmd):
    try:
        sock.send(cmd.encode())
    except:
        pass

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        send("F")
    elif keys[pygame.K_s]:
        send("B")
    elif keys[pygame.K_a]:
        send("L")
    elif keys[pygame.K_d]:
        send("R")
    else:
        send("S")

    # Grafisk
    screen.fill((25, 25, 25))

    title = font.render("ROVER CONTROLS", True, (200, 200, 200))
    screen.blit(title, (120, 20))

    controls = [
        "W  - Forward",
        "S  - Backward",
        "A  - Left",
        "D  - Right",
        "",
        "Close window to stop rover"
    ]

    y = 70
    for line in controls:
        text = font.render(line, True, (180, 180, 180))
        screen.blit(text, (100, y))
        y += 30

    pygame.display.flip()
    clock.tick(30)

# Cleanup
try:
    sock.send(b"S")
    sock.close()
except:
    pass

pygame.quit()
sys.exit()
