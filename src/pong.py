from os import kill
import pygame, sys, random, time
from pygame.locals import *

pygame.init()

SCREEN_WIDTH=720
SCREEN_HEIGHT=480

running=True

FPS=60
FramePerSec=pygame.time.Clock()

displaysurf=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

bg=pygame.image.load("pong/assets/bg.png")

class PlayerPaddle(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.surf=pygame.Surface((10,75))
        self.surf.fill((255,255,255))
        self.rect=self.surf.get_rect(center=(SCREEN_WIDTH-5,SCREEN_HEIGHT/2))
        self.score=0

    def update(self):
        pressed_keys=pygame.key.get_pressed()
        if self.rect.top>10:  
            if pressed_keys[K_UP]:
                self.rect.move_ip(0,-5)
        if self.rect.bottom<SCREEN_HEIGHT-10:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0,5)

class EnemyPaddle(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.surf=pygame.Surface((10,75))
        self.surf.fill((255,255,255))
        self.rect=self.surf.get_rect(center=(5,SCREEN_HEIGHT/2))
        self.score=0
        self.move_up=False
        self.move_down=False

    def update(self):
        if B1.rect.centery>self.rect.centery:
            if self.rect.bottom<SCREEN_HEIGHT-10:
                self.rect.move_ip(0,5)
                self.move_down=True
                self.move_up=False
        if B1.rect.centery<self.rect.centery:
            if self.rect.top>10:
                self.rect.move_ip(0,-5)
                self.move_up=True
                self.move_down=False

class Ball(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.surf=pygame.Surface((10,10))
        self.surf.fill((255,255,255))
        self.rect=self.surf.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
        self.mx=random.choice([5,-5])
        self.my=0

    def update(self):
        self.rect.move_ip(self.mx,self.my)
        ukey=pygame.key.get_pressed()
        if (self.rect.right>=SCREEN_WIDTH or self.rect.left<=0) and (not (pygame.sprite.spritecollideany(B1,Paddles))):
            if self.rect.right>=SCREEN_WIDTH:
                E1.score+=1
            if self.rect.left<=0:
                P1.score+=1
            time.sleep(0.5)
            self.rect.center=((SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
            self.mx=random.choice([5,-5])
        
        if self.rect.top<=10 or self.rect.bottom>=SCREEN_HEIGHT-10:
            self.my*=-1
        
        if pygame.sprite.spritecollideany(B1,Paddles):
            col=pygame.mixer.Sound('pong/assets/pong.wav')
            col.play()
            self.mx*=-1
            if self.rect.colliderect(P1.rect):
                if ukey[K_UP]:
                    if self.my==0:
                        B1.my-=5
                    else:
                        if B1.my>0:
                            B1.my*=-1
                if ukey[K_DOWN]:
                    if B1.my==0:
                        B1.my+=5
                    else:
                        if B1.my<0:
                            B1.my*=-1
                        pass
            
            if self.rect.colliderect(E1.rect):
                if E1.move_up:
                    if B1.my==0:
                        B1.my-=5
                if E1.move_down:
                    if B1.my==0:
                        B1.my-=5
                
P1=PlayerPaddle()
E1=EnemyPaddle()
B1=Ball()

Paddles=pygame.sprite.Group()
Paddles.add(P1)
Paddles.add(E1)

all_sprites=pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(B1)

SFont=pygame.font.Font("pong/assets/pfont.ttf", 40)
GOver=pygame.font.SysFont("pong/assets/pfont.ttf", 50)

cd=['3','2','1','START!']
cc=0

def start():
   # main_menu.disable()
    global running
    while running:
        while True:
            global cc
            if cc>=4:
                break
            displaysurf.blit(bg,(0,0))
            pygame.draw.rect(displaysurf,(255,255,255),(280,150,170,190))
            if cc<3:
                cf=pygame.font.Font("pong/assets/pfont.ttf",150).render(cd[cc],True,(0,0,0))
                displaysurf.blit(cf,(335,180))
                se=pygame.mixer.Sound('pong/assets/beep.wav')
            else:
                displaysurf.blit((pygame.font.Font('pong/assets/pfont.ttf',60).render(cd[cc],True,(0,0,0))),(295,210))
                se=pygame.mixer.Sound('pong/assets/start.wav')
            se.play()
            pygame.display.update()
            cc+=1
            time.sleep(0.5)

        for event in pygame.event.get():
            if event.type==QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                pressed=pygame.key.get_pressed()
                if pressed[K_ESCAPE]:
                    from menus import PauseMenu
                    pm=PauseMenu()
                    while pm.isEnabled:
                        pm.render()
                    pm.isEnabled=True
                    pass


        pscore=SFont.render(str(P1.score),True, (255,255,255))
        escore=SFont.render(str(E1.score),True,(255,255,255))

        displaysurf.blit(bg,(0,0))

        for entity in all_sprites:
            entity.update()
            displaysurf.blit(entity.surf,entity.rect)

        displaysurf.blit(escore,(int(290*SCREEN_WIDTH/640),30))
        displaysurf.blit(pscore,(int(330*SCREEN_WIDTH/640),30))

        if P1.score==7 or E1.score==7:
            if P1.score==7:
                win=GOver.render("You Win!",True,(255,255,255))
                displaysurf.fill((0,0,0))
                displaysurf.blit(win,(int(240*SCREEN_WIDTH/640),200))
            if E1.score==7:
                lose=GOver.render("You Lose!",True,(255,255,255))
                displaysurf.fill((0,0,0))
                displaysurf.blit(lose,(int(230*SCREEN_WIDTH/640),200))
            pygame.display.update()
            running=False
            time.sleep(1)
            break

        pygame.display.update()
        FramePerSec.tick(FPS)

    if running==False:
        kill_game()

def kill_game():
        for entity in all_sprites:
            entity.kill()
        pygame.quit()
