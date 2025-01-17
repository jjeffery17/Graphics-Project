import cv2
import screen_coords as sc

# initialise space
screen = sc.World(1000, 600)

# create face for testing
screen.world_vertices.append([100, 100, 500])
screen.world_vertices.append([-100, 100, 500])
screen.world_vertices.append([0, -100, 500])
screen.world_faces.append([0, 1, 2])

while True:
    # update screen and display
    screen.update_screen()
    cv2.imshow('image', screen.screen)
    cv2.waitKey(1)
