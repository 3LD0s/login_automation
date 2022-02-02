from requestium import Session, Keys
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class AuthWhithCreds(object):

    counter = 0

    def __init__(self, url, username, password, email):
        self.request = Session(webdriver_path=r'./chromedriver.exe', default_timeout=3, browser='chrome', webdriver_options={'arguments': ['headless']})
        self.url = url
        self.username = username
        self.password = password
        self.email = email
        self.main()

    def login_succesful(self, inputs_names, inputs_id):

        driver = self.request.driver

        # check if login successful
        time.sleep(2)
        url = driver.current_url

        if url == self.url or "login" in url or "signin" in url or "sign-in" in url:
            print("Logging Failed")
            return False

        # TODO: check if there is text like "invailed user name or password" in response
        try:
            if driver.ensure_element_by_name("{0}".format(inputs_names["username"])).size['height'] != 0 or driver.ensure_element_by_name("{0}".format(inputs_names["username"])).size['width'] != 0 or driver.ensure_element_by_name("{0}".format(inputs_names["password"])).size['height'] != 0 or driver.ensure_element_by_name("{0}".format(inputs_names["password"])).size['width'] != 0:
                driver.get(self.url)
                time.sleep(1)
                url = driver.current_url
                if url == self.url:
                    try:
                        if driver.ensure_element_by_name("{0}".format(inputs_names["username"])).size['height'] != 0 or driver.ensure_element_by_name("{0}".format(inputs_names["username"])).size['width'] != 0 or driver.ensure_element_by_name("{0}".format(inputs_names["password"])).size['height'] != 0 or driver.ensure_element_by_name("{0}".format(inputs_names["password"])).size['width'] != 0:
                            print("Logging Failed Probably Due to Wrong username or password")
                            return False
                    except Exception:
                        pass

        except Exception:
            pass

        try:
            if driver.ensure_element_by_id("{0}".format(inputs_id["username"])).size['height'] != 0 or driver.ensure_element_by_name("{0}".format(inputs_names["username"])).size['width'] != 0 or driver.ensure_element_by_id("{0}".format(inputs_id["password"])).size['height'] != 0 or driver.ensure_element_by_name("{0}".format(inputs_names["password"])).size['width'] != 0:
                driver.get(self.url)
                time.sleep(1)
                url = driver.current_url
                if url == self.url:
                    try:
                        if driver.ensure_element_by_id("{0}".format(inputs_id["username"])).size['height'] != 0 or driver.ensure_element_by_name("{0}".format(inputs_names["username"])).size['width'] != 0 or driver.ensure_element_by_id("{0}".format(inputs_id["password"])).size['height'] != 0 or driver.ensure_element_by_name("{0}".format(inputs_names["password"])).size['width'] != 0:
                            print("Logging Failed Probably Due to Wrong username or password")
                            return False

                    except Exception:
                        pass

        except Exception:
            pass

        return True

    """
    ###################################################################
    The Function log in to the site and returning the Session Logged in
    ###################################################################
    """
    def main(self):
        boolstatement = "(inp.attrs.get('name') and '{0}' in inp.attrs.get('name').lower()) or (inp.attrs.get('id')" \
                        " and '{0}' in inp.attrs.get('id')) or (inp.attrs.get('placeholder') and '{0}' in inp.attrs.get('placeholder'))"
        AuthWhithCreds.counter += 1
        if 3 > AuthWhithCreds.counter > 1:
            print("Something Went Wrong\nTrying again")
        if AuthWhithCreds.counter > 3:
            self.request.driver.close()
            print("We Couldn't Connect to the Site")
            return None, False

        inputs_id = {}
        btn_id = ""
        btn_name = ""
        inputs_names = {}
        userauth = self.email
        driver = self.request.driver
        flag = False  # False if one step login True if two steps

        driver.get(self.url)
        innerhtml = driver.execute_script("return document.body")
        time.sleep(1)
        soup = BeautifulSoup(innerhtml.get_attribute('innerHTML'), "lxml")

        doc_inputs = soup.findAll("input")
        buttons = soup.findAll("button")

        if not doc_inputs:
            print("There Was A Problem With The Connection")
            driver.close()
            return None, False

        btn_opt = None  # flag for button login option
        for btn in buttons:

            # search for Login button
            if btn.text and ("login" in btn.text.lower() or "sign-in" in btn.text.lower() or "sign in" in btn.text.lower() or "log in" in btn.text.lower()):
                if btn.attrs['type'] == "submit":

                    btn_id = btn.attrs.get('id')
                    if btn_id:
                        btn_opt = "id"
                        continue

                    btn_name = btn.attrs.get('name')
                    if btn_name:
                        btn_opt = "name"
                        continue

            # search for two step login button
            if (btn.text and btn.text.lower() == "next") or (btn.attrs.get("value") and btn.attrs.get("value").lower() == "next"):
                flag = True
                break

        for inp in doc_inputs:

            # Search for username input
            if_statment = eval(boolstatement.format('user'))
            if if_statment and (inp.attrs['type'] == "text"):
                inp_id = inp.attrs.get("id")
                if inp_id:
                    inputs_id["username"] = inp_id
                    userauth = self.username
                else:
                    userauth = self.username
                    inputs_names["username"] = inp.attrs.get('name')
                continue

            # Search for email input
            if_statment = eval(boolstatement.format('mail'))
            if if_statment and (inp.attrs['type'] == "text" or inp.attrs['type'] == "email"):
                inp_id = inp.attrs.get("id")
                if inp_id:
                    inputs_id["username"] = inp_id
                    userauth = self.email
                else:
                    userauth = self.email
                    inputs_names["username"] = inp.attrs.get('name')
                continue

            # Search for password input
            if_statment = eval(boolstatement.format('pass'))
            if if_statment and (inp.attrs['type'] == "password"):
                inp_id = inp.attrs.get("id")
                if inp_id:
                    inputs_id["password"] = inp_id
                else:
                    inputs_names["password"] = inp.attrs.get('name')
                break

        # Try with the other one
        if AuthWhithCreds.counter == 2:
            if userauth == self.email:
                userauth = self.username
            else:
                userauth = self.email

        self.request.transfer_session_cookies_to_driver(self.url)
        driver.get(self.url)
        time.sleep(1)

        try:
            # IF LOGIN By Input ID
            if inputs_id:
                # if Two steps login
                if flag:
                    driver.ensure_element_by_css_selector("#{0}".format(inputs_id["username"])).send_keys(userauth, Keys.ENTER)
                    time.sleep(1.5)

                # One Step login
                else:
                    driver.ensure_element_by_css_selector("#{0}".format(inputs_id["username"])).send_keys(userauth)

                time.sleep(1.5)

                # if Recaptcha-V2 Bypass
                try:
                    recaptchastatment = eval("driver.find_element_by_css_selector(\"iframe[name^='a-']"
                                             "[src^='https://www.google.com/recaptcha/api2/anchor?\']\").size[\'height\']"
                                             " != 0 and driver.find_element_by_css_selector(\"iframe[name^=\'a-\']"
                                             "[src^=\'https://www.google.com/recaptcha/api2/anchor?\']\").size[\'width\']"
                                             " != 0")
                    if recaptchastatment:
                        recaptcha(driver)
                        time.sleep(2)
                except Exception:
                    pass

                # type in password
                driver.ensure_element_by_css_selector("#{0}".format(inputs_id["password"])).send_keys(self.password, Keys.ENTER)

            # IF LOGIN By Input Name
            else:
                # if Two steps login
                if flag:
                    driver.ensure_element_by_name("{0}".format(inputs_names["username"])).send_keys(userauth, Keys.ENTER)
                    time.sleep(1.5)

                # One Step login
                else:
                    driver.ensure_element_by_name("{0}".format(inputs_names["username"])).send_keys(userauth)

                time.sleep(1.5)

                # if Recaptcha-V2 Bypass
                try:
                    recaptchastatment = eval("driver.find_element_by_css_selector(\"iframe[name^='a-']"
                                             "[src^='https://www.google.com/recaptcha/api2/anchor?\']\").size[\'height\']"
                                             " != 0 and driver.find_element_by_css_selector(\"iframe[name^=\'a-\']"
                                             "[src^=\'https://www.google.com/recaptcha/api2/anchor?\']\").size[\'width\']"
                                             " != 0")
                    if recaptchastatment:
                        recaptcha(driver)
                        time.sleep(2)
                except Exception:
                    pass

                # type in password
                driver.ensure_element_by_name("{0}".format(inputs_names["password"])).send_keys(self.password, Keys.ENTER)

        except Exception as e:
            print(e)
            return self.main()

        url = driver.current_url
        if url == self.url:
            # try login with button
            try:
                if btn_opt:
                    if btn_opt == "id":
                        driver.ensure_element_by_id(btn_id).click()
                    else:
                        driver.ensure_element_by_name(btn_name).click()

            except Exception:
                if self.login_succesful(inputs_names, inputs_id):
                    return self.main()

        time.sleep(2)

        if not self.login_succesful(inputs_names, inputs_id):
            return self.main()

        """print(url)
        try:
            self.request.transfer_driver_cookies_to_session()

        except Exception as e:
            driver.close()
            print("The Was An Error: The Session has been Deleted\n{0}".format(e))
            return None, False"""

        print("# Login Successfull\n")
        AuthWhithCreds.counter = 0
        return self.request, True


"""
#################################
The Function Bypass ReCaptcha-v2
#################################
"""
def recaptcha(driver):
    try:
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()
        driver.switch_to.default_content()
        return
    except Exception:
        driver.switch_to.default_content()
        return


if __name__ == '__main__':
    login = AuthWhithCreds("http://18.158.46.251:4961/index.php", "testme", "testme123", "testme@gmail.com")
