import random
import re

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
        
    print("Msg:\n" + msg)
    msg = cleanup_message(msg) #Not required, but highly recommended.

    #Do fancy things with message here

    #Your implementation is up to you. This is how we set it up but you can change it
    msg_bits = msg.split(" ")
    command = msg_bits[0].lower()

    #   This is defined here so values consisting of handler fuctions can be defined, but depending on the type of bot
    #   you wish to make you may not need it at all and instead opt for a different system. We highly recommend this
    #   though, as everything else can be handled from a function. The only real case you wouldn't want this is if
    #   you had thousands of commands.
    #
    #   It is not a bad idea for more computationally challenging functions to use AWS Lambda calls.

    commands = {
        "help": """/md Hello! I'm a prototype bot for Amazon Chime and my owner really should change this message! I'm a work in progress, so please report any bugs to my dev!
My current commands are:
* Help: brings up this menu"""
        #Additional commands can go here
    }

    # Handling commands which aren't defined.
    if command in commands:
        try:
            return commands[command]
        except Exception as e:
            print(e)
            return "I'm sorry, I threw an error just now. Not your fault. Try again or just give up honestly."
    else:
        return "/md I'm sorry, but I don't know what you want from me. Try \"@BotName help\""

    print("sending" + msg)
    return msg

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
    #If message meant for bot:

    #respond to messages here

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
