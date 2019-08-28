from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import TimeoutException
from waits.status_changed import status_changed
from waits.can_find import can_find
from ArgsHandler import args_handler
import logging
import sys
using_commands = True
for arg in sys.argv:
    arg_bits = arg.split("=")
    if arg_bits[0].lower() == "message":
        using_commands = False
if using_commands:
    try:
        import commands
    except:
        print("If not using a defined message (see '" + sys.argv[0] + " help') you must have a commands.py file present in the root directory.")
        quit()
import traceback
import time
import json

# Set up logging format
logging.basicConfig(filename='Sola.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
print("Logging configured!")

class Sola:
    def __init__(self, email, password, browser_options, dev, message):
        self.email = email
        self.password = password
        self.browser_options = browser_options
        self.dev = dev
        self.message = message

    def setup(self):
        # Select correct browser + options
        try:
            if self.browser_options["browser"] == 'chrome': #Select your browser (Maybe support other browsers in the future?)
                options = ChromeOptions()
                if self.browser_options["headless"] == (str(1)): #If headless, become the horseman
                    options.add_argument("--headless")
                    options.add_argument("--window-size=1920x1080")
                print("Creating webdriver...")
                self.driver = webdriver.Chrome(chrome_options=options)
                print("Webdriver created!")
            else:
                options = FirefoxOptions()
                if self.browser_options["headless"] == (str(1)): #If headless, become the horseman
                    options.headless = True
                print("Creating webdriver...")
                self.driver = webdriver.Firefox(options=options)
                print("Webdriver created!")

            self.wait = WebDriverWait(self.driver, 10) #Wait time-outs are stupid in this case. Just build better waits.
        except (KeyboardInterrupt, SystemExit): #Allow users to manually exit
            quit()
        except:
            logging.critical(traceback.format_exc())
            print("Could not create driver. Make sure you have installed the browser you're trying to use, have added this root folder to your path, and that you have at least 600 MB of free RAM. See Sola.log for more details on the error.")
            quit()

    def get_info(self):
        info = {}
        try:
            message_list = self.driver.find_element_by_class_name("ChatMessageList.ChatContainer__messagesList").find_element_by_class_name("ChatMessageList__messagesWrapper.ChatMessageList__messagesWrapper--shortReadReceipt")
            try:
                senders = message_list.find_elements_by_class_name("ChatMessage__sender")
                info["message_sender"] = senders[-1].get_attribute("innerHTML").split("<")[0]
                info["message_sender_email"] = senders[-1].get_attribute("data-email")
            except:
                info["message_sender"] = "Unknown"
                info["message_sender_email"] = "Unknown"
            try:
                messages = message_list.find_elements_by_class_name("ChatMessageList__messageContainer")
                info["message_text"] = messages[-1].find_element_by_class_name("Linkify").get_attribute("innerHTML")
            except:
                info["message_text"] = "Unknown"
        except:
                info["message_sender"] = "Unknown"
                info["message_sender_email"] = "Unknown"
                info["message_text"] = "Unknown"
        return info

    def find_updates(self):
        while True:
            print("Waiting for msg...")
            try:
                self.wait.until(status_changed(self.driver))
            except TimeoutException:
                continue
            except (KeyboardInterrupt, SystemExit): #Allow users to manually exit
                quit()
            except: # Some other exception 
                if self.dev: print("I ERRORED while waiting for incoming messages")
                if self.dev: print(traceback.format_exc())
                continue
            card_list = self.driver.find_element_by_class_name("CardList__items").find_elements_by_class_name("Card")
            for card in card_list: # Yes I know a for loop that only ever does one card is stupid don't @me
                card_list = self.driver.find_element_by_class_name("CardList__items").find_elements_by_class_name("Card")
                room_url_tokens = card.find_element_by_class_name("Card__link").get_attribute("href").split("/")
                print(card.get_attribute("outerHTML"))
                if "conversations" in room_url_tokens:
                    user = card.find_element_by_class_name("Card__title").get_attribute("innerHTML")
                    link = card.find_element_by_class_name("Card__link").get_attribute("href")
                    card.click()
                    values = self.get_info()
                    self.select_message_box()
                    if(self.message != None):
                        self.send_message(self.message)
                    else:
                        self.send_message(commands.process_message_personal(user, link, values["message_text"], values["message_sender"], values["message_sender_email"], self.send_message))
                    self.driver.execute_script("window.history.go(-1)")
                    time.sleep(3)
                    break
                elif ("rooms" in room_url_tokens) and (card.find_element_by_class_name("CardSubtitle__primarySubtitle").get_attribute("innerHTML").split(" ")[0] == "@mentioned"):
                    room = card.find_element_by_class_name("Card__title").get_attribute("innerHTML")
                    link = card.find_element_by_class_name("Card__link").get_attribute("href")
                    card.click()
                    values = self.get_info()
                    self.select_message_box()
                    if(self.message != None):
                        self.send_message(self.message)
                    else:
                        self.send_message(commands.process_message_group(room, link, values["message_text"], values["message_sender"], values["message_sender_email"], self.send_message))
                    self.driver.execute_script("window.history.go(-1)")
                    time.sleep(3)
                    break
                else:
                    room = card.find_element_by_class_name("Card__title").get_attribute("innerHTML")
                    link = card.find_element_by_class_name("Card__link").get_attribute("href")
                    card.click()
                    values = self.get_info()
                    self.select_message_box()
                    if(self.message == None): # ChatMessage__sender
                        self.send_message(commands.process_message_group_no_at(room, link, values["message_text"], values["message_sender"], values["message_sender_email"], self.send_message))
                    self.driver.execute_script("window.history.go(-1)")
                    time.sleep(3)
                    break

    def chime_login(self):
        #Make sure user has internet
        try:
            self.driver.get("https://app.chime.aws")
        except:
            print("You have no internet connection, so I cannot run. Fix ur internet bro")
            quit()
        
        # Navigate past the starting login screen which actually doesn't do anything.
        self.driver.find_element_by_id("profile_primary_email").send_keys(email)
        self.driver.find_element_by_class_name("providers-emailSubmit").click()

        # Gotta see if we're using an internal account:
        time.sleep(3)
        if self.driver.title.find("AWS Apps Authentication") != -1:
            self.driver.find_element_by_id("wdc_username").send_keys(self.email[:-1*len("@amazon.com")])
            self.driver.find_element_by_id("wdc_password").send_keys(self.password)
            self.driver.find_element_by_id("wdc_login_button").click()
        else:
            # Fun fact, we don't actually need that button to load, we can just navigate there directly
            self.driver.get("https://signin.id.ue1.app.chime.aws/auth/amazon")

            # Log in to the actual login page
            self.driver.find_element_by_id("ap_email").send_keys(email)
            self.driver.find_element_by_id("ap_password").send_keys(password)
            self.driver.find_element_by_id("signInSubmit").click()

        # Chill for a minute to let the page load
        time.sleep(3)

        a = 0 # little count variable so we can display captcha errors.
        while self.driver.title.find("Amazon Chime") == -1: #We got captcha'd or one-time-passworded

            # One-time password
            if self.driver.title == "Authentication required":
                # Navigate to and find the right box
                self.driver.find_element_by_id("continue").click()
                self.wait.until(can_find(self.driver, "a-input-text.a-span12.cvf-widget-input.cvf-widget-input-code"))
                code_box = self.driver.find_element_by_class_name("a-input-text.a-span12.cvf-widget-input.cvf-widget-input-code")
                
                # Get the code from user
                code = input("Please enter the one-time code from your email:\n")
                code_box.send_keys(code)
                self.driver.find_element_by_class_name("a-button-input").click()
                # Allow time for page to check code
                time.sleep(1)
                if(self.driver.title == "Authentication required"):
                    print("Incorrect code.")
            # Captcha NOTE: this does not work right now.
            else:
                ## THE BELOW CODE DOES NOT WORK. For whatever reason, when selecting the button, the captcha doesn't leave, even if the captcha is correct.
                print("############################################# Start copying below this line ######################################################")
                # Print just the snippet of the captcha (This needs to be updated to only be the URL)
                print(self.driver.find_element_by_id("auth-captcha-image-container").get_attribute("outerHTML"))
                if a != 0:
                    print(self.driver.find_element_by_class_name("a-alert-content").get_attribute("innerHTML"))
                print("Please copy the above page code and paste it into a text file. Save it as [anything].html, then open it with a browser.")
                self.driver.find_element_by_id("ap_password").send_keys(password)
                captcha = input("Please enter the captcha from the page you loaded:\n")
                self.driver.find_element_by_id("auth-captcha-guess").send_keys(captcha)
                self.driver.find_element_by_name("signIn").submit()
                time.sleep(3)
                if self.driver.title.find("Amazon Chime") == -1:
                    print("Incorrect captcha")
                    a += 1

    def select_message_box(self):
        self.message_box = self.driver.find_element_by_class_name("notranslate.public-DraftEditor-content") #Get the actual place to type

    def smart_send(self, key):
        try:
            self.message_box.send_keys(key)
        except:
            self.message_box = self.driver.find_element_by_class_name("notranslate.public-DraftEditor-content")
            message_box.send_keys(key)

    def send_message(self, message):
        #Any parsing of html bs must be done before swapping the &codes. Also, swapping & MUST be done last.
        #                                                                         THIS ↓ is NOT a space, it's a no break space. Pls no change.
        message = message.replace("&gt;", ">").replace("&lt;", "<").replace("&nbsp;", " ").replace("&amp;", "&") #Fix the replacement selenium does when reading text
        try:
            self.driver.execute_script("this.setChatInput(arguments[0]);", message)
            self.smart_send(Keys.RETURN)
        except Exception as e:
            if self.dev: print(traceback.format_exc())
            if self.dev: print("Failed to send message, most likely because the message_box reference died.")

info = args_handler(sys.argv)

email = info["email"]
password = info["password"]
browser_options = {"browser": info["browser"], "headless": info["headless"]}
dev = info["dev"] if "dev" in info else "0"
message = info["message"] if "message" in info else None

#Make our bot
bot = Sola(email, password, browser_options, dev, message)

while True:
    try:
        bot.setup()
        bot.chime_login()
        bot.find_updates()
    except (KeyboardInterrupt, SystemExit): #Allow users to manually exit
        quit()
    except:
        logging.error(traceback.format_exc())
        try: 
            bot.driver.quit()
        except:
            pass
        continue