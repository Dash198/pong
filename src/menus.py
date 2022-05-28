import pygame, sys, time
from pygame.locals import *
import pong
pygame.init()

SCREEN_WIDTH=720
SCREEN_HEIGHT=480

clock=pygame.time.Clock()

surf=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

smallfont=pygame.font.Font("pong/assets/pfont.ttf",50)

class Buttons():
    def __init__(self,mesg,xco,yco,wi,he,inc,aco):
        self.x=xco
        self.msg=mesg
        self.y=yco
        self.h=he
        self.w=wi
        self.ic=inc
        self.ac=aco
        self.clicked=False
        pass

    def update(self):
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        if self.x+self.w>mouse[0]>self.x and self.y+self.h>mouse[1]>self.y:
            pygame.draw.rect(surf,self.ac,(self.x,self.y,self.w,self.h))
            surf.blit((smallfont.render(self.msg,True,self.ic)),(self.x+20,self.y+10))
            if click[0]==1:
                self.clicked=True
        else:
            pygame.draw.rect(surf,self.ic,(self.x,self.y,self.w,self.h))
            surf.blit((smallfont.render(self.msg,True,self.ac)),(self.x+20,self.y+10))

class MainMenu():
    def __init__(self) -> None:
        start=Buttons("Start",250,170,150,70,(0,0,0),(255,255,255))
        quit=Buttons("Quit",250,250,150,70,(0,0,0),(255,255,255))
        self.buttons=[start,quit]
        self.isEnabled=True
    
    def update(self):
        surf.fill((0,0,0))
        surf.blit((pygame.font.Font("pong/assets/pfont.ttf",100).render("PONG",True,(255,255,255))),(250,50))
        for button in self.buttons:
            button.update()
            if button.clicked:
                button.clicked=False
                if button.msg=="Start":
                    pong.start()
                    self.isEnabled=False
                elif button.msg=="Quit":
                    pygame.quit()
                    sys.exit()

class PauseMenu():
    def __init__(self) -> None:
        resume=Buttons("Pause",250,170,150,70,(0,0,0),(255,255,255))
        quit=Buttons("Quit",250,250,150,70,(0,0,0),(255,255,255))
        self.buttons=[resume,quit]
        self.isEnabled=True
    
    def render(self):
        surf.fill((0,0,0))
        surf.blit((pygame.font.Font("pong/assets/pfont.ttf",100).render("Game Paused",True,(255,255,255))),(250,50))
        for button in self.buttons:
            button.update()
            if button.clicked:
                button.clicked=False
                if button.msg=="Resume":
                    self.isEnabled=False
                elif button.msg=="Quit":
                    main.isEnabled=True
                    self.isEnabled=False
                    pong.kill_game()
                    pass


main=MainMenu()

def start():
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

        surf.fill((0,0,0))

        if main.isEnabled:
            main.update()
        
        pygame.display.update()
        clock.tick(60)