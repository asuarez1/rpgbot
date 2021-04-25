from discord.ext import commands


class PosIntConverter(commands.Converter):
    async def convert(self, ctx, arg):
        try:
            i = int(arg)
            if i < 1:
                raise Exception(commands.CommandError)
            return i
        except Exception:
            await ctx.send(f"Invalid argument: '{arg}' must be a positive integer.")
            raise Exception(commands.CommandError)


class IsSkillConverter(commands.Converter):
    async def convert(self, ctx, arg):
        try:
            if arg in ['strength',
                       'dexterity',
                       'intelligence',
                       'luck',
                       'vigor',
                       'spirit']:
                return arg
            else:
                raise Exception(commands.CommandError)
        except Exception:
            await ctx.send(f"Invalid argument: '{arg}' is not a skill.")
            raise Exception(commands.CommandError)
