import random
import re
import json
import requests
import smtplib
import threading

###########################################################################################
#   This is the file you should edit. The three methods below are the only required       #
#   methods, and they must all return the string you want to respond to a message with.   #
#                                                                                         #
#   The args for all functions are as follows:                                            # 
#       name: the name of the person (personal) or group (group) who messaged you.        #
#       link: the link to the user chat or group. This is useful because it contains a    #
#           unique ID which you can use to respond to specific groups or people in unique #
#           ways, or not at all. It can also be used to send links to the conversation    #
#           through something like text if you choose to set that up.                     #
#       message_text: the text of the message sent. Not always accurate due to the delay. #
#           Will hold the value "Unknown" if Sola is not able to determine the message.   #
#       message_author: The Chime name of the Chime user who sent the message. Will hold  #
#           the value "Unknown" if Sola is not able to determine who sent the message.    #
#       message_author_email: The email of the Chime user who send the message. Will hold #
#           the value "Unknown" if Sola is not able to determine who sent the message.    #
#       message_sender: this is a function which you can call on a string to have your    #
#           bot send that message. This is used to respond to async calls, such as calls  #
#           to AWS Lambda functions.                                                      #
#                                                                                         #
#   We've included a cleanup_message() function for you which removes any strange things  #
#   left over from Chime's strangeness. It is not required, but highly recommended.       #
#                                                                                         #
#   To launch your bot, run 'py Sola [args]'. Run 'py Sola help' for additional info.     #
#   Please report any framework bugs to smthcol@.                                         #
#                                                                                         #
#   Go have fun and enjoy your lunch in peace!                                            #
###########################################################################################

def process_message_personal(name, link, message_text, message_author, message_author_email, message_sender):
    author_bits = message_author.split(",")
    author = author_bits[0]
    if len(author_bits) > 1:
        author = author_bits[1]
    msg_to_send = ("\nYou have recieved a chime message from " + message_author + " (" + message_author_email + "): " + cleanup_message(message_text))
    thread = threading.Thread(target=text_message, args=(msg_to_send,), daemon=True)
    thread.start()
    return "/md Hi " + author + ", I am sorry to say I am out of the office right now. I saw your message:\n>" + quote(cleanup_message(message_text)) + "\n\nand I'll email you at " + message_author_email + " when I get back."

###########################################################################################
#   This is the second function you can edit. This function responds to group messages.   #
#                                                                                         #
#   Note that this function is called only when you are specifically @ed, and will not    #
#   run for normal messages in a group chat. For that functionality see the below         #
#   function: process_message_group_no_at()                                               #
###########################################################################################

def process_message_group(name, link, message_text, message_author, message_author_email, message_sender):
    author_bits = message_author.split(",")
    author = author_bits[0]
    if len(author_bits) > 1:
        author = author_bits[1]
    msg_to_send = ("\nYou have recieved a chime message from " + message_author + " (" + message_author_email + "): " + cleanup_message(message_text))
    thread = threading.Thread(target=text_message, args=(msg_to_send,), daemon=True)
    thread.start()
    return "/md Hi " + author + ", I am sorry to say I am out of the office right now. I saw your message:\n>" + quote(cleanup_message(message_text)) + "\n\nand I'll email you at " + message_author_email + " when I get back."

###########################################################################################
#   This is the third function you can edit. This function responds to group messages     #
#   even when you are not @ed.                                                            #
#                                                                                         #
#   Note: This is VERY dangerous, as it can easily result in heavy spam to group chats    #
#   and make you public enemy #1 at work. I HIGHLY recommend never returning anything but #
#   the empty string, and instead using this function to do something like log the groups #
#   whose messages you missed, or text you links to chats with high activity, or          #
#   something that doesn't require a response.                                            #
###########################################################################################

def process_message_group_no_at(name, link, message_text, message_author, message_author_email, message_sender):
    print("I was called")
    return ""


def cleanup_message(msg):
    #Fix hyperlink html garbage 
    msg = re.sub(r'<a href=".*" target="_blank" rel="noopener noreferrer">', '', msg)
    msg = re.sub(r'</a>', '', msg)

    #Fix emoji html garbage
    msg = re.sub(r'<span class="Emoji" style="background-position: \S*% \S*%; background-size: \S*% auto; background-image: url\(\S*\);">','',msg)
    msg = re.sub(r'</span>', '', msg)

    #Fix mention garbage
    msg = re.sub(r'<span class="AtMention AtMention__Messageable">','',msg)
    msg = re.sub(r'<span class="AtMention">','',msg)

    #Fix any other potential garbage
    msg = re.sub(r'<.*>','',msg) #Reminder that typed characters '<' and '>' show up as '&lt;' and '&gt;' and therefore aren't affected here.
    return msg

########### Helper functions here ###################
def text_message(msg_to_send):
    print("I'm being called!")
    gmail_user = 'myemail@myemail.com'
    gmail_password = 'myP@ssw0rd'

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
    except Exception as e:
        print("Could not send email:")
        print(e)
    chunk_size = 100
    msgs = [ msg_to_send[i:i+chunk_size] for i in range(0, len(msg_to_send), chunk_size) ]
    for msg in msgs:
        # vtext.com is for verison. Check your carrier here https://en.wikipedia.org/wiki/SMS_gateway
        server.sendmail(gmail_user, "MyPhoneNumber@vtext.com", msg)
        print("sent " + msg)

def quote(msg):
    a = msg.split("\n")
    op = "\n>"
    return op.join(a)