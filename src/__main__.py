"""Entry point for the util package."""
import asyncio
from cli import cli

if __name__ == "__main__":
    asyncio.run(cli())
