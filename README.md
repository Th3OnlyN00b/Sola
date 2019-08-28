# Sola
Out of Office messaging tool for Amazon Chime

Written by smthcol@. Please ping with bugs or errors in documentation.

## So you would like to make your own bot? Simply follow the steps bellow:

Please note that this assumes you have:
* [Python 3.6](https://www.python.org/downloads/) or greater installed on your computer. It may work with lower versions of 3.x, but they are not officially supported.
* Firefox or Chrome installed **in their default directories**
* Pip (which should come with Python in >= 3.4, but you may have uninstalled it or something.

## 0. Download Sola:
* Download either the zip file for your OS, or clone the repo and open the folder for your OS.
* If you downloaded a zip file, unzip it and open the folder.
* This will be referenced as your **root folder**

## 4. Program your bot (Optional):
* Download or clone this framework into a file on your local or virtual or cloud machine.
* Create a file in the root folder for the project called "commands.py"
* Copy the content from "commands_template.py" into the newly created "commands.py"
* Modify "commands.py" to your heart's content.

## 6. Run your bot:
* You will need to add the geckodriver/chromedriver file to your system's path.
  - On Windows, search "path" into the windows search bar. Select "Edit the system environment variables" then "Environment Variables" then double click the line labeled "Path" on the top box. Select "add", then enter the file path to your root folder. Select "Ok" and close the windows.
  - On Unix, simply run `export PATH=$PATH:/path/to/root/folder/.` 
* Run `pip install -U selenium` to make sure you have the latest version of selenium
* Run `pip install Boto3` to make sure you have the latest version of Boto3
* Run `py Sola.py help` from the root folder for details on how to run your bot. If you're having an error saying "selenium not defined" or something, you've likely used pip from another python install (probably 2.X) and you'll need to use python 3's pip to install the previous two.
* You may be asked to enter a one-time password (especially if you are on a new AWS instance). This happens sometimes, just check the bot's email and enter the code. Sola will handle the rest.
* You might also be asked to copy a url into your browser and type the resultant captcha. This feature is currently broken. If you see this screen, wait a few hours and try again, the captcha will usually go away. If it doesn't (or you don't want to wait) simply open a browser and login manually from the computer you want to run the bot on. This will remove the captcha flag and you'll be able to run Sola normally. If you can't do that because you're on a slow computer, restart your router/ec2 instance (stop and start, in the latter case), this will give you a new IP and the captcha will go away. Sorry!

## 7. Have fun!
* Your bot should be running now. Enjoy yourself!

## Notes about running on AWS:
* If you're planning to make a bot persist using AWS, Sola itself can run on anything with more than one gig of ram such as a t2.small ubuntu or linux instance. You can also run it on a t2.micro (the same instance which is elegable for the free tier), but only for a short time (about 24-36 hours) because the browser builds a cache which knocks it over the 1gb ram limit. In programming your bot, it is good practice to not exceed 1.5 gigs in total (leaving 0.5 for your bot), and make any process heavy calls to AWS Lambda functions. For async calls such as those, be sure to make use of the `message_sender` function which is a param in both `process_raw` and `process_message`, unless you want to stall your bot until the function call completes.  

## TODO:
* Try to find a way to clear browser cache as to not use that much ram

## Updates: 
* Initial release

