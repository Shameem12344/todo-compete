Video demo at: https://youtu.be/5X8T8Yz9N2E

# Table of Contents
* [Introduction](#introduction)
* [Code and organization](#Code and organization)
    * Templates
    * Models
    * Views
    * Urls
    * Static
    * context processors
    * Settings
    * template tags
* How to run todo-compete
* [Distinctiveness and complexity](#Distinctiveness#and#complexity)
* [Extras](#Extras)

# Introduction 
So the reason I created this app was due to the productivity and the growth I have had as an individual since I got a planner and started to write down each thing I was going to accomplish in the day. This sparked my interest to create a to-do styled app where the user types the goals they have each day and is rewarded for what they complete. The app stresses the idea that if you are cheating or lying for points you are only hurting yourself. The app aims at promoting a sense of urgency and productivity within individuals while also fostering a sense of community.


# Distinctiveness and complexity
Todo_Compete has a group feature which is different from anything we did in the social network where people can create and join groups where they can see each other's daily tasks and hold each other accountable.
It also has countless other features that seperate it from anything we have done in this course.
- This app proves its distinct and complex nature through the:
* grouping feature
* the leaderboard feature: Which includes both the individual and group leaderboard.
* Current and all_time gems: Which is utilized in the leaderboard to rank groups and individuals without hindering their use of the shop to spend gems due to the all_time gems being what matters in user ranking.
* the to-do/completion functionality
* the gem tallying and subtracting functionality
* The shop: A user can buy an extra task for the day with 3 gems in order to be able to get more gems per day to climb the leaderboards. 
* Task limit: Creates a limit of tasks that can be done in a day unless user uses gems to buy more.
* Task reset: Which resets the amount of tasks that can be completed back to 5 in the start of a new day. 
* Light and dark mode: On user toggle
* sparkles: On user click
* Greeting: depending on time of day

# Extras
Used this in the shell:
from todo_app.models import ShopItem

Try to get the ShopItem, or create it if it doesn't exist
item, created = ShopItem.objects.get_or_create(
    effect='increase_task_limit',
    defaults={
        'name': 'Increase Task Limit',
        'description': 'Increases the daily task limit.',
        'price': 3  # Initial price
    }
)

If the item was not newly created, update the price
if not created:
    item.price = 3
    item.save()

print(f"Updated {item.name} price to {item.price} gems")
