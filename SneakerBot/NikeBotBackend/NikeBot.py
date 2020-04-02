#from seleniumwire import webdriver
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import threading


#GLOBAL VARS
delay = 2 #seconds -> Later, If the drops happen at specific times usually can have bot only check most
                   #frequently around then

class NikeBot:

    def __init__(self, url, size, username, password, guest_checkout=False):
        # only grabbing one username/password so that I can spawn multiple threads of this process for multiple profiles.
        self.url                    = str(url)
        self.size                   = str(size)
        self.username               = str(username)
        self.password               = str(password)
        self.guest_checkout         = bool(guest_checkout)
        # open webdriver, incognito & start maximized
        chrome_options              = Options()
        # Setup chrome options for better performance / less issues with elements in the way
        # headless browser = No UI = Less Resources;
        chrome_options.add_argument("--headless")
        # incognito for no leftover cookies
        chrome_options.add_argument("--incognito")
        # use maximzied when not using headless
        # chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("--window-size=1920x1080")
        # https://medium.com/@pyzzled/running-headless-chrome-with-selenium-in-python-3f42d1f5ff1d
        self.driver                 = webdriver.Chrome(executable_path='chromedriver.exe', 
                                    options=chrome_options) #, seleniumwire_options={'verify_ssl': False}
        #Modiftying Headers for headless version
        self.driver.header_overrides = {
            'Access-Control-Allow-Origin': f'{self.url}',
            'SameSite': 'True',
        }
        self.driver.implicitly_wait(1)
        # self.wait.until(EC.presence_of_elemennt(BY.ID, "name")
        self.wait                   = WebDriverWait(self.driver, delay)
        # start main loop, unsure if this is correct process; 
        
        
    def main_loop(self):
        #will monitor the URL & select size (new function) & finally click add to cart
        self.driver.get(self.url)
        #Scroll Window to "height" to uncover Size & add-to-cart buttons just in case they are covered;
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #Setup While Loop, will refresh page every 10seconds (we can make this much more effecient)
        # We could refresh every 10-15sec but only when close to the "drop"
        purchaseEnabled = False
        while(purchaseEnabled == False):
            try:
                purchaseBtn = self.driver.find_element_by_xpath('//button[@data-qa="add-to-cart"]')
                
            except Exception as err:
                print(f'+[main_loop]: {err}')
                print(f'+[main_loop]: Sleeping 10 Seconds & Refreshing the Page.')
                time.sleep(10)
                self.driver.refresh()
                time.sleep(1)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1) #i havent found a better way to wait after running javascript  
            else:
                if purchaseBtn.is_displayed():
                    purchaseEnabled = True
                    return self.select_size()

    def select_size(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        try:
            sizeBtn = self.driver.find_element_by_xpath(f'//button[contains(text(), "{self.size}")]')
            self.driver.execute_script("arguments[0].scrollIntoView(true);", sizeBtn)
            time.sleep(2)
            sizeBtn.click()
            self.driver.save_screenshot(f"{self.driver.service.process.pid}-show size clicked.png")
            #self.wait.until(EC.element_to_be_clickable(
                #(By.XPATH, f'//button[contains(text(), "{self.size}")]'))).click()
            
        except Exception as err:
            #print(err)
            #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.close()
            return print(f"+[select_size]: Error Selecting Size, Is it available? {err}")
        else:
            print("+[select_size]: Size Selected")

            return self.add_to_cart()

    def add_to_cart(self):
        add2cartBtn = self.driver.find_element_by_xpath('//button[@data-qa="add-to-cart"]')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", add2cartBtn)
        # self.wait.until(EC.presence_of_element_located(add2cartBtn))                              TRY THIS NEXT
        time.sleep(2) #this sleep is necessary to wait until the above script has finished;
        try:
            #time.sleep(2)
            #add2cartBtn.click()                           
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//button[@data-qa="add-to-cart"]'))).click()
                #if this returns true with no exceptions, we should have an item in our cart, lets
                # check it out 
        except Exception as err:
            #if there is any Exception, scroll bottom of page into view & try again in finally branch;
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(f"+[add_to_cart]: Error: {err} ")
            #self.driver.close()
            return False
        else:
            print("+[add_to_cart]: add-to-cart button clicked")
            return self.go_to_cart()

    def go_to_cart(self):
        # click nav-bar cart instead of iframe popup, iframe is unreliable timing wise;
        # could even just navigate to nike.com/cart probably;
        #WebDriverWait(self.driver, delay).until(EC.element_to_be_clickable(
        #    (By.XPATH, '//li[@data-qa="top-nav-cart-link"]'))).click()
        cart_button = self.driver.find_element_by_xpath('//li[@data-qa="top-nav-cart-link"]')
        cart_button.click()
        try:
            self.wait.until(EC.title_contains('Cart'))
        except:
            return print("+[go_to_cart]: didnt detect title change to cart")
        else:
            time.sleep(5)
            x_items = self.driver.find_element_by_xpath('//div[@class="ncss-col-sm-12 css-8yxtvd"]')
            x_items_innerHTML = str(x_items.get_attribute("innerHTML"))
            if x_items_innerHTML.startswith('1'):
                self.driver.save_screenshot(f"{self.driver.service.process.pid}-1 item in cart.png")
                return self.check_out()
            elif x_items_innerHTML.startswith('0'):
                #No items found
                #self.driver.save_screenshot(f"{self.driver.service.process.pid}-no item cart.png")
                print("+[go_to_cart]: No Items Found In Cart, Restarting")
                self.driver.get(self.url)
                time.sleep(2)
                #self.driver.execute_script("window.history.go(-1)")
                #time.sleep(2) #necessary for above script to finish going back in browser;
                return self.select_size() #test this
            else:
                print("+[go_to_cart]: More than 1 Item, or Error")
                return False

    def close(self):
        return self.driver.close()

    def check_out(self):
        #click checkout link on pop up
        #self.driver.save_screenshot(f"{self.driver.service.process.pid}.png")
        #time.sleep(2) #time to let frame popup
        try:
            #attempt to click checkout-link on popup, if it fails, click cart-icon on nav-bar
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//button[@data-automation="checkout-button"]'))).click()
        except Exception as err:
            print(f"+[check_out]: {err}")
            return False
        else:
            print("+[check_out]: Entered Checkout Processes")
            #now login as member
            # scroll to top of window for screenshot
            self.driver.execute_script("window.scrollTo(0,0);")
            # take screenshot to make sure it added to cart;
            self.driver.save_screenshot(f"{self.driver.service.process.pid}-member or guest.png")
            #return self.check_out_as_member()
            if self.guest_checkout == True:
                print(f"+[check_out]: Checking out as Guest: {self.guest_checkout}")
                return self.checkout_as_guest()
            else:
                print(f"+[check_out]: Checking out as Guest: {self.guest_checkout}")
                print("+[check_out]: Checking out as Member")
                return self.check_out_as_member()

    def check_out_as_member(self):
        #We're on the page that ask's whether you want to login or checkout as guest now;
        try: #fill in username
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//input[@data-componentname="emailAddress"]'))).send_keys(self.username)
            #self.driver.find_element_by_xpath('//input[@data-componentname="emailAddress"]').send_keys(self.username)
        except Exception as err:
            print(f"Login Error: {err}")
        else:
            self.driver.find_element_by_xpath('//input[@data-componentname="password"]').send_keys(self.password)
            self.driver.save_screenshot(f"{self.driver.service.process.pid}-before clicking login.png")
            self.driver.find_element_by_xpath('//input[@value="MEMBER CHECKOUT"]').click()
            time.sleep(1)   # sleep to allow loading for screenshot; all sleeps can be optimized.
            self.driver.save_screenshot(f"{self.driver.service.process.pid}-after clicking login.png")
            return 

    def checkout_as_guest(self):
        #We're on the page that ask's whether you want to login or checkout as guest now;
        
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="qa-guest-checkout"]'))).click()
        #input first name
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//input[@id="firstName"]'))).send_keys('John')
        
        #input last name
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//input[@id="lastName"]'))).send_keys('Doe')

        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//a[@id="addressSuggestionOptOut"]'))).click()

        #start to fill in address
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//input[@id="address1"]'))).send_keys('2400 harbor blvd')
        
        #fill in city
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//input[@id="city"]'))).send_keys('costa mesa')
    
        #select state from drop down
        myselect = Select(self.driver.find_element_by_id('state'))
        #select visible text / state
        myselect.select_by_visible_text("California")
        
        #enter zip code
        self.driver.find_element_by_xpath('//input[@id="postalCode"]').send_keys('92626')
        
        #enter email address
        self.driver.find_element_by_xpath('//input[@id="email"]').send_keys('nowaythisisarealnikeeamil@gmail.com')
        
        #enter phone number
        self.driver.find_element_by_xpath('//input[@id="phoneNumber"]').send_keys('1234567897')
        
        #click continue after entering address
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@class="js-next-step saveAddressBtn mod-ncss-btn ncss-btn-accent ncss-brand pt3-sm prl5-sm pb3-sm pt2-lg pb2-lg d-md-ib u-uppercase u-rounded fs14-sm mod-button-width"]'))).click()

        #click continue to payment information
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@class="js-next-step continuePaymentBtn mod-ncss-btn ncss-btn-accent ncss-brand mod-button-width pt3-sm prl5-sm pb3-sm pt2-lg pb2-lg u-md-ib u-uppercase u-rounded fs14-sm"]'))).click()

        #now entering credit card information
        time.sleep(2)
        
        # wait for cc frame & switch to it;
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(
            (By.XPATH,"//iframe[@class='credit-card-iframe mt1 u-full-width prl2-sm']")))
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@class='mod-ncss-input ncss-input pt2-sm pr4-sm pb2-sm pl4-sm' and @id='creditCardNumber']"))).send_keys("1234567812345678")
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@class='mod-ncss-input ncss-input pt2-sm pr4-sm pb2-sm pl4-sm' and @id='expirationDate']"))).send_keys("0822")
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@class='mod-ncss-input ncss-input pt2-sm pr4-sm pb2-sm pl4-sm' and @id='cvNumber']"))).send_keys("682")
        self.driver.save_screenshot(f"{self.driver.service.process.pid}-all done.png")
        self.driver.save_screenshot()
        self.driver.save_screenshot(f"/screenshots/{self.driver.service.process.pid}-all done.png")
