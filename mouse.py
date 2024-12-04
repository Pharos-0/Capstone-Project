##import mouse
####
##### left click
##mouse.click('left')
####
##### right click
####mouse.click('right')
####
##### middle click
####mouse.click('middle')

# https://pyautogui.readthedocs.io/en/latest/mouse.html

import pyautogui

pyautogui.click(10, 5)

pyautogui.click(100, 100)
pyautogui.moveTo(100, 150)
pyautogui.moveRel(0, 10)  # move mouse 10 pixels down
pyautogui.dragTo(100, 150)
pyautogui.dragRel(0, 10)  # drag mouse 10 pixels down
