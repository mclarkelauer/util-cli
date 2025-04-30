import click
from google import genai

from rich.markdown import Markdown
from rich.console import Console


class Gemini:

    Client = None

    def __init__(self, apikey, version="gemini-2.0-flash"):
        self.apikey = apikey
        self.version = version
        self.client = genai.Client(api_key=self.apikey)

    def request(self, text):
        response = client.models.generate_content(models=self.version, contents=[text])
        click.echo(response.text)

    def chat(self):
        chat = self.client.chats.create(model="gemini-2.0-flash")
        console = Console()

        while True:
            value = click.prompt("Prompt:", type=str)
            if value == "q" or value == "quit":
                break
            response = chat.send_message(value)
            md = Markdown(response.text)
            console.print(md)

    @staticmethod
    def create_client(apikey):
        Gemini.Client = Gemini(apikey)

    @staticmethod
    def get_client():
        if Gemini.Client is None:
            raise Exception("Client never initialized")
        return Gemini.Client


@click.command
@click.option("--apikey", "apikey", default=None)
@click.pass_context
def gemini(ctx, apikey):
    if not apikey:
        apikey = ctx.obj.get_config("GEMINI", "apikey")
    Gemini.create_client(apikey)
    client = Gemini.get_client()
    client.chat()
