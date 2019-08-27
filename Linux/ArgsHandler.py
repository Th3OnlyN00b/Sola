import json
from SecretGrabber import get_secret

def handle_arg_error(msg):
        print(msg)
        print("Run 'Sola.py help' if needed.")
        quit()

def args_handler(arguments):
    #User ran 'Sola help'
    if (len(arguments) == 2) and (arguments[1].lower() == "help"):
        print("""This is the Sola away messaging framework for Amazon Chime. There are two methods to launch: 
        1) Using AWS Secrets Manager through boto3
        2) Entering the login info for the bot account manually.
        
    To launch using the first method, run 'Luna.py headless=[1|0] browser=[chrome|firefox] bot_name=[bot name] secret_name=[secret_name] region=[region]'.
    Your secret (the one referenced by secret_name) MUST be in the format: 
        email: [bot login email]
        password: [bot login password]
        
    To launch using the second method, run '{botname} headless=[1|0] browser=[chrome|firefox] bot_name=[bot name] email=[bot login email] pass=[bot login password]'

    botname should be the name the bot has in chime, as it would look if someone were to @ your bot.""".format())
        quit()

    using_pass = True

    if len(arguments) < 5:
        handle_arg_error("Required arguments missing. You must run 'Sola headless=[1|0] browser=[chrome|firefox] [email|secret_name]=[account email] [pass|region]=[account password] (dev=[1|0]) (messsage=<Out of Office Message>)'")
    elif len(arguments) > 7:
        handle_arg_error("Too many arguments. You must run 'Sola headless=[1|0] browser=[chrome|firefox] [email|secret_name]=[account email] [pass|region]=[account password] (dev=[1|0]) (messsage=\"<Out of Office Message>\")'\nPlease note that your message must have quotes (\"\") surrounding it, such as: \"I am out of the office, sorry!\"")
    
    # Load all arguments into a dict to make life easy
    args = {}
    for arg in arguments[1:]:
        split_arg = arg.split("=")
        if len(split_arg) < 2:
            print("Cannot leave " + str(split_arg[0]) + " blank!")
            quit()
        args[split_arg[0].lower()] = split_arg[1]

    if "headless" not in args:
        handle_arg_error("'headless' option must be defined")
    if (args["headless"] != str(1)) and (args["headless"] != str(0)):
        handle_arg_error("'headless' option must be specified as 1 for true and 0 for false. You specified: " + args["headless"])
    
    if "browser" not in args:
        handle_arg_error("'browser' option must be defined")
    if (args["browser"].lower() != "chrome") and (args["browser"].lower() != "firefox"):
        handle_arg_error("'browser' option must be either 'chrome' for Google Chrome or 'firefox' for Mozilla Firefox")
    
    if ("email" not in args) and ("secret_name" not in args):
        handle_arg_error("'email' or 'secret_name' must be defined.")
    if ("email" in args) and ("secret_name" in args):
        handle_arg_error("Please choose to use either email/password login or secret_name/region login as both cannot be used.")
    if ("email" in args) and ("pass" not in args):
        handle_arg_error("If using email and password login, both 'email' and 'pass' must be defined.")
    if ("email" in args) and ("region" in args):
        handle_arg_error("'region' must be used only when using secret_name/region login. When using email/password, please only define 'email' and 'pass' for your credentials.")
    
    if ("secret_name" in args) and ("region" not in args):
        handle_arg_error("If using secret_name/region login, both 'secret_name' and 'region' must be defined")
    if ("secret_name" in args) and ("pass" in args):
        handle_arg_error("'pass' must be used only when using email/pass login. When using secret_name/region, please only define 'secret_name' and 'region' for your credentials.")
    
    dev = False
    if ("dev" in args) and (str(args["dev"]) == '1'):
        dev = True
        print("Developer mode engaged!")
    if "message" in args:
        print("Your out-of-office message is:")
        print(args["message"])


    
    if "email" not in args:
        using_pass = False

    email_or_secret = args["email"] if "email" in args else args["secret_name"] # For whatever stupid reason, Python rebukes decades of language development and makes a statement which is evaluated from the middle outwards, which is why this doesn't throw a KeyError
    pass_or_region = args["pass"] if "pass" in args else args["region"] # I really, really hate the fact that this works.

    print("Args Verified!")


    # Grab important info from args
    email = ""
    password = ""

    if not using_pass:
        print("Logging in without a password")
        login_info = json.loads(get_secret(email_or_secret, pass_or_region))
        args["email"] = login_info["email"]
        args["password"] = login_info["password"]
    else:
        print("Logging in with pasword")
        args["email"] = email_or_secret
        args["password"] = pass_or_region

    return args

