So the reason I created this app was due to the productivity and the growth I have had as an individual since I got a planner and started to write down each thing I was going to accomplish in the day. This sparked my interest to create a to-do styled app where the user types the goals they have each day and is rewarded for what they complete. The app stresses the idea that if you are cheating or lying for points you are only hurting yourself. It also has a group feature which is different from anything we did in the social network where people can create and join groups where they can see each other's daily tasks and hold each other accountable.
This is nothing like we have done before and is much more complex due to the grouping feature I created, the leaderboard feature, the to-do/completion functionality, and the point tallying feature which can be used to buy unlocks in the shop which depletes that point amount, and the most unique feature that resets the tasks at the start of each new day and archives previous tasks by their date. 

Used this in the shell:
from todo_app.models import ShopItem

# Try to get the ShopItem, or create it if it doesn't exist
item, created = ShopItem.objects.get_or_create(
    effect='increase_task_limit',
    defaults={
        'name': 'Increase Task Limit',
        'description': 'Increases the daily task limit.',
        'price': 3  # Initial price
    }
)

# If the item was not newly created, update the price
if not created:
    item.price = 3
    item.save()

print(f"Updated {item.name} price to {item.price} gems")
