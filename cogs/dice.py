import os
import random
import disnake
from disnake import File
from disnake.ext import commands
from logs import logger


def get_basketball_result(roll: int) -> str:
    return "1" if roll >= 4 else "0"


GAME_CONFIG = {
    "🎯": {"name": "dart", "folder": "dart", "min_roll": 0, "max_roll": 5},
    "🎲": {"name": "dice", "folder": "dice", "min_roll": 1, "max_roll": 6},
    "🎳": {"name": "bowling", "folder": "bowling", "min_roll": 1, "max_roll": 6},
    "⚽": {"name": "soccer", "folder": "soccer-ball", "min_roll": 1, "max_roll": 5},
    "🏀": {"name": "basketball", "folder": "basketball", "min_roll": 1, "max_roll": 5},
}


class DiceCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._register_commands()

    def _register_commands(self):
        for emoji, cfg in GAME_CONFIG.items():
            def create_command(config):
                async def command_func(inter: disnake.ApplicationCommandInteraction):
                    await inter.response.send_message(
                        file=self.get_image(config, inter.user.name)
                    )

                return command_func

            cmd = commands.InvokableSlashCommand(
                func=create_command(cfg),
                name=cfg["name"],
                description=f"Roll for a {cfg['name']}",
                install_types=disnake.ApplicationInstallTypes(guild=True, user=True),
                contexts=disnake.InteractionContextTypes(guild=True, bot_dm=True, private_channel=True)
            )
            self.bot.add_slash_command(cmd)

    async def get_or_create_webhook(self, channel: disnake.TextChannel) -> disnake.Webhook | None:
        try:
            webhooks = await channel.webhooks()
            webhook_name = os.getenv("WEBHOOK_NAME", "tellagram")
            existing = disnake.utils.get(webhooks, name=webhook_name)
            if existing:
                return existing
            return await channel.create_webhook(name=webhook_name)
        except (disnake.Forbidden, disnake.HTTPException):
            return None

    def get_image(self, config: dict, username: str = "Someone"):
        roll = random.randint(config.get("min_roll", 0), config["max_roll"])

        # logic_func is applied if it exists in the config
        if "logic" in config:
            filename = config["logic"](roll)
        else:
            filename = str(roll)

        logger.debug(
            f"{username} rolled a {config['folder']} and got a {'bullseye!' if roll == config['max_roll'] and config['folder'] == 'dart' else roll}")
        return File(f"assets/{config['folder']}/{filename}.webp")

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot or not message.guild or message.content not in GAME_CONFIG:
            return

        cfg = GAME_CONFIG[message.content]
        webhook = await self.get_or_create_webhook(message.channel)
        if webhook is None:
            return

        logger.debug(f"{message.author.name} sent a {message.content}")
        saved = message
        await message.delete()
        await webhook.send(
            username=saved.author.display_name,
            avatar_url=saved.author.display_avatar.url,
            file=self.get_image(cfg, message.author.name)
        )


def setup(bot: commands.Bot):
    bot.add_cog(DiceCog(bot))