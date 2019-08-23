import random
import re
import constants
import _thread
import time
import json
import requests
import sys

###########################################################################################
#   This is the file you should edit. The two methods below are the only required methods,#
#   and this first one must return the string which the bot is supposed to say based on   #
#   the given input.                                                                      #
#                                                                                         #
#   The args for both functions are as follows:                                           # 
#       msg: the message recieved by the bot.                                             #
#       bot_name: the bot's name (for convenience)                                        #
#       message_sender: this is a function which you can call on a string to have your    #
#           bot send that message. This is used to respond to async calls, such as calls  #
#           to AWS Lambda functions.                                                      #
#                                                                                         #
#   We've included a cleanup_message() function for you which removes any strange things  #
#   left over from Chime's strangeness. It is not required, but highly recommended.       #
#                                                                                         #
#   To launch your bot, run 'py Luna [args]'. Run 'py Luna help' for additional info.     #
#   Please report any framework bugs to smthcol@. Make sure they are framework bugs,      #
#   as I will not debug your bot for you.                                                 #
#                                                                                         #
#   Go have fun and make some bots!                                                       #
###########################################################################################

def process_message(msg, bot_name, message_sender):
    return ""

###########################################################################################
#   This is the second function you can edit. This function is to allow responses to non- #
#   @ messages, such as "hello!"                                                          #
#                                                                                         #
#   This function is slightly different than the last, where whatever your returned would #
#   be sent by the bot. In this function, if you do not desire to send a message, return  #
#   the empty string (""). If you don't, your bot will respond to every single message    #
#   sent in the chat.                                                                     #
###########################################################################################

def process_raw(msg, bot_name, message_sender):
    bits = msg.split(" ")
    #If message meant for bot:
    if bits[0].lower() == "@timer":
        webhook_timer_helper(bits, msg)
    #respond to messages here
    elif (re.match(r'^(?=.*e?c?n?e?ce?d)([b-l]|n|r|[t-v]){41,44}', msg) and (len(msg) > 40) and (len(msg) < 45)):
        send_webhook_msg("#YubikeyReactsOnly")
    #Message not meant for Bot
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
def send_webhook_msg(msg):
    try:
        response = requests.post(
            url="http://MyWebhookURLHere",
            json={"Content": msg})
    except:
        pass

def webhook_print_time(delay, msg):
    time.sleep(delay)
    if msg == "":
        send_webhook_msg("Timer complete!")
    else:
        send_webhook_msg(msg)

def webhook_timer_helper(bits, msg):
    secs = 0
    if len(bits) < 2:
        send_webhook_msg("I need a number of seconds to set the timer!")
    try:
        mult = 0
        if bits[1][-1] =='s':
            mult = 1
        elif bits[1][-1] == 'm':
            mult = 60
        elif bits[1][-1] == 'h':
            mult = 60*60
        if mult == 0:
            secs = int(bits[1])
        else:
            secs = mult*int(bits[1][:-1]) # Parse out the 's'/'m'/'h'
        if secs < 0:
            send_webhook_msg("I can't time negative amounts")
        if len(bits) > 2:
            _thread.start_new_thread(webhook_print_time, (secs, msg[len("timer ")+len(bits[1])+2:]))
        else:
            _thread.start_new_thread(webhook_print_time, (secs, ""))
    except:
        send_webhook_msg("I couldn't set the timer, sorry! Make sure you're using a real integer")

    send_webhook_msg("Timer set for " + str(secs) + " seconds!")

    