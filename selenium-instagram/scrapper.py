# Built-In Imports
import time
import re
import sys
# Local Import
from conf import URL, USR, PWD, DEFAULT_TIME_SLEEP
from data_manager import get_data, data_to_file
# Selenium Import
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

# NOTE: Headless is generating a warning so for the time being the option is commented
# Once solved will be implemented again

# Setup Browser Options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('log-level=3')
# Create Selenium Browser
# browser = webdriver.Chrome(options=chrome_options)
browser = webdriver.Chrome()

# FUNCTIONS
def select_now_not():
    # Search Notification Pop-Ups and select 'Not Now' option
    if len(browser.find_elements_by_class_name("cmbtv")) > 0:
        not_now_btn = browser.find_element_by_class_name("cmbtv").find_element_by_css_selector("button[type='button']")
        not_now_btn.click()
    elif len(browser.find_elements_by_class_name("mt3GC")) > 0:
        not_now_btn = browser.find_element_by_class_name("mt3GC").find_element_by_class_name("HoLwm")
        not_now_btn.click()
    else:
        return True
    return False

def get_profile_data():
    # Gets data from target profile and stores it in a dictionary
    profile_info_list = browser.find_elements_by_class_name("-nal3")
    profile_dict = dict()
    # Split text to get data and key
    for info in profile_info_list:
        info_content = info.text.split(' ')
        # 1: Desc. 0: Data
        profile_dict.update({info_content[1]: info_content[0]})

    return profile_dict

def get_given_profiles(profile):
    # Indicate profile to be scraped
    print(f"Proccessing {profile}'s account...")
    # Goto target profile and get data
    browser.get(f'{URL}/{profile}')

    time.sleep(DEFAULT_TIME_SLEEP)

    # Check if profile exists
    if len(browser.find_elements_by_class_name("dialog-404")) < 1:

        # Followers, Following and Posts
        profile_data = fix_data(get_profile_data())
        # Username
        profile_data.update({'username': profile})
        # Posts's Likes and Comments
        profile_data.update({'content': get_profile_posts()})
        # Posts description (mean, median, min. max, variance)
        desc = get_data(profile_data['content'])
        profile_data.update({'description': desc})

        return profile_data

    print(f"Account {profile} is not available or does not exists.")
    return dict()

def fix_data(profile):
    # Cleans data and converts it to integer
    keys = profile.keys()
    for k in keys:
        if type(profile[k]) == str:
            # Remove commas from integers
            profile[k] = profile[k].replace(',','')
            # k = thousand case, m = millions case
            if profile[k].__contains__('k'):
                profile[k] = float(profile[k].replace('k',''))*1000
            elif profile[k].__contains__('m'):
                profile[k] = float(profile[k].replace('m',''))*1000000
            profile[k] = int(profile[k])

    return profile

def scroll_to_bottom():
    visited = list() # List of post already mined
    posts = list() # List of dictionaries with data

    while not browser.execute_script("if ((window.innerHeight + window.scrollY) >= document.getElementsByClassName('_9eogI E3X2T')[0].scrollHeight) {return true;} else {return false;}", browser.find_element_by_tag_name("html")):
        # Step 1: Scroll to bottom
        browser.execute_script("document.scrollingElement.scrollTop = document.scrollingElement.scrollHeight;", browser.find_element_by_tag_name("html"))
        time.sleep(DEFAULT_TIME_SLEEP)
        # Step 2: Get urls
        raw_html = browser.find_element_by_tag_name('html').get_attribute('innerHTML')
        regex_list = re.findall(r'href=[\'"]?([^\'" >]+)', raw_html)
        # Step 3: Filter urls
        post_links = [l for l in regex_list if l.__contains__('/p/') and l not in visited]
        # Step 4: Get likes and comments
        posts.extend([get_likes_and_comments(href) for href in post_links])
        # Step 5: Add visited urls
        visited.extend(post_links)

    return posts

def get_likes_and_comments(href):
    # Locate Post element
    target_link = browser.find_element_by_xpath(f'//a[@href="{href}"]')
    time.sleep(1)
    # Hover element to display target data
    hover = ActionChains(browser).move_to_element(target_link)
    hover.perform()

    # Get data from hovered element
    if browser.find_element_by_class_name("qn-0x"):
        # Check if description element is empty (Applies for sensitive content posts)
        if browser.find_element_by_class_name("qn-0x").text != '':

            data_element = browser.find_element_by_xpath("//div[@class='qn-0x']")
            element_data_list = data_element.find_elements_by_class_name("-V_eO")

            profile_dict = dict()

            # 0: Likes 1: Comments
            profile_dict.update({'Likes': element_data_list[0].text, 'Comments': element_data_list[1].text, 'IsSensitive': 0})

            # Convert strings to integers
            cleaned_profile_dict = fix_data(profile_dict)

            # Add post URL
            cleaned_profile_dict.update({'url': href})

            return cleaned_profile_dict
        else:
            return {'Likes': 0, 'Comments': 0, 'IsSensitive': 1}

    # If cannot find element return an empty dictionary
    return dict()

def get_profile_posts():
    # Get Likes and Comments from the user's posts
    posts_content = scroll_to_bottom()

    return posts_content

# MAIN EXECUTION
def init(username=USR, password=PWD):

    # Goto Website
    browser.get(URL)

    time.sleep(DEFAULT_TIME_SLEEP)

    # Login fields and Submit
    username_field = browser.find_element_by_name("username")
    password_field = browser.find_element_by_name("password")

    submit_button = browser.find_element_by_css_selector("button[type='submit']")

    username_field.send_keys(USR)
    password_field.send_keys(PWD)

    time.sleep(DEFAULT_TIME_SLEEP)

    submit_button.click()

    time.sleep(DEFAULT_TIME_SLEEP)

    # Check if Username/Passwords are valid
    if not browser.find_elements_by_id("slfErrorAlert"):

        print("Login Successful")

        # Enter the Target Profiles
        print("Be sure to separate the target users with a comma ','")
        profiles = input("Enter the Target Profiles: ").replace(" ","").split(",")

        print("Please wait until data has ben adquired.")

        check = False

        # If notification options are disabled select the 'Not Now' option from the Pop-Up
        while not check:
            check = select_now_not()
            time.sleep(DEFAULT_TIME_SLEEP)

        # Change Language to English
        lang_select = browser.find_element_by_css_selector("select[class='hztqj']")
        lang_select.find_element_by_css_selector("option[value='en']").click()

        # List of target Instagram profiles
        # profiles = ['somekindofcomedy', 'shgurr', 'laurenillustrated']

        # Extract data from profiles
        full_data = list(map(get_given_profiles, profiles))

        # Proceed to create JSON file with data
        data_to_file(full_data)

    else:
        # If error message is generated copy the message and display it
        error_msg = browser.find_element_by_id("slfErrorAlert").text
        print(error_msg)

    # Exit Selenium
    browser.quit()


if __name__ == '__main__':
    try:
        # Enter Username and Password
        # INST_USERNAME = sys.argv[1]
        # INST_PASSWORD = sys.argv[2]

        init()

        # Check if fields fulfill the requirements
        """
        if len(INST_USERNAME) > 1 and len(INST_PASSWORD) > 6:
            init(INST_USERNAME, INST_PASSWORD)
        else:
            print("Username/Password is too short!.")"""
    except IndexError as err:
        print("There was a problem with the username and password. Did you remember to add them?")