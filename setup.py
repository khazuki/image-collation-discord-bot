import os

os.system('cmd /c "pip install discord urlextract"')

user_id=input("Input your Discord user id: ")
user_token=input("Input your Discord user token: ")

f=open("auth.py", "w")
f.write("my_id = %s\ntoken = '%s'"%(user_id, user_token))
f.close()

input("Setup complete. Run bot.py to start the bot. Hit enter to close this window.")
