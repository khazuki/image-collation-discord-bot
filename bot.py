import discord
import pickle
import urlextract

extractor = urlextract.URLExtract()

try:
	from auth import token, my_id
except:
	input("Missing auth.py file. Run setup.py. Hit enter to close this window.")
	exit()

try:
	registry_file = open("registry.pickle", "rb")
	registry = pickle.load(registry_file)
	registry_file.close()
except:
	registry_file = open("registry.pickle", "wb")
	registry = {"output":[], "input":[]}
	pickle.dump(registry, registry_file)
	registry_file.close()

client = discord.Client()

@client.event
async def on_message(message):
	if message.author.bot:
		return

	if message.author.id == my_id:
		if message.content == "!icb_test":
			await message.channel.send("ICB test received")
		
		elif message.content == "!icb_exit":
			await message.channel.send("ICB exiting")
			exit()
		
		elif message.content == "!icb_help":
			await message.channel.send('''
"!list_servers" will list all discord servers you are on, with an id number for each.
"!list_channels id" will list all channels for the server with that id, with an id number for each.
"!register_input serverid channelid" will register the chosen channel for input.
"!register_output serverid channelid" will register the chosen channel for output. All attachments and links from all input channels will be reposted to all output channels.
"!list_registered" lists all output and input channels you have registered, with an id number for each.
"!unregister output id"/"!unregister input id" unregisters the chosen channel.
"!icb_test" will send "ICB test received" via your account if the bot is running correctly.
"!icb_help" gives you this same information.
"!icb_exit" shuts down the bot.
			''')
		
		elif message.content == "!list_servers":
			c=0
			for guild in client.guilds:
				await message.channel.send(str(c)+": "+guild.name)
				c+=1
				
			await message.channel.send("---")
		
		elif message.content.startswith("!list_channels"):
			try:
				command, argument=message.content.split(" ")
				guild = client.guilds[int(argument)]

				c=0
				for channel in guild.channels:
					if str(channel.type) == "text":
						await message.channel.send(str(c)+": "+channel.name)
					c+=1

				await message.channel.send("---")

			except ValueError:
				await message.channel.send("Insufficient arguments")
		
		elif message.content == ("!list_registered"):
			await message.channel.send("Output channels:")
			c=0
			for registered_output_channel in registry["output"]:
				server=client.get_guild(registered_output_channel[0])
				channel=server.get_channel(registered_output_channel[1])
				await message.channel.send(str(c)+": %s@%s"%(channel.name, server.name))
				c+=1
			
			await message.channel.send("\nInput channels:")
			c=0
			for registered_input_channel in registry["input"]:
				server=client.get_guild(registered_input_channel[0])
				channel=server.get_channel(registered_input_channel[1])
				await message.channel.send(str(c)+": %s@%s"%(channel.name, server.name))
				c+=1
		
			await message.channel.send("---")
		
		elif message.content.startswith("!register"):
			try:
				command, guild, channel=message.content.split(" ")
				guild=client.guilds[int(guild)]
				channel=guild.channels[int(channel)]

				if command == "!register_output":
					for registered_channel in registry["input"]:
						if guild.id == registered_channel[0] and channel.id == registered_channel[1]:
							await message.channel.send("Cannot register an input channel for output. Would destroy the Earth.")
							break
					else:
						for registered_channel in registry["output"]:
							if guild.id == registered_channel[0] and channel.id == registered_channel[1]:
								await message.channel.send("%s@%s is already a registered output channel."%(channel.name, guild.name))
								break
						else:
							registry["output"].append([guild.id, channel.id])

							registry_file = open("registry.pickle", "wb")
							pickle.dump(registry, registry_file)
							registry_file.close()

							await message.channel.send("Registered %s@%s as output channel."%(channel.name, guild.name))

				elif command == "!register_input":
					for registered_channel in registry["output"]:
						if guild.id == registered_channel[0] and channel.id == registered_channel[1]:
							await message.channel.send("Cannot register an output channel for input. Would destroy the Earth.")
							break
					else:
						for registered_channel in registry["input"]:
							if guild.id == registered_channel[0] and channel.id == registered_channel[1]:
								await message.channel.send("%s@%s is already a registered input channel."%(channel.name, guild.name))
								break
						else:
							registry["input"].append([guild.id, channel.id])

							registry_file = open("registry.pickle", "wb")
							pickle.dump(registry, registry_file)
							registry_file.close()

							await message.channel.send("Registered %s@%s as input channel."%(channel.name, guild.name))
				
			except ValueError:
				await message.channel.send("Insufficient arguments")

		elif message.content.startswith("!unregister"):
			try:
				command, put, channel_id=message.content.split(" ")
				registered_channel=registry[put][int(channel_id)]
				
				guild=client.get_guild(registered_channel[0])
				channel=guild.get_channel(registered_channel[1])
				await message.channel.send("Removed %s@%s from registered %s channels"%(channel.name, guild.name, put))
				registry[put].pop(int(channel_id))

				registry_file = open("registry.pickle", "wb")
				pickle.dump(registry, registry_file)
				registry_file.close()
				
			except ValueError:
				await message.channel.send("Insufficient arguments")

	if message.guild.id in [channel[0] for channel in registry["input"]] and message.channel.id in [channel[1] for channel in registry["input"]]:
		#attachments
		if len(message.attachments) > 0:
			for registered_output_channel in registry["output"]:
				guild=client.get_guild(registered_output_channel[0])
				channel=guild.get_channel(registered_output_channel[1])

				await channel.send("%s@%s:%s - %s"%(message.author.name, message.guild.name, message.channel.name, message.jump_url), files=[await attachment.to_file() for attachment in message.attachments])

		#links
		else:
			urls = extractor.find_urls(message.content)
			
			if len(urls)>0:
				for registered_output_channel in registry["output"]:
					guild=client.get_guild(registered_output_channel[0])
					channel=guild.get_channel(registered_output_channel[1])

					await channel.send("%s@%s - %s (<%s>)\n%s"%(message.author.name, message.guild.name, message.channel.name, message.jump_url, "\n".join(urls)))

client.run(token, bot=False)
