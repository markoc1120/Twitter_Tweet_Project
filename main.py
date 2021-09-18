from selenium import webdriver
import time
import os

chrome_driver = os.environ.get('chrome_driver')
DOWN = 35
UP = 20
EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')


class InternetSpeedTwitterBot:

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=chrome_driver)
        self.down: float
        self.up: float

    def get_internet_speed(self):
        self.driver.get('https://www.speedtest.net/')
        consent_b = self.driver.find_element_by_css_selector('#_evidon-banner-acceptbutton')
        consent_b.click()
        time.sleep(5)
        start_b = self.driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a')
        start_b.click()
        time.sleep(45)
        self.down = float(self.driver.find_element_by_css_selector('.result-item-download .download-speed').text)
        self.up = float(self.driver.find_element_by_css_selector('.result-item-upload .upload-speed').text)

    def tweet_at_provider(self):
        self.get_internet_speed()
        self.driver.get('https://twitter.com/login?lang=en-gb')
        time.sleep(5)
        email = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input')
        email.send_keys(EMAIL)
        password = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input')
        password.send_keys(PASSWORD)
        login = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div')
        login.click()
        time.sleep(10)
        if DOWN < self.down or UP < self.up:
            tweet_msg = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div')
            message = f'Hey my internet connection is {self.down}down/{self.up}up instead of the guaranteed {DOWN}down/{UP}up'
            tweet_msg.send_keys(message)
            tweet_b = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]')
            tweet_b.click()
        else:
            print('Everything is good.')

        self.driver.quit()


bot = InternetSpeedTwitterBot()
bot.tweet_at_provider()
