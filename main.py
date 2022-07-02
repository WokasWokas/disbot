from parser.setting_parser import Parser
from parser.args_parser import parse_args
from discord.ext import commands
from logger.log import Logger
import discord

client = commands.Bot(command_prefix="!")

def init_logger(cl: int) -> Logger:
    logger = Logger(cl)
    return logger

def close_logger() -> None:
    logger.save_log()

def init_settings_parser() -> dict[str, str]:
    setparser = Parser()
    logger.update_log('info', 'Init settings parser', __name__)
    return setparser
        
def create_embed_on_connection(user: discord.User) -> discord.Embed:
    embed=discord.Embed()
    embed.add_field(name=user.nick, value=user.avatar, inline=True)
    return embed

def create_embed_on_wrong_command(user: discord.Member, command: str) -> discord.Embed:
    embed = discord.Embed()
    embed.add_field(name=user.display_name, value=user.desktop_status, inline=True)
    embed.add_field(name=client.user.name, value=f'Not enough arguments for command {command}', inline=True)
    return embed

@client.event
async def on_ready():
    logger.update_log('info', f'Bot started with name {client.user.name}', 'bot')

@client.event
async def on_disconnect():
    logger.update_log('info', f'Bot closed', 'bot')
    close_logger()

@client.event
async def on_member_join(Member: discord.Member):
    logger.update_log('info', 'Connected to the server', Member.nick)
    channel = client.get_channel(876918408590000188)
    await channel.send(create_embed_on_connection(Member))

@client.event
async def on_error(event: str) -> None:
    logger.update_log('error', f'Error {event}', 'bot')

@client.event
async def on_message(message: discord.Message):
    if message.author.display_name == client.user.name:
        return 
    elif message.content.startswith('$'):
        command = message.content[1:].split(' ')
        if command[0] == "test":
            if len(command) < 2:
                logger.update_log('warn', f'Not enough arguments for command {command[0]}', message.author.nick)
                await message.author.send(embed=create_embed_on_wrong_command(message.author, command[0]))
                return
            await message.channel.send(f'Function test was called with arguments {command[1:]}')
        else:
            logger.update_log('warn', f'Unknown command {command[0]}', message.author.nick)
    else:
        logger.update_log('info', f'{message.author} send message', f'ch-{message.channel.name}')

def apply_settings_to_logger(settings: dict[str, str]) -> None:
    if logger.filename != settings['filename']:
        logger.set_filename(settings['filename'])
    
    if logger.log_path != settings['log_path']:
        logger.set_log_path(settings['log_path'])
    
    if logger.loglevel != settings['loglevel']:
        logger.set_loglevel(settings['loglevel'])
    
    if logger.timeformat != settings['timeformat']:
        logger.set_timeformat(settings['timeformat'])

def main() -> None:
    logger.update_log('info', 'Getting token from settings', __name__)
    token = settings['token']

    logger.update_log('info', 'Starting discord bot', __name__)

    client.run(token)

if __name__ == "__main__":
    try:
        consolelog = 0 if ('cl', 0) in parse_args() else 1

        global logger, settings
        logger = init_logger(consolelog)

        logger.update_log('info', 'Initialization settings parser', __name__)
        settings_parser = init_settings_parser()
    
        logger.update_log('info', 'Getting settings', __name__)
        settings = settings_parser.get_settings()

        apply_settings_to_logger(settings)

        main()

        close_logger()
    except Exception as error:
        crash_log = init_logger()
        crash_log.set_log_path('crashs')
        crash_log.update_log("error", error)
        crash_log.save_log()
