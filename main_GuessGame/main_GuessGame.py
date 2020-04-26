__author__ = 'Jie'
"""
a simple number guess game
"""
import pygame as pg
import time

pg.init()
class Guessgame:

    def __init__(self,nums,mn=0,mx=100):
        self.nums=int(nums)
        self.min=mn
        self.max=mx
        self.guesses=0
        self.guessed=False

    def get_guess(self,guess):
        # guess=input("Please input your guess number (from {} to {}): ".format(self.min,self.max))
        if self.valid_number(guess):
            return int(guess)
        else:
            print ("Please enter a valid number")
            return self.get_guess(guess)

    def valid_number(self,str_number):
        try:
            number=int(str_number)
        except:
            return False
        return    True  #number >=self.min  and number <=self.max

    def play(self,guess):
        while True:
            self.guesses+=1
            guess=self.get_guess(guess)

            if guess<self.nums:
                print ("Your guess was under")
            elif guess >self.nums:
                print ("Your guess was over")
            else:
                break
        print ("Your guessed it in {} guesses".format(self.guesses))


# screen = pg.display.set_mode((640, 480))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FNT=pg.font.SysFont("comicsans",40)  # create a font type of text
# FONT = pg.font.Font(None, 32)
class InputBox:

    def __init__(self,x,y,width, height, text= 'aa'):
        self.rect=pg.Rect(x,y,width,height)  # create a rect box
        self.width=width
        self.height=height
        self.text=text
        self.color=COLOR_ACTIVE
        self.txt_surface=FNT.render(text,True,self.color)  # render the specific text with a specific color.
        self.active=False
        self.selected=None
        self.flag=False
        self.guessed=False

    def update_model(self):
        # resize the box if the text is too long
        width=max(200,self.txt_surface.get_width()+10)
        self.rect.w=width

    def draw(self,screen):
        # assign coordinates, and draw the rendered specific text to the windows/screens
        screen.blit(self.txt_surface,(self.rect.x+5,self.rect.y+5))
        # draw the rect on the screen
        # pg.draw.rect(screen,self.color,self.rect,3)

        if self.selected:
            pg.draw.rect(screen,self.color,self.rect,3)

    def operate_event(self, event):

        if event.type==pg.MOUSEBUTTONDOWN:
            # Check if the rect is active by use collidepoint method
            if self.rect.collidepoint(event.pos):
                # the event.pos is collide with rect, then active
                self.active=not self.active
                self.selected=True
            else:
                self.active=False
                self.selected=False
            # change the color of the input box
            self.color=COLOR_ACTIVE if self.active else COLOR_INACTIVE

        if event.type==pg.KEYDOWN:
            if self.active:
                if event.key==pg.K_RETURN:
                    print(self.text)
                    # self.text=""
                    self.flag=True
                elif event.key==pg.K_BACKSPACE:
                    self.text=self.text[:-1]
                    self.txt_surface=FNT.render(self.text,True,self.color)
                else:
                    self.text +=event.unicode
                #Re-render the text
                    self.txt_surface=FNT.render(self.text,True,self.color)
    def playgame(self):
        guessgame=Guessgame(50,0,100)
        if self.flag :
            guessgame.play(self.text)
        if self.text==guessgame.nums:
            self.guessed=True
        return self.guessed


def main():
    win=pg.display.set_mode((500,500))

    inputBox_1=InputBox(100,100,140,40)
    inputBox_2=InputBox(100,300,140,40)
    inputBoxs=[inputBox_1,inputBox_2]
    pg.display.set_caption("GuessGame")

    start_time=time.time()
    run=True
    while run:
        play_time=round(time.time()-start_time,1)  # round a number with some decimals

        for event in pg.event.get():
            if event.type==pg.QUIT:
                run=False
            inputBox_1.operate_event(event)
        guessed=inputBox_1.playgame()

        inputBox_1.update_model()
        win.fill((255,255,255))
        inputBox_1.draw(win)

        if guessed:
            run=False
        pg.display.update()

main()

# guessGame=Guessgame(50,0,100)
# guessGame.play()


