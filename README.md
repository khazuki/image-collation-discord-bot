This is the Image Collation Bot for Discord. This bot allows you to register "input" channels, and then reposts all attachments (images, videos, etc) and links to any registered "output" channels. This is useful if you are using several discord servers as image feeds, and want all of them collected in one place.

This is a "self bot", meaning it runs on your own account, rather than on a bot account, which is against Discord TOS. If you get reported for using it, your account will be banned. However, if you set this bot to only post to a channel on your own private server, it will go entirely unnoticed.

You need python and pip installed to use this bot. You also need to be able to find your discord id and user token.

Run setup.py to install the required libraries.

Then run bot.py to start the bot.

Because the bot is subject to discord traffic limits, the bot will frequently pause will printing lists of servers/channels/etc. Every list ends with "---"

"!list_servers" will list all discord servers you are on, with an id number for each.

"!list_channels id" will list all channels for the server with that id, with an id number for each.

"!register_input serverid channelid" will register the chosen channel for input.

"!register_output serverid channelid" will register the chosen channel for output. All attachments and links from all input channels will be reposted to all output channels.

"!list_registered" lists all output and input channels you have registered, with an id number for each.

"!unregister output id"/"!unregister input id" unregisters the chosen channel.

"!icb_test" will send "ICB test received" via your account if the bot is running correctly.

"!icb_help" gives you this same information.

"!icb_exit" shuts down the bot.
