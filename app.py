import nextcord
import argparse


parser = argparse.ArgumentParser()
parser.add_argument(
    "--token",required=True,help="Argument to pass your bot token",type=str
)

args = parser.parse_args()
token = args.token