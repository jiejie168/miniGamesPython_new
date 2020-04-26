__author__ = 'Jie'
import pygame
import os
import time
import random
pygame.init()

WIDTH,HEIGHT=750,750  # Capital indicates Constant.
WIN=pygame.display.set_mode((WIDTH,HEIGHT)) # create a display surface.
pygame.display.set_caption("Space Shooter Tutorial")

# load images for the following utilize
RED_SPACE_SHIP=pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
GREEN_SPACE_SHIP=pygame.image.load(os.path.join("assets","pixel_ship_green_small.png"))
BLUE_SPACE_SHIP=pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png"))


# Play ship
YELLOW_SPACE_SHIP=pygame.image.load(os.path.join("assets","pixel_ship_yellow.png"))

#Lasers
RED_LASER=pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
GREEN_LASER=pygame.image.load(os.path.join("assets","pixel_laser_green.png"))
BLUE_LASER=pygame.image.load(os.path.join("assets","pixel_laser_blue.png"))
YELLOW_LASER=pygame.image.load(os.path.join("assets","pixel_laser_yellow.png"))

#Background
BG=pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")),(WIDTH,HEIGHT))

class Laser:
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.img=img
        self.mask=pygame.mask.from_surface(self.img)

    def draw(self,window):
        window.blit(self.img,(self.x,self.y))
    def move(self,vel):
        self.y+=vel
    def off_screen(self,height):
        return not (self.y<=height and self.y>=0)
    def collision(self,obj):
        return collide(obj,self)



class Ship:
    # this is a parent class for the following use
    COOLDOWN=30  # class parameter for cooldown time, half second.
    def __init__(self,x,y,health=100):
        self.x=x
        self.y=y
        self.health=health
        self.ship_img=None
        self.laser_img=None
        self.lasers=[]
        self.cool_down_counter=0

    def draw(self,window):
        # pygame.draw.rect(window,(255,0,0),(self.x,self.y,50,50)) # 50 is the size of object
        window.blit(self.ship_img,(self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self,vel,obj):
        self.cooldown()  # to check if we can start to shoot
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                # to check if laser is inside the screen
                self.lasers.remove(laser)
            elif laser.collision(obj):
                # check if the laser collide with obj, and then drop some health.
                obj.health-=10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter>=self.COOLDOWN:
            self.cool_down_counter=0
        elif self.cool_down_counter>0:
            self.cool_down_counter+=1

    def shoot(self):
        # make sure we do not shoot too fast
        if self.cool_down_counter==0:
            laser=Laser(self.x,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter+=1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)
        self.ship_img=YELLOW_SPACE_SHIP
        self.laser_img=YELLOW_LASER
        self.mask=pygame.mask.from_surface(self.ship_img)  # the mask is used for the image boundary during collision
        self.max_health=health

    def move_lasers(self,vel,objs):
        # check if the enemies objects are hit by the laser.
        self.cooldown()  # to check if we can start to shoot
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                # to check if laser is inside the screen
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj) #once hit, remove (for enemy)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    def draw(self,window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self,window):
        pygame.draw.rect(window,(255,0,0),(self.x,self.y+self.ship_img.get_height()+10,self.ship_img.get_width(),10))
        ratio=self.health/self.max_health
        pygame.draw.rect(window,(0,255,0),(self.x,self.y+self.ship_img.get_height()+10,self.ship_img.get_width()*ratio,10))

        
