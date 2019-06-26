#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from DataStructure.StringManipulator import Enumerate, Manipulate
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Selenium:

    sleep_time_default = 0.1
    max_try_count_default = 2
    sleep_time = sleep_time_default
    max_try_count = max_try_count_default
    xpath = None
    link = None
    trigger_xpaths_list = []
    element = None
    elements = None
    elements_count = None
    extract = None

    def __init__(self, extension_directory_path=None):

        chrome_driver_path = "/home/user/Desktop/prodPop/chromedriver"


        if extension_directory_path is not None:
            chrome_options = Options()
            chrome_options.add_argument("--load-extension=" + extension_directory_path)
            self.Driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=chrome_options)
        elif extension_directory_path is None:
            chrome_options = Options()
            chrome_options.add_argument("--window-size=1920,1080");
            chrome_options.add_argument("--start-maximized");
            chrome_options.add_argument("--disable-gpu")
            #chrome_options.add_argument("--headless");
            self.Driver = webdriver.Chrome(executable_path=chrome_driver_path,chrome_options=chrome_options)
        #self.Driver.set_window_size(2500, 15000)


    def Close(self):

        self.Driver.close()

    def Refresh(self):
        self.Driver.refresh()
    def ResetParameter(self, parameter):

        if parameter == "sleep_time" or parameter is None:
            self.sleep_time = self.sleep_time_default
        if parameter == "max_try_count" or parameter is None:
            self.max_try_count = self.max_try_count_default
        if parameter == "link" or parameter is None:
            self.link = None
        if parameter == "trigger_xpaths_list" or parameter is None:
            self.trigger_xpaths_list = []
        if parameter == "element" or parameter is None:
            self.element = None
        if parameter == "elements" or parameter is None:
            self.elements = None
        if parameter == "elements count" or parameter is None:
            self.elements = None
        if parameter == "extract" or parameter is None:
            self.extract = None

    def ResetParameters(self, parameters=None):

        if isinstance(parameters, list):
            for parameter in parameters:
                self.ResetParameter(parameter)
        else:
            self.ResetParameter(parameters)

    def BackPage(self):
        self.Driver.back()

    def Load(self, link=None):

        if link is not None:
            self.link = link
        print("Loading:", self.link)
        self.Driver.get(self.link)
        self.ResetParameters("trigger_xpaths_list")

    def ErrorHandling(self, e, try_count):

        self.element = None
        print(str(e))
        if self.max_try_count - try_count != 1:  # Prevents unneccesary refresh at last try count
            self.Load(self.link)
            time.sleep(self.sleep_time * try_count)
            print("Re-clicks:", self.trigger_xpaths_list)
            self.BackPage()
            for trigger_xpath in self.trigger_xpaths_list:
                self.ClickIt(trigger_xpath, reserve_trigger=False)
                time.sleep(self.sleep_time * try_count)

    def ExtractElementProcess(self):

        for try_count in range(0, self.max_try_count):
            try:
                # wait for element to appear, then hover it
                wait = WebDriverWait(self.Driver, 20)
                self.element = wait.until(EC.visibility_of_element_located((By.XPATH, self.xpath)))
                ActionChains(self.Driver).move_to_element(self.element).perform()
                print("Extracted element:", self.xpath)
                break
            except Exception as e:
                a = 10
                print(e)
                #self.ErrorHandling(e, try_count)

    def ExtractElement(self, xpath=None):

        self.element = None
        self.extract = None
        if isinstance(xpath, list):
            for self.xpath in xpath:
                self.ExtractElementProcess()
                if self.element is not None:
                    return self.element
        elif xpath is not None:
            self.xpath = xpath
            self.ExtractElementProcess()
        return self.element
    def ExtractElementsProcess(self):

        for try_count in range(0, self.max_try_count):
            self.elements = self.Driver.find_elements_by_xpath(self.xpath)
            self.elements_count = len(self.elements)
            if self.elements_count != 0:
                print("Extracted", str(self.elements_count), "elements:", self.xpath)
                break
            elif self.elements_count == 0:
                a = None
                print("none")
                #self.ErrorHandling(e, try_count)

    def ExtractElements(self, xpath=None, return_type = None):

        self.elements = None
        self.extract = None
        self.elements_count = None
        if xpath is not None:
            self.xpath = xpath
        if isinstance(xpath, list):
            for self.xpath in xpath:
                self.ExtractElementsProcess()
                if self.elements_count != 0:
                    if return_type is None:
                        return self.elements
                    elif return_type == "elements_count":
                        return self.elements_count
        elif xpath is not None:
            self.xpath = xpath
            self.ExtractElementsProcess()
        if return_type is None:
            return self.elements
        elif return_type == "elements_count":
            return self.elements_count


    def ClickIt(self, trigger_xpath):
        wait = WebDriverWait(self.Driver, 20)
        Click_Process = wait.until(EC.element_to_be_clickable((By.XPATH,trigger_xpath)))
        Click_Process.click()


    def ExtractElementsToSeparatedText(self, separator=", ", xpath=None):

        if xpath is not None:
            self.xpath = xpath
        self.ExtractElements(self.xpath)
        if self.elements is []:
            self.extract = None
        elif self.elements != [] and self.elements is not None:
            self.extract = []
            for element in self.elements:
                self.element = element
                self.extract.append(self.element.text)
                if separator is not None:
                    self.extract.append(separator)
            self.extract.pop(-1)
            self.extract = ''.join(self.extract)
        return self.extract

    def ExtractElementText(self, xpath=None):

        if xpath is not None:
            self.xpath = xpath
        self.ExtractElement(self.xpath)
        if self.element is not None:
            self.extract = self.element.text
            if self.extract is not None:
                self.extract = Manipulate().RemoveLargeEmos(self.extract)
        print("Extracted text:", self.extract)
        return self.extract


    def ExtractAttribute(self, attribute):
        try:
            if self.element is not None:
                self.extract = self.element.get_attribute(attribute)
            print("Extracted attribute:", self.extract)
            return self.extract
        except Exception as e:
            print(e)
            return None



    def ExtractElementAttribute(self, attribute, xpath=None):

        if xpath is not None:
            self.xpath = xpath
        self.ExtractElement(self.xpath)
        self.ExtractAttribute(attribute)
        return self.extract


    def ExtractElementToNumber(self, xpath=None):

        if xpath is not None:
            self.xpath = xpath
        self.ExtractElementText(self.xpath)
        self.extract = Enumerate().ReformToNumber(self.extract)
        return self.extract


    def ActivateKeywordsEverywhere(self):

        keywords_everywhere_options_path = "chrome-extension://hbapdpeemoojbophdfndmlgdhppljgmp/html/options.html"
        self.Load(keywords_everywhere_options_path)
        API_key_text_box = self.ExtractElement("//input[contains(@id, 'apiKey')]")
        API_key_text_box.send_keys("3d0ecbbfbba59de3f447")
        API_key_text_box.send_keys(Keys.ENTER)

        self.Load("https://www.google.com/")
        self.Driver.switch_to.window(self.Driver.window_handles[-1])
        self.Driver.close()
        self.Driver.switch_to.window(self.Driver.window_handles[-1])

    def ClearTextBox(self, element):

        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)

    def InsertClearedTextBox(self, element, text):

        self.ClearTextBox(element)
        element.send_keys(text)

    def inputClearedTextBox(self, element, text):

        self.InsertClearedTextBox(element, text)
        element.send_keys(Keys.ENTER)

    def scrollDown(self, numberOfScrollDowns):
        #self.Driver.execute_script("window.scrollTo(0, 520);")
        body = self.Driver.find_element_by_tag_name("body")
        while numberOfScrollDowns>= 0:
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)
            numberOfScrollDowns -= 1
    def scrollUp(self, numberOfScrollUps):
        #self.Driver.execute_script("window.scrollTo(0, 520);")
        body = self.Driver.find_element_by_tag_name("body")
        while numberOfScrollUps>= 0:
            time.sleep(0.5)
            body.send_keys(Keys.PAGE_UP)
            numberOfScrollUps -= 1
    def scrollDown1(self):
        #self.Driver.execute_script("window.scrollTo(0, 520);")
        self.Driver.execute_script("window.scrollTo(0, (document.body.scrollHeight)4);")
    def scrollDown2(self):
        #self.Driver.execute_script("window.scrollTo(0, 520);")
        self.Driver.execute_script("window.scrollTo(0, (document.body.scrollHeight)/2);")
    def scrollDown3(self):
        #self.Driver.execute_script("window.scrollTo(0, 520);")
        self.Driver.execute_script("window.scrollTo(0, (document.body.scrollHeight)*2/3);")

    def clear_cache(self):
        self.Driver.delete_all_cookies()

    def ForwardPage(self):
        self.Driver.forward()
