import cv2
import screen_coords as sc
import random

screen = sc.World(1000, 500)

screen.world_vertices.append([100, 100, 500])
screen.world_vertices.append([-100, 100, 500])
screen.world_vertices.append([0, -100, 500])
screen.world_faces.append([0, 1, 2])

screen.world_vertices.append([200, 200, 500])
screen.world_vertices.append([-200, 200, 500])
screen.world_vertices.append([0, -200, 500])
screen.world_faces.append([0, 1, 2])

while True:
    '''for i in range(1):
        for j in range(3):
            screen.world_vertices.append([random.uniform(-1000, 1000), random.uniform(-1000, 1000), random.uniform(-1000, 1000)])
        l = len(screen.world_vertices)
        screen.world_faces.append([l - 3, l - 2, l - 1])'''
    screen.update_screen()
    cv2.imshow('image', screen.screen)
    cv2.waitKey(1)
