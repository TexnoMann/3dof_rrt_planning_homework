import pygame
import time
import numpy as np
from typing import Tuple
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.collision_checking import Line, Circle, Chain, check_chain_circle_tuple_collision
from algorithms.RRR_3dof_kinematic import *
from algorithms.RRTVlad import RRT,Map

SCREEN_SIZE = (800, 800)
FIELD_SIZE = (3.0, 3.0)
BASE_POINT = np.array([0.0, 0.0])
SCALE_FACTOR = np.array(SCREEN_SIZE)/np.array(FIELD_SIZE)
LINK_LENGHT = np.array([0.8, 0.7, 0.9])
METRICS_SCALE_FACTOR = np.linalg.norm(np.array(SCREEN_SIZE))/np.linalg.norm(np.array(FIELD_SIZE))

def draw_chain(surf: pygame.display, chain: Chain):
    key_points = []
    for p in chain.points:
        lp = p*SCALE_FACTOR
        key_points.append((lp[0], lp[1],))
    # print(key_points)
    pygame.draw.lines(surf, (0,125, 185), False, key_points, width=5)
    for p in key_points:
        pygame.draw.circle(surf, (255, 80, 10), p, 5)

def draw_circle(surf: pygame.display, circle: Circle):
    pygame.draw.circle(surf, (100, 100, 100), circle.p*SCALE_FACTOR, circle.r*METRICS_SCALE_FACTOR)

th = np.array([np.pi/4, np.pi/3, np.pi/4])

if __name__ == "__main__":


    map3Drand = Map(dim=3, obs_num=2,
        obs_size_min=0.05, 
        obs_size_max=0.4, 
        xinit=np.array([0.1, 0.3, 0.1]), 
        xgoal=np.array([1.5, 0.0, 0.5]), 
        field_range = np.array([-np.pi/2 , np.pi]), 
        links_length=LINK_LENGHT
    )

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    screen.fill((255, 255, 255))

    running = True
    time_start = time.time()
    while running:
        screen.fill((255, 255, 255))

        # th = np.random.rand(3)*2*np.pi - np.pi/2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pos = pygame.mouse.get_pos()
        pressed1 = pygame.mouse.get_pressed()[0]
        # Check if rectangle collided with pos and if the left mouse button was pressed
        if pressed1:
            print("You have opened a chest!")
            th = get_angles2(pos/SCALE_FACTOR, LINK_LENGHT, th)[0]

        if th is None:
            continue
        
        print(th)
        # print(th)
        ch = Chain(tuple([BASE_POINT] +list(get_point(th, LINK_LENGHT))))
        
        for ob in map3Drand.obstacles:
            draw_circle(screen, ob)
        draw_chain(screen, ch)

        print(check_chain_circle_tuple_collision(ch, map3Drand.obstacles) )

        pygame.display.flip()
        time.sleep(0.001)

    pygame.quit()