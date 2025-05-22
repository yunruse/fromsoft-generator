from functools import partial
from pathlib import Path
from io import BytesIO

from discord import Client, Intents
from discord import Interaction
from discord import app_commands, File

from fromsoft import elden_ring, GRADIENTS

CLIENT_KEY = Path('discord.keys').read_text().strip()

class FromsoftGenerator(Client):
    async def on_ready(self):
        print('Ready!')

    async def setup_hook(self):
        self.tree = app_commands.CommandTree(self)
        for k, v in vars(type(self)).items():
            if isinstance(v, app_commands.Command):
                print(" " * 28, "Found command:", k)
                # annoyingly, discord.py hates OOP it seems
                v._callback = partial(v.callback, self)
                self.tree.add_command(v)
        await self.tree.sync()
        print(" " * 28, "Commands synchronised!")


    @app_commands.command(
        name="fromsoft", description="Verb a noun in Elden Ring style"
    )
    @app_commands.describe(
        text="The text to render",
        hidden="Whisper the response so nobody else sees it.",
        color="The colour as a hex code, or one of " + ', '.join(GRADIENTS.keys()),
        all_caps="Automatically capitalise all text?",
    )
    async def fromsoft(
        self,
        ctx: Interaction,
        text: str,
        color: str = '#ffd042',
        hidden: bool = False,
        all_caps: bool = True,
    ):
        if all_caps:
            text = text.upper()
        img = elden_ring(text, GRADIENTS.get(color, color))
        with BytesIO() as buffer:
            img.save(buffer, 'PNG')
            buffer.seek(0)
            file = File(fp=buffer, filename='image.png')
            await ctx.response.send_message(
                file=file,
                ephemeral=hidden,
            )
        print('fromsoft', text, hidden, ctx)

if __name__ == '__main__':
    intents = Intents.default()

    client = FromsoftGenerator(intents=intents)
    client.run(CLIENT_KEY)
