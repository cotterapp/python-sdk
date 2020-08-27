import click
import cotter
from pprint import pprint
__author__ = "Putri Karunia"


@click.group()
def main():
    """
    Simple CLI for testing Cotter login using cotter package
    """
    pass


@main.command()
def login():
    """Login using email magic link using Cotter SDK"""
    api_key = "API_KEY_ID"
    port = 8080
    response = cotter.login_with_email_link(api_key, port)
    pprint(response)


if __name__ == "__main__":
    main()
