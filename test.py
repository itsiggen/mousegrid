# from gym import envs
# all_envs = envs.registry.all()
# env_ids = [env_spec.id for env_spec in all_envs]
# # print(env_ids)

# # del envs.registry.env_specs['MousePlane-v0']
# if 'MousePlane-v0' in envs.registry.env_specs:
#     a=1
    

# import pyautogui

# screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor.

# currentMouseX, currentMouseY = pyautogui.position() # Get the XY position of the mouse.

# # pyautogui.moveTo(100, 150) # Move the mouse to XY coordinates.

# pyautogui.moveTo(700, 500, duration=1, tween=pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.

from math import sin, cos, radians, pi, atan2, degrees, sqrt

a = [0,0]
b = [-1,-1]
d = 12

def posToAngle(p0, p1):
    angle = degrees(atan2(p1[1] - p0[1], p1[0] - p0[0]))
    return angle % 360

def angleToPos(p0, amplitude, angle):
    theta = radians(angle)
    point = [int(p0[0] + amplitude * cos(theta)), int(p0[1] + amplitude * sin(theta))]
    return point

def posToDist(p0, p1):
    dx = (p0[0]-p1[0])**2
    dy = (p0[1]-p1[1])**2
    return sqrt(dx + dy)

c = posToAngle(a, b)
e = angleToPos(a, d, c)
g = posToDist(b, e)