import os
import random
import re

import disnake
from disnake import File
from disnake.ext import commands

from logs import logger


class DartCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def get_or_create_webhook(self, channel: disnake.TextChannel) -> disnake.Webhook | None:
        """Retrieve the webhook for a given channel, creating it if it doesn't exist."""
        try:
            webhooks = await channel.webhooks()
            webhook_name = os.getenv("WEBHOOK_NAME", "tellagram")

            try:
                existing = disnake.utils.get(webhooks, name=webhook_name)
                if existing:
                    return existing
            except disnake.NotFound:
                pass

            return await channel.create_webhook(name=webhook_name)
        except (disnake.Forbidden, disnake.HTTPException):
            return None

    def get_dart_image(self, username: str = "Someone"):
        roll = random.randint(0, 5)
        logger.debug(f"{username} rolled a {'bullseye!' if roll == 5 else roll}")
        return File(f"assets/dart/{roll}.webp")

    @commands.slash_command(name="dart")
    @commands.install_types(guild=True, user=True)
    @commands.contexts(guild=True, bot_dm=True, private_channel=True)
    async def dart(
            self, inter: disnake.ApplicationCommandInteraction
    ):
        await inter.response.send_message(file=self.get_dart_image(inter.user.name))

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot or not message.guild:
            return

        webhook = await self.get_or_create_webhook(message.channel)
        if webhook is None:
            logger.warning(f"Failed to get or create webhook in #{message.channel.name}")
            return

        if message.content == "🎯":
            logger.debug(f"{message.author.name} sent a 🎯")
            saved = message
            await message.delete()
            await webhook.send(
                username=saved.author.display_name,
                avatar_url=saved.author.display_avatar.url,
                file=self.get_dart_image(message.author.name)
            )


def setup(bot: commands.Bot):
    bot.add_cog(DartCog(bot))