# from gym import envs
# all_envs = envs.registry.all()
# env_ids = [env_spec.id for env_spec in all_envs]
# # print(env_ids)

# # del envs.registry.env_specs['MousePlane-v0']
# if 'MousePlane-v0' in envs.registry.env_specs:
#     a=1
    
# import random
# import pyautogui

# screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor.

# currentMouseX, currentMouseY = pyautogui.position() # Get the XY position of the mouse.

# # pyautogui.moveTo(100, 150) # Move the mouse to XY coordinates.

# #chrome coords 438, 526
# pyautogui.moveTo(468, 506, duration=0, tween=pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.

# import requests

# r = requests.get("http://localhost:5000/alterego/result")
# result = r.json()["score"]
# print(result)

# from random import choice, randrange

# a = choice([(1,5),(9,15),(21,27)])
# b = randrange(*a)

import pyautogui as ag

ag.moveTo(990, 260, duration=0.5, tween=ag.easeOutQuad) 

# from math import sin, cos, radians, pi, atan2, degrees, sqrt

# a = [0,0]
# b = [-1,-1]
# d = 12

# def posToAngle(p0, p1):
#     angle = degrees(atan2(p1[1] - p0[1], p1[0] - p0[0]))
#     return angle % 360

# def angleToPos(p0, amplitude, angle):
#     theta = radians(angle)
#     point = [int(p0[0] + amplitude * cos(theta)), int(p0[1] + amplitude * sin(theta))]
#     return point

# def posToDist(p0, p1):
#     dx = (p0[0]-p1[0])**2
#     dy = (p0[1]-p1[1])**2
#     return sqrt(dx + dy)

# c = posToAngle(a, b)
# e = angleToPos(a, d, c)
# g = posToDist(b, e)

