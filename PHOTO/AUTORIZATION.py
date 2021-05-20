import pickle
import time
import os

from loguru import logger

from DELETE_WATEMARK import tarnslate_photo_on_treatment
from DRIVER import get_chromedriver
from GET_PHOTO_ORIGINAL import get_photo_original, get_photo_download

class PhotoOptimazerPy:

    @staticmethod
    def get_driver():
        driver = get_chromedriver(use_proxy=False, mobile=False)
        return driver

    def auth(self, driver):
        driver.get('https://www.myheritage.com/photo-enhancer?lang=RU')
        time.sleep(3)

        cookies = pickle.load(open("cookies", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)

        driver.refresh()
        time.sleep(3)


    def upgrage_photo(self):
        photos = get_photo_download()
        for photo in photos:
            tarnslate_photo_on_treatment(photo)
            os.remove(photo)

        logger.debug('All Photo Upgrade')


    def load_photo(self):
        driver = self.get_driver()
        self.auth(driver)
        logger.info('Auth Accepted')
        photos = get_photo_original()

        for photo in photos:
            driver.get('https://www.myheritage.com/photo-enhancer?lang=RU')
            time.sleep(2)

            PHOTO_INPUT = driver.find_element_by_xpath(
                '//*[@id="photo_enrichment_root"]/div/div[1]/section/div[2]/div/button/span/input')
            PHOTO_INPUT.send_keys(photo)
            time.sleep(30)

            driver.find_element_by_xpath(
                '//*[@id="photo_enrichment_root"]/div/div/div/section/div[1]/div[1]/span/span/button').click()
            time.sleep(2)
            driver.find_element_by_xpath(
                '//*[@id="photo_enrichment_root"]/div/div/div/section/div[1]/div[1]/span/ul/li[1]').click()
            time.sleep(10)
            os.remove(photo)


        driver.close()
        driver.quit()
        logger.info('START UPGRATE PHOTO')
        self.upgrage_photo()


if __name__ == '__main__':
    logger.debug('Satrt Ptrogramm...')
    photo_optimazer_py = PhotoOptimazerPy()

    while True:
        try:
            photo_optimazer_py.load_photo()
        except:
            time.sleep(100)
