import random
import re
import json
import requests
import sys

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
    return "This is my out-of-office message to people who DM me!"

###########################################################################################
#   This is the second function you can edit. This function responds to group messages.   #
#                                                                                         #
#   Note that this function is called only when you are specifically @ed, and will not    #
#   run for normal messages in a group chat. For that functionality see the below         #
#   function: process_message_group_no_at()                                               #
###########################################################################################

def process_message_group(name, link, message_text, message_author, message_author_email, message_sender):
    return "This is my out-of-office message to groups who @me!"

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


    