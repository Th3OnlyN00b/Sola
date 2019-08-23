#Custom wait class
class status_changed(object):
    
    def __init__(self, driver):
        self.driver = driver

    def __call__(self, driver):
        card_list = self.driver.find_element_by_class_name("CardList__items").find_elements_by_class_name("Card")
        return (len(card_list) != 0)
