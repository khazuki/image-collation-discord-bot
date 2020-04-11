while True:
	answer = input("Will this be a self-bot, running on your personal account (this is against Discord TOS)? y/n\n")

	if answer.startswith("y"):
		selfbot = True
		break

	elif answer.startswith("n"):
		selfbot = False
		break

if selfbot:
	secret = input("Input your account's secret.")
else:
	secret = input("Input your bot's secret (available in the discord developer portal):\n")

owner_id = input("Input your discord id, used to identify you as the bot's owner:\n")
bot_testing_guild_id = input("Input the id of the server you will use for testing your bot:\n")
bot_testing_channel_id = input("Input the id of the channel you will use for testing your bot:\n")
prefix = input("Input the prefix your bot will use for its commands:\n")

f=open("auth.py", "w")
f.write("secret = '%s'\nowner_id = %d\nbot_testing_guild_id = %d\nbot_testing_channel_id = %d\nprefix = '%s'\nselfbot = %s"%(secret, int(owner_id), int(bot_testing_guild_id), int(bot_testing_channel_id), prefix, str(selfbot)))
f.close()

input("Setup complete. Run main.pyw to start the bot. Hit enter to close this window.")
