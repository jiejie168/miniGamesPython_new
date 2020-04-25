__author__ = 'Jie'
"""
a simple number guess game
"""
import pygame
import time

#pygame.init()
class Guessgame:

    def __init__(self,nums,mn=0,mx=100):
        self.nums=int(nums)
        self.min=mn
        self.max=mx
        self.guesses=0

    def get_guess(self):
        guess=input("Please input your guess number (from {} to {}): ".format(self.min,self.max))
        if self.valid_number(guess):
            return int(guess)
        else:
            print ("Please enter a valid number")
            return self.get_guess()

    def valid_number(self,str_number):
        try:
            number=int(str_number)
        except:
            return False
        return    True  #number >=self.min  and number <=self.max

    def play(self):
        while True:
            self.guesses+=1
            guess=self.get_guess()

            if guess<self.nums:
                print ("Your guess was under")
            elif guess >self.nums:
                print ("Your guess was over")
            else:
                break
        print ("Your guessed it in {} guesses".format(self.guesses))

def main():
    win=pygame.display.set_mode((300,300))
    pygame.display.set_caption("GuessGame")

    start_time=time.time()
    run=True
    while run:
        play_time=round(time.time()-start_time)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False

main()

# guessGame=Guessgame(50,0,100)
# guessGame.play()

