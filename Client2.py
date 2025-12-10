import pygame, socket, math

ESP_IP = "192.168.0.100"
PORT = 4210

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("ESP32 Rover Controller")

CENTER = (250,250)
RADIUS = 200
STICK_RADIUS = 25
MAX_PWM = 60000
MIN_PWM = 20000

DEADZONE_X = 0.1
DEADZONE_Y = 0.05

stick_pos = CENTER
dragging = False
clock = pygame.time.Clock()

# Font til tekst
font = pygame.font.SysFont("Arial", 20)

def motor(v):
    if abs(v) < DEADZONE_Y:
        return 1,0
    direction = 1 if v>0 else 0
    pwm = int(MIN_PWM + abs(v)*(MAX_PWM-MIN_PWM))
    return direction,pwm

running = True
while running:
    screen.fill((245, 245, 220))  # beige baggrund

    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            running=False
        elif e.type==pygame.MOUSEBUTTONDOWN:
            dragging=True
        elif e.type==pygame.MOUSEBUTTONUP:
            dragging=False
            stick_pos=CENTER

    x = y = 0.0
    if dragging:
        mx,my = pygame.mouse.get_pos()
        dx = mx - CENTER[0]
        dy = my - CENTER[1]
        dist = math.hypot(dx,dy)
        if dist>RADIUS:
            dx,dy = dx/dist*RADIUS, dy/dist*RADIUS
        stick_pos = (CENTER[0]+dx, CENTER[1]+dy)
        x = dx / RADIUS
        y = -dy / RADIUS

        if abs(x) < DEADZONE_X:
            x = 0

    # Blød drejning og invert X
    left  = max(min(y - x*0.5, 1), -1)
    right = max(min(y + x*0.5, 1), -1)
    d1, p1 = motor(left)
    d2, p2 = motor(right)

    # M2 kompensation
    M2_SCALE = 1.05
    p2 = int(p2 * M2_SCALE)
    if p2 > 65535:
        p2 = 65535

    msg = f"{d1},{d2},{p1},{p2}"
    sock.sendto(msg.encode(), (ESP_IP, PORT))

    # DRAW joystick base og stick
    pygame.draw.circle(screen, (200, 200, 200), CENTER, RADIUS)   # base
    pygame.draw.circle(screen, (0,0,0), stick_pos, STICK_RADIUS)  # sort stick
    pygame.draw.circle(screen, (100,100,100), CENTER, 5)          # midtpunkt

    # Y-Throttle 
    y_percent = int(y * 100)  # -100% til 100%
    throttle_text = font.render(f"Y-Throttle: {y_percent}%", True, (0,0,0))
    screen.blit(throttle_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)
