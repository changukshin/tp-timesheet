""" Module containing tool to submit the form """
import os
import time
import datetime
from selenium import webdriver
from PIL import Image

DESKTOP_PATH = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')

def submit_timesheet(url, email, date, debug=False):
    if not isinstance(date, datetime.datetime):
        raise TypeError(f"Date must be of type <datetime.datetime>, got {date}, of type: {type(date)}")

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    browser = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=options
    )

    # use browser to access desired webpage
    browser.get(URL)

    # wait a bit for elements on webpage to fully load
    browser.implicitly_wait(5)

    # find the email field element and fill your email
    email = browser.find_element("xpath", "/html/body/div/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div[1]/div/div[3]/div/div/input")
    email.send_keys(EMAIL)

    # find the date field and fill date
    date = browser.find_element("xpath", "/html/body/div/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/div[3]/div/div/input[1]")
    date.send_keys(date.strftime("%m/%d/%Y"))
    
    if debug:
        # Capture image of top half of submission
        image_path = os.path.join(DESKTOP_PATH, f"timesheet_top_{date.strftime('%d_%m_%Y')}.png")
        print(f"Saving top of timesheel to: {image_path}")
        browser.save_screenshot(image_path)
        image = Image.open(image_path)
        image.show()

    # find and fill in live hours
    live_hours = browser.find_element("xpath", "/html/body/div/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div[3]/div/div[3]/div/div/input")
    live_hours.send_keys("8")

    # find and fill in the rest of the hours
    idle_hours = browser.find_element("xpath", "/html/body/div/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div[4]/div/div[3]/div/div/input")
    idle_hours.send_keys("0")
    training_hours = browser.find_element("xpath", "/html/body/div/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div[5]/div/div[3]/div/div/input")
    training_hours.send_keys("0")
    tool_issues = browser.find_element("xpath", "/html/body/div/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div[6]/div/div[3]/div/div/input")
    tool_issues.send_keys("0")

    # find submit button and click submit
    submit = browser.find_element("xpath", "/html/body/div/div/div/div/div[1]/div/div[1]/div[2]/div[3]/div[1]/button/div")
    submit.click()
    browser.implicitly_wait(5)

    
    if debug:
        # Capture image of top half of submission
        image_path = os.path.join(DESKTOP_PATH, f"timesheet_bottom_{date.strftime('%d_%m_%Y')}.png")
        print(f"Saving bottom of timesheel to: {image_path}")
        browser.save_screenshot(image_path)
        image = Image.open(image_path)
        image.show()

    # close the browser after submitting
    browser.quit()
