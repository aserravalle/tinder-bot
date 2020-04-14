from selenium import webdriver
from credentials import *
from time import sleep
import model

class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome("../chromedriver")

    def login(self):
        # Load page and click "Login with Facebook"
        self.driver.get("https://tinder.com/")
        sleep(3)
        self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[2]/button').click()

        # Switch to popup
        base_window = self.driver.window_handles[0]
        self.driver.switch_to.window(self.driver.window_handles[1])

        # Login with credentials
        self.driver.find_element_by_xpath('//*[@id="email"]').send_keys(username)
        self.driver.find_element_by_xpath('//*[@id="pass"]').send_keys(password)
        self.driver.find_element_by_xpath('//*[@id="u_0_0"]').click()

        # Return to Tinder window and close popups that arise
        self.driver.switch_to.window(base_window)
        sleep(5)
        self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]').click()
        sleep(0.5)
        self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]').click()
        sleep(5)

    def like(self):
        self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button').click()
        print("like")

    def dislike(self):
        self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[1]').click()
        print("dislike")

    def close_popup(self):
        self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button[2]').click()
        print("close popup")

    def match(self):
        # Determine when we are in a "Match State" and send the canned opener
        self.driver.find_element_by_xpath('//*[@id="chat-text-area"]').send_keys(opener)
        self.driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/div[3]/form/button/span').click()
        print("match")

    def auto_swipe(self):
        while True:
            sleep(0.5)
            try: # Find hit like or dislike based on output of model.py
                p = model.predict()
                print(p)
                if p < 0.8:
                    self.like()
                else:
                    self.dislike()
            except: # If the like button is gone...
                try:
                    self.match()
                except: # send match
                    self.close_popup()

if __name__ == '__main__':
    bot = TinderBot()
    bot.login()
    bot.auto_swipe()
