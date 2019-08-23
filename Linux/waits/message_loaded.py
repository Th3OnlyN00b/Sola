#Custom wait class
class message_loaded(object):
    
    def __init__(self, message_list, prev_msg_ID):
        self.message_list = message_list
        self.prev_msg_ID = prev_msg_ID

    def __call__(self, driver):
        messages = self.message_list.find_elements_by_class_name("ChatMessageList__messageContainer")
        if len(messages) == 0:
            return False
        message_text = messages[-1].get_attribute('innerHTML')
        if message_text == None:
            return False
        message_pieces = message_text.split("\"")
        if message_pieces[1] == "TypingIndicator":
            return False
        return (self.prev_msg_ID != message_pieces[1])
