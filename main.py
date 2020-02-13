import discord
import pickle
import urlextract

extractor = urlextract.URLExtract()

token = "" #your discord user token
my_id = 0 #your discord user id

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
		
		elif message.content == "!help":
			await message.channel.send('''
!list_servers - Lists all servers you are on, and their bot-assigned ID.
!list_channels id - List all channels on server 'id'. Example '!list_channels 5' lists all channels on server 5.
!list_registered - Lists all registered output and input channels.
!register_output server_id channel_id - Registers a channel for output. Only send output to your own private server.
!register_input server_id channel_id - Registers a channel for input.
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
				await message.channel.send(str(c)+"%s@%s"%(channel.name, server.name))
				c+=1
			
			await message.channel.send("\nInput channels:")
			c=0
			for registered_input_channel in registry["input"]:
				server=client.get_guild(registered_input_channel[0])
				channel=server.get_channel(registered_input_channel[1])
				await message.channel.send(str(c)+"%s@%s"%(channel.name, server.name))
				c+=1
		
			await message.channel.send("---")
		
		elif message.content.startswith("!register"):
			try:
				command, guild, channel=message.content.split(" ")
				guild=client.guilds[int(guild)]
				channel=guild.channels[int(channel)]

				if command == "!register_output":
					registry["output"].append([guild.id, channel.id])

					registry_file = open("registry.pickle", "wb")
					pickle.dump(registry, registry_file)
					registry_file.close()

					await message.channel.send("Registered this channel as output channel.")

				elif command == "!register_input":
					registry["input"].append([guild.id, channel.id])

					registry_file = open("registry.pickle", "wb")
					pickle.dump(registry, registry_file)
					registry_file.close()

					await message.channel.send("Registered %s@%s as input channel."%(channel.name, guild.name))
				
			except ValueError:
				await message.channel.send("Insufficient arguments")

	if message.guild.id in [channel[0] for channel in registry["input"]] and message.channel.id in [channel[1] for channel in registry["input"]]:
		if len(message.attachments) > 0:
			url=message.attachments[0].url
			
			for registered_output_channel in registry["output"]:
				guild=client.get_guild(registered_output_channel[0])
				channel=guild.get_channel(registered_output_channel[1])

				image=discord.Embed()
				image.set_image(url=url)
				await channel.send("%s@%s: %s"%(message.channel.name, message.guild.name, message.author.display_name), embed=image)

		else:
			urls = extractor.find_urls(message.content)
			
			if len(urls)>0:
				for registered_output_channel in registry["output"]:
					guild=client.get_guild(registered_output_channel[0])
					channel=guild.get_channel(registered_output_channel[1])
				
					await channel.send("%s@%s: %s - %s"%(message.channel.name, message.guild.name, message.author.display_name, urls[0]))

client.run(token, bot=False)