# if __name__ == '__main__':
#     url1 = 'https://www.nike.com/launch/t/air-max-triax-96-university-red/'
#     url2 = 'https://www.nike.com/launch/t/sb-dunk-high-paul-rodriguez/'  #no checkout button available until 1/21 @ 8am;
#     url3 = 'https://www.nike.com/launch/t/pg-4-gatorade-gx/'
#     url4 = 'https://www.nike.com/launch/t/air-jordan-1-high-black-gym-red/'
#     size = 'M 10'
#     login_username = 'removed_for_security'
#     login_temp_pass = 'removed_for_security'
#     #test1= NikeBot(url1, size, login_username, login_temp_pass, True )
#     # test2= NikeBot(url2, size, login_username, login_temp_pass )
#     test3= NikeBot(url3, 'M 7.5', login_username, login_temp_pass, True )
#     # test4= NikeBot(url4, size, login_username, login_temp_pass )

#     try:
#         #test1.main_loop()
#         test3.main_loop()
#     except:
#         #test1.close()
#         test3.close()
#     else:
#         #test1.close()
#         test3.close()

#     # test3.close()
#     # test4.close()

#     # test3= NikeBot(url3, 'M 7.5', login_username, login_temp_pass )
#     # test3.main_loop()
#     # test3.close()

#     # test4= NikeBot(url4, size, login_username, login_temp_pass )
#     # test4.main_loop()
#     # test4.close()
#     #test.close()
