import cv2
import pyautogui
import numpy as np
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def bezier_curve(t, p0, p1, p2):
    #Compute a quadratic Bezier curve point.
    return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2

def human_like_move(start_x, start_y, end_x, end_y):
    #Move mouse with a slight curve and random jitter.
    mid_x = (start_x + end_x) // 2 + random.randint(-50, 50)
    mid_y = (start_y + end_y) // 2 + random.randint(-50, 50)
    
    # Number of steps
    num_steps = max(8, int(np.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2) / 10))
    
    for i in range(num_steps + 1):
        t = i / num_steps
        x = bezier_curve(t, start_x, mid_x, end_x) + random.randint(-1, 1)
        y = bezier_curve(t, start_y, mid_y, end_y) + random.randint(-1, 1)
        
        pyautogui.moveTo(x, y, duration=0.0001)
        
        if random.random() < 0.1:
            time.sleep(random.uniform(0.01, 0.02))

driver = webdriver.Chrome()
driver.get("https://dirtyditto.ddns.net/")
time.sleep(1.5)

button_template = cv2.imread('red_circle_template.png', cv2.IMREAD_GRAYSCALE)

last_mouse_pos = pyautogui.position()
last_move_time = time.time()

while True:
    try:
        word_display = driver.find_element(By.ID, "word-display")
        word_input = driver.find_element(By.ID, "word-input")

        if word_display.is_displayed():
            word_to_type = word_display.text.strip()
            print(f"Typing: {word_to_type}")
            word_input.send_keys(word_to_type)
            time.sleep(random.uniform(0.02, 0.05))
            continue
    except:
        pass  

    try:
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)

        result = cv2.matchTemplate(screenshot_gray, button_template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.85

        locations = np.where(result >= threshold)
        if len(locations[0]) > 0:
            print("Button detected!")

            top_left = (locations[1][0], locations[0][0])
            button_w = button_template.shape[1]
            button_h = button_template.shape[0]
            center_x = top_left[0] + button_w // 2
            center_y = top_left[1] + button_h // 2

            print(f"Moving cursor to: ({center_x}, {center_y})")

            human_like_move(*pyautogui.position(), center_x, center_y)
            time.sleep(random.uniform(0.01, 0.02))
            pyautogui.click()
            time.sleep(random.uniform(0.02, 0.05))
            continue
    except Exception as e:
        print(f"Error in button detection: {e}")
        pass

    current_mouse_pos = pyautogui.position()
    if current_mouse_pos == last_mouse_pos and (time.time() - last_move_time) > 2:
        print("Mouse hasn't moved for 2 seconds, forcing a click!")
        pyautogui.click()
        last_move_time = time.time()  

    try:
        end_message = driver.find_element(By.ID, "end-message")
        if end_message.is_displayed():
            print("Game Over! Exiting bot.")
            break
    except:
        pass  

driver.quit()
