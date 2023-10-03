import discord

class PermissionNotFound(discord.DiscordException):
    pass


class NotGuildChannel(discord.DiscordException):
    pass


class NotDMChannel(discord.DiscordException):
    pass
