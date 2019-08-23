#Custom wait class
class can_find_css(object):
    
    def __init__(self, driver, class_to_find):
        self.driver = driver
        self.class_to_find = class_to_find

    def __call__(self, driver):
        try:
            self.driver.find_element_by_css_selector(self.class_to_find)
            return True
        except:
            return False
