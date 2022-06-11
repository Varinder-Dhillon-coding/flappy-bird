import pygame as pg
from pygame.locals import *
import random 

scr_size = height,width = 400,600

jump = False
gravity = 3
jump_height = 23
speed = jump_height

pg.init()

screen = pg.display.set_mode(scr_size)
pg.display.set_caption("Flappy Bird")

bg = pg.image.load("bg.png")
bg = pg.transform.scale(bg,(400,800))
bg1 = bg.get_rect()
bg1.center = 200,200

idle_flappy = pg.image.load("idle_flappy.png")
idle_flappy = pg.transform.scale(idle_flappy,(60,60))
idle_flappy1 = idle_flappy.get_rect(midleft =(20,100))

jump_flappy = pg.image.load("fly_flappy.png")
jump_flappy = pg.transform.scale(jump_flappy,(60,60))

pipe = pg.image.load("pipe.png")
pipe = pg.transform.scale(pipe,(80,400))
pipe1 = pipe.get_rect(bottomleft =(400,700))

piper = pg.image.load("pipe.png")
piper = pg.transform.scale(piper,(80,400))
piper = pg.transform.rotate(piper,180)
piper1 = piper.get_rect(bottomleft =(400,150))

font = pg.font.Font('freesansbold.ttf', 32)
text = font.render('Game Over', True, (0, 255, 200), (0, 0, 128))
text_loc = text.get_rect()
text_loc.center = 200,300

clock = pg.time.Clock()

q = False
running = True
while running:
    pipe1.x -= 2
    piper1.x -= 2
    idle_flappy1.y += gravity

    if idle_flappy1.y >= 545 :
            idle_flappy1.y = 545
    
    for event in pg.event.get() :
        if event.type == QUIT:
            running = False
            q = True

        if event.type == KEYDOWN:
            if event.key == K_UP:
                jump = True

    if jump:

        idle_flappy1.y -= speed
        speed -= gravity
        
        if idle_flappy1.y <= 0 :
            idle_flappy1.y = 0
            
        if speed <= 0 :
            jump = False
            speed = jump_height

    
    
    if pipe1.x == -70:
        ran = random.randint(0,3) 
        print(ran)
        if ran == 0:
            pipe1.x = 400
            piper1.x = 400
            pipe1.y = 520
            piper1.y = -10

        elif ran == 1:
            pipe1.x = 400
            piper1.x = 400
            pipe1.y = 200
            piper1.y = -340
            
        elif ran == 2:
            pipe1.x = 400
            piper1.x = 400
            pipe1.y = 450
            piper1.y = -90
            
        elif ran == 3:
            pipe1.x = 400
            piper1.x = 400
            pipe1.y = 300
            piper1.y = -250
            
    screen.blit(bg,bg1)
    screen.blit(idle_flappy,idle_flappy1)
    screen.blit(pipe,pipe1)
    screen.blit(piper,piper1)
    clock.tick(60)
    if idle_flappy1.colliderect(pipe1):
        running = False
        screen.blit(text,text_loc)

    elif idle_flappy1.colliderect(piper1):
        running = False
        screen.blit(text,text_loc)
    pg.display.update()
if q == True :
    pg.quit()
