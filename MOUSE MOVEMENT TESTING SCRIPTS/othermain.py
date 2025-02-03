import time
import keyboard
import cv2
import numpy as np
import mouse  # Using the mouse library for smoother movement
from scipy.interpolate import interp1d
import random
import pyautogui

# Load the template image
template_path = "template.JPG"
template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]  # Get width and height of template

def find_template_location():
    """Captures the screen, converts it to grayscale, and finds the template location using OpenCV."""
    screenshot = np.array(mouse.get_position())  # Using mouse lib for cursor position
    screenshot = np.array(pyautogui.screenshot())
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # If confidence is high, return coordinates
    threshold = 0.8  # Adjust this threshold as needed
    if max_val >= threshold:
        return max_loc[0] + w // 2, max_loc[1] + h // 2  # Center of matched area
    return None

def smooth_move(x, y, duration=0.7, steps=30):
    """Moves the mouse smoothly using a Bézier-like curve."""
    start_x, start_y = mouse.get_position()
    
    # Create intermediate points
    mid_x = (start_x + x) // 2 + random.randint(-50, 50)
    mid_y = (start_y + y) // 2 + random.randint(-50, 50)
    
    xs = np.linspace(0, 1, steps)
    interp_x = interp1d([0, 0.5, 1], [start_x, mid_x, x], kind='quadratic')
    interp_y = interp1d([0, 0.5, 1], [start_y, mid_y, y], kind='quadratic')

    for i in xs:
        mouse.move(interp_x(i), interp_y(i), absolute=True, duration=duration / steps)
        time.sleep(duration / steps)

if __name__ == "__main__":
    while True:
        if keyboard.is_pressed('x'):
            for i in range(5):
                coords = find_template_location()
                if coords:
                    smooth_move(coords[0], coords[1], duration=0.1)
                    mouse.click()
                    time.sleep(0.05)
            time.sleep(0.5)  # Small delay to prevent excessive triggering
        time.sleep(0.1)
