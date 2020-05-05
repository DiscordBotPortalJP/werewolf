import discord
import asyncio

colmn_reactions = [
    '\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}',
    '\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}',
    '\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}',
    '\N{DIGIT FOUR}\N{COMBINING ENCLOSING KEYCAP}',
    '\N{DIGIT FIVE}\N{COMBINING ENCLOSING KEYCAP}',
    '\N{DIGIT SIX}\N{COMBINING ENCLOSING KEYCAP}',
    '\N{DIGIT SEVEN}\N{COMBINING ENCLOSING KEYCAP}',
    '\N{DIGIT EIGHT}\N{COMBINING ENCLOSING KEYCAP}',
]
back_reaction = '\U00002b05'
go_reaction = '\U000027a1'


class Pagenator:
    def __init__(self, bot, target_user, channel, data, title, desc):
        self.channel = channel
        self.target_user = target_user
        self.bot = bot
        self.title = title
        self.desc = desc

        # [value, value2, value3]
        self.data = data
        self.page = 0

        self.message = None

        # 1ページのデータの個数
        self.columns = 8

        self.max_page = len(self.data) / 8 if not len(self.data) % 8 else len(self.data) // 8 + 1

    async def reflesh_message(self):
        if self.message:
            self.message = await self.channel.fetch_message(self.message.id)

    async def loop(self):
        def check(reaction, user):
                if str(reaction.emoji) not in colmn_reactions + [back_reaction, go_reaction]:
                    return False
                return user.id == self.target_user.id and isinstance(reaction.channel, discord.DMChannel)

        while not self.bot.is_closed():
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=None)
            emoji = str(reaction.emoji)
            if emoji in colmn_reactions:
                p = colmn_reactions.index(emoji)
                embeded_data = self.data[self.page * 8:self.page * 8 + 8]
                selected = embeded_data[p]
                return selected

            elif emoji in [back_reaction, go_reaction]:
                if emoji == back_reaction:
                    self.back_page()
                else:
                    self.go_page()

                await self.edit_embed(self.get_embed())
                await self.reflesh_message()
                continue

    async def add_reactions(self):
        if self.message is None:
            return
        for x in colmn_reactions:
            await self.message.add_reaction(x)
        await self.message.add_reaction(back_reaction)
        await self.message.add_reaction(go_reaction)

    async def start(self):
        """処理を開始し、結果を返す"""
        if self.message is not None:
            return

        message = await self.channel.send(self.get_embed())
        await self.add_reactions()
        return await self.loop()

    async def edit_embed(self, embed):
        if self.message is None:
            return
        await self.message.edit(embed=embed)

    def get_embed(self):
        embed = discord.Embed(title=self.title, description=self.desc)
        embeded_data = self.data[self.page * 8:self.page * 8 + 8]
        for i, column in enumerate(embeded_data, start=1):
            embed.add_field(name=str(i), value=str(column))

        return embed


    def go_page(self):
        """ページを進める"""
        if self.page == self.max_page:
            return
        self.page += 1

    def back_page(self):
        """ページを戻す"""
        if self.page == 0:
            return
        self.page -= 1
