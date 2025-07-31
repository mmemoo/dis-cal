import nextcord
import argparse
import aiohttp
from scripts.add_cal_to_state import add_cal_to_state
from scripts.calc_cal import estimate_cals_and_nutrients
from scripts.estimate_foods import estimate_food_amounts
from scripts.check_setup_state import check_setup_state

parser = argparse.ArgumentParser()
parser.add_argument(
    "--token",required=True,help="Argument to pass your bot token",type=str
)

args = parser.parse_args()
token = args.token


if check_setup_state():
    client = nextcord.Client()


    @client.slash_command(
        name="estimate",
        description="Estimate cals and nutrients in a photo which contains food. (Best works when only the foods you care are in the frame and from a good angle.)"
    )
    async def estimate(
        interaction,
        img : nextcord.Attachment = nextcord.SlashOption(name="image",description="Image to be the foods calories in it estimated.")
    ):
        if img.content_type.startswith("image/"):
            await interaction.response.defer()
            
            with aiohttp.ClientSession() as session:
                with session.get(img.url) as response:
                    if response.status == 200:
                        image_data = await response.read()

                        await image_data.save("imgs/"+img.filename)

            food_items = estimate_food_amounts("imgs/"+img.filename)
            total_nutrients,total_cals = estimate_cals_and_nutrients(food_items)

            await interaction.followup.send(f""":white_check_mark: Calories and nutrients estimated :

    Total cals = {total_cals}
    Protein = {total_nutrients["Protein"][0] + " " + total_nutrients["Protein"][1]}""")

        else:
            await interaction.response.send_message(
                ":exclamation: The content you uploaded wasn't an image, please upload a proper image. :exclamation:"
            )

    client.run(token)
else:
    print("Cant run app.py while setup is not done. Complete the setup and try again.")