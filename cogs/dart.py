import random

import disnake
from disnake.ext import commands

from logs import logger


class DartCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="dart")
    @commands.install_types(guild=True, user=True)
    @commands.contexts(guild=True, bot_dm=True, private_channel=True)
    async def dart(
        self, inter: disnake.ApplicationCommandInteraction
    ):
        roll = random.randint(0, 5)
        logger.debug(f"{inter.user.name} rolled a {'bullseye!' if roll == 5 else roll}")
        await inter.response.send_message("dart")


def setup(bot: commands.Bot):
    bot.add_cog(DartCog(bot))