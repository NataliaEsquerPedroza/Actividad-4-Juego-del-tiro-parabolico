"""
1) Aumentar la velocidad del proyectil y de los balones.
2) Hacer que el juego nunca termine: los balones que salen de ventana
   se reposicionan a la derecha con nueva altura.
"""

from random import randrange
from turtle import *
from freegames import vector

TARGET_SPEED = 2.0     
GRAVITY = 0.35         
SHOT_SPEED_DIV = 18.0  
SPAWN_CHANCE = 40       
TICK_MS = 40            
TARGET_Y_RANGE = (-150, 150)
BORDER = 200           

ball = vector(-200, -200)  
speed = vector(0, 0)       
targets = []              

def tap(x, y):
    """Lanza el proyectil con mayor velocidad inicial."""
    if not inside(ball):
        ball.x = -199
        ball.y = -199
        # Más rápido: reducimos el divisor para aumentar la magnitud
        speed.x = (x + 200) / SHOT_SPEED_DIV
        speed.y = (y + 200) / SHOT_SPEED_DIV

def inside(xy):
    """Regresa True si xy está dentro de la ventana."""
    return -BORDER < xy.x < BORDER and -BORDER < xy.y < BORDER

def draw():
    """Dibuja proyectil y balones."""
    clear()

    # Targets (azules)
    for target in targets:
        goto(target.x, target.y)
        dot(20, 'blue')

    # Proyectil (rojo)
    if inside(ball):
        goto(ball.x, ball.y)
        dot(6, 'red')

    update()

def move():
    """Actualiza posiciones del proyectil y de los balones."""
    # Posible aparición de nuevo balón
    if randrange(SPAWN_CHANCE) == 0:
        y = randrange(*TARGET_Y_RANGE)
        target = vector(BORDER, y)
        targets.append(target)

    # Mover balones a la izquierda, más rápido
    for target in targets:
        target.x -= TARGET_SPEED

        # Si sale por la izquierda, reposicionar a la derecha (juego infinito)
        if target.x < -BORDER - 10: 
            target.x = BORDER
            target.y = randrange(*TARGET_Y_RANGE)

    if inside(ball):
        speed.y -= GRAVITY
        ball.move(speed)

    # Colisiones: elimina targets golpeados
    vivos = []
    for target in targets:
        if abs(target - ball) > 13:
            vivos.append(target)
    targets[:] = vivos

    draw()

    ontimer(move, TICK_MS)

setup(420, 420, 370, 0)
hideturtle()
up()
tracer(False)
onscreenclick(tap)
move()
done()
