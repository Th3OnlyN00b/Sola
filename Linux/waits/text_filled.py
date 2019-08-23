#Custom wait class
class text_filled(object):
    
    def __init__(self, text_box, text_to_type):
        self.text_box = text_box
        self.text_to_type = text_to_type

    def __call__(self, text_box):
        try:
            return self.text_box.get_attribute("innerHTML") == self.text_to_type 
        except:
            return False
