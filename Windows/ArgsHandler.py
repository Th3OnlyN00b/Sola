import json
from SecretGrabber import get_secret

def handle_arg_error(msg):
        print(msg)
        print("Run 'Sola.py help' if needed.")
        quit()

def args_handler(arguments):
    #User ran 'Sola help'
    if (len(arguments) == 2) and (arguments[1].lower() == "help"):
        print("""This is the Luna bot framework for Amazon Chime. There are two methods to launch: 
        1) Using AWS Secrets Manager through boto3
        2) Entering the login info for the bot account manually.
        
    To launch using the first method, run 'Luna.py headless=[1|0] browser=[chrome|firefox] bot_name=[bot name] secret_name=[secret_name] region=[region]'.
    Your secret (the one referenced by secret_name) MUST be in the format: 
        email: [bot login email]
        password: [bot login password]
        
    To launch using the second method, run 'Luna.py headless=[1|0] browser=[chrome|firefox] bot_name=[bot name] email=[bot login email] pass=[bot login password]'

    botname should be the name the bot has in chime, as it would look if someone were to @ your bot.""")
        quit()

    using_pass = True

    if len(arguments) < 5:
        handle_arg_error("Required arguments missing. You must run 'Sola headless=[1|0] browser=[chrome|firefox] [email|secret_name]=[account email] [pass|region]=[account password] (dev=[1|0])'")
    elif len(arguments) > 6:
        handle_arg_error("Too many arguments. You must run 'Sola headless=[1|0] browser=[chrome|firefox] [email|secret_name]=[account email] [pass|region]=[account password]'")
    elif (arguments[1] != ('headless='+str(1))) and (arguments[1] != ('headless='+str(0))):
        handle_arg_error("Headless option must be specified as 1 for true and 0 for false. You specified: " + arguments[1])
    elif (arguments[2].lower() != "browser=chrome") and (arguments[2].lower() != "browser=firefox"):
        handle_arg_error("browser option must be either 'chrome' for Google Chrome or 'firefox' for Mozilla Firefox")
    arg4 = arguments[3].split("=")
    if(len(arg4) < 2):
        handle_arg_error("email/secret_name must be defined.")
    if (arg4[0].lower() != "email") and (arg4[0].lower() != "secret_name"):
        handle_arg_error("You must have either 'email' or 'secret_name' defined, such as email=[email] or secret_name=[secret name].")
    arg5 = arguments[4].split("=")
    if(len(arg5) < 2):
        handle_arg_error("pass/region must be defined.")
    elif (arg5[0].lower() != "pass") and (arg5[0].lower() != "region"):
        handle_arg_error("You must have either 'pass' or 'region' defined, such as pass=[password] or region=[region].")
    dev = False
    if(len(arguments) > 5) and (arguments[5].split('=')[0] == "dev"):
        arg6=arguments[5].split('=')
        if (len(arg6)>1) and (str(arg6[1]) == '1'):
            dev = True
            print("Developer mode engaged!")

    if arg4[0].lower() == "email":
        if arg5[0].lower() != "pass":
            handle_arg_error("If using email/password login you must have the arguments 'email' and 'pass' defined.")
    else:
        if arg5[0].lower() != "region":
            handle_arg_error("If using secrets login you must have the arguments 'secret_name' and 'region' defined.")
        using_pass = False

    email_or_secret = arg4[1]
    pass_or_region = arg5[1]

    print("Args Verified!")


    # Grab important info from args
    email = ""
    password = ""

    if not using_pass:
        print("Logging in without a password")
        login_info = json.loads(get_secret(email_or_secret, pass_or_region))
        email = login_info["email"]
        password = login_info["password"]
    else:
        print("Logging in with pasword")
        email = email_or_secret
        password = pass_or_region

    return {"email": email, "password": password, "dev": dev}

