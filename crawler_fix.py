"""
     A simple search-based twitter scraper
"""

import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import pandas as pd


def create_webdriver_instance():
    driver = webdriver.Edge()
    driver.maximize_window()
    return driver


def login_to_twitter(username, password, driver):
    url = 'https://twitter.com/i/flow/login'
    try:
        driver.get(url)
        username = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "text"))).send_keys(username)
        username = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "text"))).send_keys(Keys.ENTER)
        username = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys(password)
        username = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys(Keys.ENTER)
    except exceptions.TimeoutException:
        print("Timeout while waiting for Login screen")
        return False
        
    try:
        url = "https://twitter.com/home"
        WebDriverWait(driver, 10).until(EC.url_to_be(url))
    except exceptions.TimeoutException:
        print("Timeout while waiting for home screen")
    return True


def generate_tweet_id(tweet):
    return ''.join(tweet)


def scroll_down_page(driver, last_position, num_seconds_to_load=0.5, scroll_attempt=0, max_attempts=5):
    """The function will try to scroll down the page and will check the current
    and last positions as an indicator. If the current and last positions are the same after `max_attempts`
    the assumption is that the end of the scroll region has been reached and the `end_of_scroll_region`
    flag will be returned as `True`"""
    end_of_scroll_region = False
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(num_seconds_to_load)
    curr_position = driver.execute_script("return window.pageYOffset;")
    if curr_position == last_position:
        if scroll_attempt < max_attempts:
            end_of_scroll_region = True
        else:
            scroll_down_page(last_position, curr_position, scroll_attempt + 1)
    last_position = curr_position
    return last_position, end_of_scroll_region


def save_tweet_data_to_csv(records, filepath, mode='a+'):
    header = ['display_name', 'username', 'tweet_text','profile_img', 'post_url', 'post_date', 'reply_count', 'retweet_count', 'like_count']
    with open(filepath, mode=mode, newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if mode == 'w':
            writer.writerow(header)
        if records:
            writer.writerow(records)


def collect_all_tweets_from_current_view(driver, lookback_limit=25):
    """The page is continously loaded, so as you scroll down the number of tweets returned by this function will
     continue to grow. To limit the risk of 're-processing' the same tweet over and over again, you can set the
     `lookback_limit` to only process the last `x` number of tweets extracted from the page in each iteration.
     You may need to play around with this number to get something that works for you. I've set the default
     based on my computer settings and internet speed, etc..."""
    sleep(10)
    #page_cards = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="tweet"]')))
    page_cards = driver.find_elements(By.XPATH, '//div[@data-testid]//article[@data-testid="tweet"]') #(By.XPATH, '//div[@data-testid="tweet"]')
    if len(page_cards) <= lookback_limit:
        return page_cards
    else:
        return page_cards[-lookback_limit:]

def extract_data_from_current_tweet_card(card):
    #Extract Displayed Name
    try:
        display_name =  card.find_element(By.XPATH, './/span').text
    except exceptions.NoSuchElementException:
        display_name = ""
    except exceptions.StaleElementReferenceException:
        return
    #Extract Username
    try:
        username = card.find_element(By.XPATH, './/span[contains(text(), "@")]').text
    except exceptions.NoSuchElementException:
        username = ""
    #Extract Displayed Name Post Name
    try:
        post_date =  card.find_element(By.XPATH, './/time').get_attribute('datetime')
    except exceptions.NoSuchElementException:
        return
    #Extract Tweet
    try:
        tweet_text = card.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
        tweet_text = tweet_text.replace("\n", "")
    except exceptions.NoSuchElementException:
        tweet_text = ""
    #Extract reply_count
    try:
        reply_count = card.find_element(By.XPATH,'.//div[@data-testid="reply"]').text
        if reply_count == "" :
            reply_count = "0"
    except exceptions.NoSuchElementException:
        reply_count = ""
    #Extract retweet_count
    try:
        retweet_count =  card.find_element(By.XPATH,'.//div[@data-testid="retweet"]').text
        if retweet_count == "" :
            retweet_count = "0"
    except exceptions.NoSuchElementException:
        retweet_count = ""
    #Extract like_count
    try:
        like_count =  card.find_element(By.XPATH,'.//div[@data-testid="like"]').text
        if like_count == "" :
            like_count = "0"
    except exceptions.NoSuchElementException:
        like_count = ""
    #Extract profile image
    try:
        profile_img =  card.find_element(By.CSS_SELECTOR, 'img[alt][draggable="true"]').get_attribute('src')
        if profile_img == "" :
            profile_img = "N/A"
    except exceptions.NoSuchElementException:
        profile_img = ""
    #Extract post_url
    try:
        post_url =  card.find_element(By.CSS_SELECTOR, "a[aria-label][dir]")
        post_url = str(post_url.get_attribute("href")) #str(post_url.get_attribute("href").split("/")) + " " + 
        if post_url == "" :
            post_url = "N/A"
    except exceptions.NoSuchElementException:
        post_url = ""

    tweet = (display_name, username, tweet_text, profile_img, post_url, post_date, reply_count, retweet_count, like_count)
    print(tweet)
    return tweet

def main(username, password, filepath, target):
    save_tweet_data_to_csv(None, target, 'w')  # create file for saving records
    last_position = None
    end_of_scroll_region = False
    unique_tweets = set()

    driver = create_webdriver_instance()
    logged_in = login_to_twitter(username, password, driver)
    if not logged_in:
        return

    df = pd.read_csv(filepath)
    for url in df["post_url"]:
        url_split = url.split('/')
        end_of_scroll_region = False
        if url_split[3] != 'mandiricare' :
            driver.get(url)
            try :
                clicked = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Show']/ancestor::div[@role='button']")))
                clicked.click()
                print(url + "success clicked")
            except exceptions.TimeoutException:
                print(url + "failed clicked")
                pass
            try :
                clicked = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Show more replies']/ancestor::div[@role='button']")))
                clicked.click()
                print(url + "success clicked")
            except exceptions.TimeoutException:
                print(url + "failed clicked")
                pass
            while not end_of_scroll_region:
                cards = collect_all_tweets_from_current_view(driver)
                for card in cards:
                    try:
                        tweet = extract_data_from_current_tweet_card(card)
                    except exceptions.StaleElementReferenceException:
                        continue
                    if not tweet:
                        continue
                    tweet_id = generate_tweet_id(tweet)
                    if tweet_id not in unique_tweets:
                        unique_tweets.add(tweet_id)
                        save_tweet_data_to_csv(tweet, target)
                last_position, end_of_scroll_region = scroll_down_page(driver, last_position)

    driver.quit()


if __name__ == '__main__':
    usr = "reyndomly"
    pwd = "5141211Nobita"
    path = 'tweet_brand_abuse.csv'
    target = 'target.csv'

    main(usr, pwd, path, target)