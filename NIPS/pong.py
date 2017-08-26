#PONG pygame

import random
import pygame, sys
from pygame.locals import *
from pykeyboard import PyKeyboard
#from pyautogui import typewrite


pygame.init()

fps = pygame.time.Clock()
#colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)

#globals
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
ball_pos = [0,0]
ball_vel = [0,0]
paddle1_vel = 0
paddle2_vel = 0
l_score = 0
r_score = 0

#canvas declaration
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Hello World')

# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2,HEIGHT/2]
    horz = random.randrange(2+8,4+8)
    vert = random.randrange(1+8,3+8)
    
    if right == False:
        horz = - horz
        
    ball_vel = [horz,-vert]

# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel,l_score,r_score  # these are floats
    global score1, score2  # these are ints
    paddle1_pos = [HALF_PAD_WIDTH - 1,HEIGHT/2]
    paddle2_pos = [WIDTH +1 - HALF_PAD_WIDTH,HEIGHT/2]
    l_score = 0
    r_score = 0
    if random.randrange(0,2) == 0:
        ball_init(True)
    else:
        ball_init(False)


#draw function of canvas
def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score
           
    canvas.fill(BLACK)
    pygame.draw.line(canvas, WHITE, [WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)
    pygame.draw.circle(canvas, WHITE, [WIDTH//2, HEIGHT//2], 70, 1)

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1] > HALF_PAD_HEIGHT and paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel > 0:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel < 0:
        paddle1_pos[1] += paddle1_vel
    
    if paddle2_pos[1] > HALF_PAD_HEIGHT and paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HALF_PAD_HEIGHT and paddle2_vel > 0:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle2_vel < 0:
        paddle2_pos[1] += paddle2_vel

    #update ball
    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])

    #draw paddles and ball
    pygame.draw.circle(canvas, RED, ball_pos, 20, 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], 0)

    #ball collision check on top and bottom walls
    if int(ball_pos[1]) <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    
    #ball collison check on gutters or paddles
    if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball_pos[1]) in range(paddle1_pos[1] - HALF_PAD_HEIGHT,paddle1_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
        r_score += 1
        ball_init(True)
        
    if int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(ball_pos[1]) in range(paddle2_pos[1] - HALF_PAD_HEIGHT,paddle2_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
        l_score += 1
        ball_init(False)

    #update scores
    myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
    label1 = myfont1.render("Score "+str(l_score), 1, (255,255,0))
    canvas.blit(label1, (50,20))

    myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
    label2 = myfont2.render("Score "+str(r_score), 1, (255,255,0))
    canvas.blit(label2, (470, 20))  
    
    
#keydown handler
def keydown(event):
    global paddle1_vel, paddle2_vel
    
    if event.key == K_i:
        paddle2_vel = -8
    elif event.key == K_k:
        paddle2_vel = 8
    elif event.key == K_w:
        paddle1_vel = -8
    elif event.key == K_s:
        paddle1_vel = 8

#keyup handler
def keyup(event):
    global paddle1_vel, paddle2_vel
    
    if event.key in (K_w, K_s):
        paddle1_vel = 0
    elif event.key in (K_i, K_k):
        paddle2_vel = 0

init()

def send_key(key):
    '''simulates key press'''
    keyboard = PyKeyboard()
    keyboard.press_key(key)
    keyboard.release_key(key)

'''   
while True:
    draw(window)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            keydown(event)
        elif event.type == KEYUP:
            keyup(event)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fps.tick(60)
'''

class Pong(object):
    '''class to represent the Pong world'''

    @staticmethod
    def initialize():
        init()

    def __init__(self):
        '''class constructor'''
        Pong.initialize()
        self.paddle1_pos_x = paddle1_pos[0]
        self.paddle1_pos_y = paddle1_pos[1]
        self.paddle2_pos_x = paddle2_pos[0]
        self.paddle2_pos_y = paddle2_pos[1]
        self.ball_pos_x = ball_pos[0]
        self.ball_pos_y = ball_pos[1]
        self.score = l_score
        self.opponent_score = r_score
        self.actions = ['w','s','i','k']
        self.start = self
        self.features = ["paddle1_xpos","paddle1_ypos","paddle2_xpos","paddle2_ypos","ball_xpos","ball_ypos","score","opponent_score"]

    def takeAction(self,state,action):
        '''returns new state
           invalid action does nothing
        '''
        global paddle1_pos,paddle2_pos,ball_pos,l_score,r_score
        if action not in self.actions:
            return state
        paddle1_pos = [state.paddle1_pos_x,state.paddle1_pos_y]
        paddle2_pos = [state.paddle2_pos_x,state.paddle2_pos_y]
        ball_pos = [state.ball_pos_x,state.ball_pos_y]
        l_score = state.score
        r_score = state.opponent_score
        i = 0
        while i < 10:
            draw(window)
            for event in pygame.event.get():
                send_key(action)
                if event.type == KEYDOWN:
                    keydown(event)
                elif event.type == KEYUP:
                    keyup(event)
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            fps.tick(60)
            i += 1
        state.paddle1_pos_x = paddle1_pos[0]
        state.paddle1_pos_y = paddle1_pos[1]
        state.paddle2_pos_x = paddle2_pos[0]
        state.paddle2_pos_y = paddle2_pos[1]
        state.ball_pos_x = ball_pos[0]
        state.ball_pos_y = ball_pos[1]
        state.score = l_score
        state.opponent_score = r_score
        if state.score>=2 or state.opponent_score>=2:
            if state.score >= state.opponent_score:
                return "winner"
            else:
                return "loser"
        return state

    def factored(self,state):
        '''returns all feature values of the state as a list'''
        factored_state = [state.paddle1_pos_x]
        factored_state += [state.paddle1_pos_y]
        factored_state += [state.paddle2_pos_x]
        factored_state += [state.paddle2_pos_y]
        factored_state += [state.ball_pos_x]
        factored_state += [state.ball_pos_y]
        factored_state += [state.score]
        factored_state += [state.opponent_score]
	return factored_state

    def __repr__(self):
        '''outputs this on call to print'''
        output_string = "\npaddle1 position: ("+str(self.paddle1_pos_x)+","+str(self.paddle1_pos_y)+")"
        output_string += "\npaddle2 position: ("+str(self.paddle2_pos_x)+","+str(self.paddle2_pos_y)+")"
        output_string += "\nball position: ("+str(self.ball_pos_x)+","+str(self.ball_pos_y)+")" 
        output_string += "your score: "+str(self.score)
        output_string += "opponent score: "+str(self.opponent_score)
        return output_string
    
'''
p = Pong()
state = p.start
print state
while state!="winner" or state!="loser":
    action = p.actions[int(random.random()*len(p.actions))]
    state = p.takeAction(state,action)
'''
