import time
import pyautogui
import keyboard
import cv2
import numpy as np

# Load the template image
template_path = "template.JPG"
template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]  # Get width and height of template

def find_template_location():
    """Captures the screen, converts it to grayscale, and finds the template location using OpenCV."""
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # If confidence is high, return coordinates
    threshold = 0.8  # Adjust this threshold as needed
    if max_val >= threshold:
        return max_loc[0] + w // 2, max_loc[1] + h // 2  # Center of matched area
    return None

if __name__ == "__main__":
    while True:
        if keyboard.is_pressed('x'):
            for i in range(5):
                coords = find_template_location()
                if coords:
                    pyautogui.moveTo(coords[0], coords[1], duration=0.5, tween=pyautogui.easeInOutQuad)

                    pyautogui.click()
                    time.sleep(0.05)
            time.sleep(0.5)  # Small delay to prevent excessive triggering
        time.sleep(0.1)
