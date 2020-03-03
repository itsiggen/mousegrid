# from gym import envs
# all_envs = envs.registry.all()
# env_ids = [env_spec.id for env_spec in all_envs]
# print(env_ids)

import pyautogui

screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor.

currentMouseX, currentMouseY = pyautogui.position() # Get the XY position of the mouse.

# pyautogui.moveTo(100, 150) # Move the mouse to XY coordinates.

pyautogui.moveTo(2500, 500, duration=1, tween=pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.

# distance = 200
# while distance > 0:
#         pyautogui.drag(distance, 0, duration=0.5)   # move right
#         distance -= 5
#         pyautogui.drag(0, distance, duration=0.5)   # move down
#         pyautogui.drag(-distance, 0, duration=0.5)  # move left
#         distance -= 5
#         pyautogui.drag(0, -distance, duration=0.5)  # move up