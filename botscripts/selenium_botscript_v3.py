import cv2
import pyautogui
import numpy as np
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def bezier_curve(p0, p1, p2, p3, n=10):
    """Generates n points along a bezier curve for fast movement"""
    points = []
    for t in np.linspace(0, 1, n):
        x = (1 - t)**3 * p0[0] + 3 * (1 - t)**2 * t * p1[0] + 3 * (1 - t) * t**2 * p2[0] + t**3 * p3[0]
        y = (1 - t)**3 * p0[1] + 3 * (1 - t)**2 * t * p1[1] + 3 * (1 - t) * t**2 * p2[1] + t**3 * p3[1]
        points.append((x, y))
    return points

def human_like_move(start_x, start_y, end_x, end_y):
    """Move mouse smoothly, with speed variation"""
    num_points = random.randint(7, 12) 
    
    # Create random control points 
    mid_x1 = start_x + random.randint(-40, 40)
    mid_y1 = start_y + random.randint(-40, 40)
    mid_x2 = end_x + random.randint(-40, 40)
    mid_y2 = end_y + random.randint(-40, 40)

    path = bezier_curve((start_x, start_y), (mid_x1, mid_y1), (mid_x2, mid_y2), (end_x, end_y), n=num_points)

    # Move along the path quickly
    for (x, y) in path:
        pyautogui.moveTo(x, y, duration=random.uniform(0.002, 0.007)) 

# Start WebDriver
driver = webdriver.Chrome()
driver.get("https://dirtyditto.ddns.net/")
time.sleep(1.5)  # Reduce wait time

button_template = cv2.imread('red_circle_template.png', cv2.IMREAD_GRAYSCALE)

last_mouse_pos = pyautogui.position()
last_move_time = time.time()

while True:
    try:
        # Start of word challenge
        word_display = driver.find_element(By.ID, "word-display")
        word_input = driver.find_element(By.ID, "word-input")

        if word_display.is_displayed():
            word_to_type = word_display.text.strip()
            print(f"Typing: {word_to_type}")
            word_input.send_keys(word_to_type)
            time.sleep(random.uniform(0.2, 0.4))  # Adjust for faster typing
            continue
    except:
        pass  

    try:
        # Start of button challenge
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)

        # Perform template matching
        result = cv2.matchTemplate(screenshot_gray, button_template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.85  # Slightly stricter for better accuracy

        locations = np.where(result >= threshold)
        if len(locations[0]) > 0:
            print("Button detected!")

            # Get first match
            top_left = (locations[1][0], locations[0][0])
            button_w = button_template.shape[1]
            button_h = button_template.shape[0]
            center_x = top_left[0] + button_w // 2
            center_y = top_left[1] + button_h // 2

            print(f"Fast-moving cursor to: ({center_x}, {center_y})")

            human_like_move(*pyautogui.position(), center_x, center_y)
            pyautogui.click()

            time.sleep(random.uniform(0.1, 0.2))  # Minimize delay
            continue
    except Exception as e:
        print(f"Error in button detection: {e}")
        pass

    current_mouse_pos = pyautogui.position()
    if current_mouse_pos == last_mouse_pos and (time.time() - last_move_time) > 2:
        print("Mouse hasn't moved for 2 seconds, forcing a click!")
        pyautogui.click()
        last_move_time = time.time()  

    # Checks if the game is over
    try:
        end_message = driver.find_element(By.ID, "end-message")
        if end_message.is_displayed():
            print("Game Over! Exiting bot.")
            break
    except:
        pass  

# Close the browser
driver.quit()
