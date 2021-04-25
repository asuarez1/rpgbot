from discord.ext import commands


class Errors(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("That command does not exist.")
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send('This command is on a %.2fs cooldown' % error.retry_after)
        else:
            raise error


def setup(client):
    client.add_cog(Errors(client))
