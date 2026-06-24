import os

import disnake
from disnake.ext import commands
from dotenv import load_dotenv

from logs import logger

intents = disnake.Intents.default()
intents.message_content = True

bot = commands.InteractionBot(intents=intents)

EXTENSIONS = (
    "cogs.lifecycle",
    "cogs.dice",
)

def load_extensions() -> None:
    for ext in EXTENSIONS:
        try:
            bot.load_extension(ext)
        except Exception as e:
            logger.error(f"Failed to load extension {ext}.")
            raise


def main():
    load_extensions()
    load_dotenv()
    bot.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()