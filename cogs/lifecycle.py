import disnake
from disnake.ext import commands

from logs import logger


class LifecycleCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        logger.success(f"Logged in as {self.bot.user}!")


def setup(bot: commands.Bot):
    bot.add_cog(LifecycleCog(bot))