class Enemy(Ship):
    # class parameters
    COLOR_MAP={"red":(RED_SPACE_SHIP,RED_LASER),
               "green":(GREEN_SPACE_SHIP,GREEN_LASER),
               "blue":(BLUE_SPACE_SHIP,BLUE_LASER)}

    def __init__(self,x,y,color,health=100):
        super().__init__(x,y,health)
        self.ship_img,self.laser_img=self.COLOR_MAP[color]  # assign the relevant ship and layer to each enemy ships.
        self.mask=pygame.mask.from_surface(self.ship_img)

    def move(self,vel):
        self.y+=vel

    def shoot(self):
        # make sure we do not shoot too fast
        if self.cool_down_counter==0:
            laser=Laser(self.x-20,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter+=1

def collide(obj1,obj2):
    # judge if the two objects are overlap.
    offset_x=obj2.x-obj1.x
    offset_y=obj2.y-obj1.y
    ##  obj2 @imaginary origin+(3,4) +(offset_x, offset_y)=obj1 @imaginary origin
    # if the two objects are not overlapping, return None.
    return obj1.mask.overlap(obj2.mask,(offset_x,offset_y)) !=None


def main():
    run=True # control the run loop
    FPS= 60 # the frame per second when displaying
    level=0
    lives=5
    player_vel=5
    laser_vel=4
    main_font=pygame.font.SysFont("comicMe",50) # create a main font for the following text
    lost_font=pygame.font.SysFont("comicMe",60) # create a main font for the following text

    enemies=[]
    wave_length=5 # the number of enemies
    enemy_vel=1 # the speed of enemy
    lost=False
    lost_count=0

    player=Player(300,630)
    clock=pygame.time.Clock()

    def redraw_window():
        # refresh window every time with an operation
        WIN.blit(BG,(0,0)) #  creat the new background
        # draw text
        lives_label=main_font.render("Lives: {}".format(lives),1,(255,255,255))
        level_label=main_font.render("Level: {}".format(level),1,(255,255,255))

        WIN.blit(lives_label,(10,10))  # put the text into windows with a specific coordinate
        WIN.blit(level_label,(WIDTH-level_label.get_width()-10,10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            # the situation when you lost.
            lost_label=lost_font.render("You Lost !",1,(255,255,255))
            WIN.blit(lost_label,(WIDTH/2-lost_label.get_width()/2,350))

        pygame.display.update()  # update the display.

    while run:
        clock.tick(FPS) #  compatiable for different computers.
        redraw_window()
        if lives<=0 or player.health<=0:
            lost=True
            lost_count+=1

        if lost:
            if lost_count>FPS*3:
                # waiting time is too long, then quit the game after 3 seconds.
                run=False
            else:
                continue

        if len(enemies)==0:
            level+=1
            wave_length+=5
            for i in range(wave_length):
                enemy=Enemy(random.randrange(50,WIDTH-100),random.randrange(-1500,-100),
                            random.choice(["red","blue","green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            # capture every operation
            if event.type==pygame.QUIT:
                quit()

        keys=pygame.key.get_pressed()  # return a dictionary for operations keys
        if keys[pygame.K_a] and player.x-player_vel>0:  # move to left
            player.x-=player_vel
        if keys[pygame.K_d] and player.x+player_vel+player.get_width()<WIDTH:  #right
            player.x+=player_vel
        if keys[pygame.K_w] and player.y-player_vel>0:  #up
            player.y-=player_vel
        if keys[pygame.K_s] and player.y +player_vel+player.get_height()+15<HEIGHT:  #down
            player.y+=player_vel

        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            # enemies[:] is a copy of enemies, which will not modify the original list
            enemy.move(enemy_vel)  # make the enemy move
            enemy.move_lasers(laser_vel,player)

            if random.randrange(0,2*60)==1:
                # let the enemy shoot every 2 seconds.
                enemy.shoot()

            if collide(enemy,player):
                # check if enemy collide with player
                player.health-=10
                enemies.remove(enemy)
            elif enemy.y+enemy.get_height()>HEIGHT:
                # if the enemy is offscreen, or escape.
                lives-=1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel,enemies)

def main_menu():
    title_font=pygame.font.SysFont("comicMe",70)
    run=True
    while run:
        WIN.blit(BG,(0,0))
        title_label=title_font.render("Press the mouse to begin..",1,(255,255,255))
        WIN.blit(title_label,(WIDTH/2-title_label.get_width()/2,350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()
# if __name__ == '__main__':
#     main()

# a test1


