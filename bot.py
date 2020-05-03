import random
import pyautogui

screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor.

currentMouseX, currentMouseY = pyautogui.position() # Get the XY position of the mouse.

    
def box():
    pyautogui.moveTo(438, 526, duration=0.2, tween=pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.
    pyautogui.click()
    pyautogui.moveTo(1968, 396, duration=0.2, tween=pyautogui.easeInOutQuad)
    
def v2():
    pyautogui.moveTo(468, 396, duration=0, tween=pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.
    pyautogui.click()
    pyautogui.moveTo(1968, 396, duration=0, tween=pyautogui.easeInOutQuad)
    
def v3():
    pyautogui.moveTo(608, 396, duration=0, tween=pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.
    pyautogui.click()
    pyautogui.moveTo(1968, 396, duration=0, tween=pyautogui.easeInOutQuad)
    
def trig():
    pyautogui.moveTo(468, 506, duration=0, tween=pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.
    pyautogui.click()
    pyautogui.moveTo(1968, 396, duration=0, tween=pyautogui.easeInOutQuad)
    
def clear():
    pyautogui.moveTo(448, 806, duration=0, tween=pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.
    pyautogui.click()
    pyautogui.moveTo(1968, 396, duration=0, tween=pyautogui.easeInOutQuad)
    
def bottin():
    reps = 50
    pyautogui.moveTo(500, 500, duration=0, tween=pyautogui.easeInOutQuad)
    while reps > 0:
        pyautogui.moveTo(random.randrange(100, 1000), random.randrange(100, 750), duration=0.001, tween=pyautogui.easeInOutQuad)
        reps -= 1
    pyautogui.moveTo(1968, 396, duration=0, tween=pyautogui.easeInOutQuad)
    
def bottin2():
    reps = 50
    pyautogui.moveTo(500, 500, duration=0, tween=pyautogui.easeInOutQuad)
    while reps > 0:
        pyautogui.moveTo(500, 1000, duration=0, tween=pyautogui.easeInOutQuad)
        pyautogui.moveTo(500, 500, duration=0, tween=pyautogui.easeInOutQuad)
        reps -= 1
    pyautogui.moveTo(1968, 396, duration=0, tween=pyautogui.easeInOutQuad)
    
def reset():
    pyautogui.moveTo(998, 526, duration=0, tween=pyautogui.easeInOutQuad)
    pyautogui.click()       
    pyautogui.press('esc')
    pyautogui.moveTo(1968, 396, duration=0, tween=pyautogui.easeInOutQuad)      
        
# box()
# reset()
# v2()
# v3()
# trig()
# clear()
bottin()
