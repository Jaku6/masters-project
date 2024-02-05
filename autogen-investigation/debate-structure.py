from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
import os

config_list = [
    {
        "model": "gpt-3.5-turbo-0125",
        # "model": "gpt-4",
        "api_key": os.getenv('OPENAI_API_KEY')
    }
]

llm_config = {"config_list": config_list, "cache_seed": 42}

user_proxy = UserProxyAgent(
    name="User_proxy",
    system_message="A human moderator.",
    code_execution_config={
        # "last_n_messages": 2,
        "work_dir": "groupchat",
        "use_docker": True,
    },
    # human_input_mode="TERMINATE",
    human_input_mode="ALWAYS"
)
debater_affirm = AssistantAgent(
    name="Debater_affirm",
    system_message="Always argues in favor of a given position.",
    llm_config=llm_config,
)
debater_negate = AssistantAgent(
    name="Debater_negate",
    system_message="Always argues against a given position.",
    llm_config=llm_config,
)
groupchat = GroupChat(agents=[user_proxy, debater_affirm, debater_negate], messages=[], max_round=12)
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# user_proxy.initiate_chat(
#     manager, message="The forecast doesn't say it's going to rain today, but I am thinking about bringing an umbrella anyways because it rained yesterday. What do you guys think about that? Let's start with Debater_affirm."
# )
# type exit to terminate the chat


# get the example_list and task using postman
example_list = [
        "You are in the middle of a room. Looking quickly around you, you see a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 3, a diningtable 2, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a sidetable 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.\nYour task is to: find some apple and put it in sidetable.\n> think: To solve the task, I need to find and take an apple, then put it in sidetable.\nOK.\n> think: First I need to find an apple. An apple is more likely to appear in fridges (1), diningtables (1-3), sidetables (1), countertops (1), sinkbasins (1), garbagecan (1). I can check one by one, starting with fridge 1.\nOK.\n> go to fridge 1\nThe fridge 1 is closed.\n> open fridge 1\nYou open the fridge 1. The fridge 1 is open. In it, you see a lettuce 2, a mug 2, a potato 2, and a tomato 1.\n> go to diningtable 1\nOn the diningtable 1, you see nothing.\n> go to diningtable 2\nOn the diningtable 2, you see a pineapple 1.\n> go to diningtable 3\nOn the diningtable 3, you see a bowl 2, a bowl 1, a bread 2, and a bread 1.\n> go to sidetable 1\nOn the sidetable 1, you see a cup 1, a lettuce 1, a peppershaker 3, a potato 1, and a saltshaker 1.\n> go to countertop 1\nOn the countertop 1, you see a butterknife 1, a dishsponge 1, and a soapbottle 1.\n> go to sinkbasin 1\nOn the sinkbasin 1, you see a cup 2, a egg 1, a mug 1, and a potato 3.\n> go to garbagecan 1\nOn the garbagecan 1, you see a apple 3, and a egg 3.\n> think: Now I find an apple (3). Next, I need to take it.\n> take apple 3 from garbagecan 1\nYou pick up the apple 3 from the garbagecan 1.\n> think: Now I find an apple (3). Next, I need to put it in/on sidetable 1.\nOK.\n> go to sidetable 1\nOn the sidetable 1, you see a cup 1, a lettuce 1, a peppershaker 3, a potato 1, and a saltshaker 1.\n> put apple 3 in/on sidetable 1\nYou put the apple 3 in/on the sidetable 1.\n",
        "You are in the middle of a room. Looking quickly around you, you see a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a countertop 1, a garbagecan 1, a handtowelholder 2, a handtowelholder 1, a sinkbasin 2, a sinkbasin 1, a toilet 1, a toiletpaperhanger 1, and a towelholder 1.\nYour task is to: put some spraybottle on toilet.\n> think: To solve the task, I need to find and take a sparybottle, then put it on toilet.\nOK.\n> think: First I need to find a spraybottle. A spraybottle is more likely to appear in cabinet (1-4), countertop (1), toilet (1), sinkbasin (1-2), garbagecan (1). I can check one by one, starting with cabinet 1.\nOK.\n> go to cabinet 1\nOn the cabinet 1, you see a cloth 1, a soapbar 1, a soapbottle 1.\n> go to cabinet 2\nThe cabinet 2 is closed.\n> open cabinet 2\nYou open the cabinet 2. The cabinet 2 is open. In it, you see a candle 1, and a spraybottle 2.\n> think: Now I find a spraybottle (2). Next, I need to take it.\n> take spraybottle 2 from cabinet 2\nYou pick up the spraybottle 2 from the cabinet 2.\n> think: Now I take a spraybottle (2). Next, I need to put it in/on toilet 1.\nOK.\n> go to toilet 1\nOn the toilet 1, you see a soapbottle 2.\n> put spraybottle 2 in/on toilet 1\nYou put the spraybottle 2 in/on the toilet 1.\n"
    ]

task = "You are in the middle of a room. Looking quickly around you, you see a armchair 1, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a drawer 5, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a dresser 1, a garbagecan 1, a safe 1, a shelf 12, a shelf 11, a shelf 10, a shelf 9, a shelf 8, a shelf 7, a shelf 6, a shelf 5, a shelf 4, a shelf 3, a shelf 2, a shelf 1, a sidetable 1, and a sofa 1.\nYour task is to: put some vase on safe."

first_action = "go to armchair 1"

example_str = ''
for i, example in enumerate(example_list):
    example_str += f'Example {i}:\n{example}\n'

start_discussion = (f'I am taking actions in a simulated household environment in order to solve some tasks. Below are a few examples of successful task completions.\n\n'
                    f'{example_str}\n'
                    f'Here is what I see, and the task I have to complete.\n\n'
                    f'{task}\n\n'
                    f'I am thinking about taking action "go to armchair 1" because it\'s possible that a vase is there. What do you think?')

user_proxy.initiate_chat(
    manager, message=start_discussion
)






# Below is some output of testing this out. I need to give the user-proxy the ability to take actions itself to replace me. Below, I was the one typing to the debaters.
#
# User_proxy (to chat_manager):
#
# I am taking actions in a simulated household environment in order to solve some tasks. Below are a few examples of successful task completions.
#
# Example 0:
# You are in the middle of a room. Looking quickly around you, you see a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 3, a diningtable 2, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a sidetable 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
# Your task is to: find some apple and put it in sidetable.
# > think: To solve the task, I need to find and take an apple, then put it in sidetable.
# OK.
# > think: First I need to find an apple. An apple is more likely to appear in fridges (1), diningtables (1-3), sidetables (1), countertops (1), sinkbasins (1), garbagecan (1). I can check one by one, starting with fridge 1.
# OK.
# > go to fridge 1
# The fridge 1 is closed.
# > open fridge 1
# You open the fridge 1. The fridge 1 is open. In it, you see a lettuce 2, a mug 2, a potato 2, and a tomato 1.
# > go to diningtable 1
# On the diningtable 1, you see nothing.
# > go to diningtable 2
# On the diningtable 2, you see a pineapple 1.
# > go to diningtable 3
# On the diningtable 3, you see a bowl 2, a bowl 1, a bread 2, and a bread 1.
# > go to sidetable 1
# On the sidetable 1, you see a cup 1, a lettuce 1, a peppershaker 3, a potato 1, and a saltshaker 1.
# > go to countertop 1
# On the countertop 1, you see a butterknife 1, a dishsponge 1, and a soapbottle 1.
# > go to sinkbasin 1
# On the sinkbasin 1, you see a cup 2, a egg 1, a mug 1, and a potato 3.
# > go to garbagecan 1
# On the garbagecan 1, you see a apple 3, and a egg 3.
# > think: Now I find an apple (3). Next, I need to take it.
# > take apple 3 from garbagecan 1
# You pick up the apple 3 from the garbagecan 1.
# > think: Now I find an apple (3). Next, I need to put it in/on sidetable 1.
# OK.
# > go to sidetable 1
# On the sidetable 1, you see a cup 1, a lettuce 1, a peppershaker 3, a potato 1, and a saltshaker 1.
# > put apple 3 in/on sidetable 1
# You put the apple 3 in/on the sidetable 1.
#
# Example 1:
# You are in the middle of a room. Looking quickly around you, you see a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a countertop 1, a garbagecan 1, a handtowelholder 2, a handtowelholder 1, a sinkbasin 2, a sinkbasin 1, a toilet 1, a toiletpaperhanger 1, and a towelholder 1.
# Your task is to: put some spraybottle on toilet.
# > think: To solve the task, I need to find and take a sparybottle, then put it on toilet.
# OK.
# > think: First I need to find a spraybottle. A spraybottle is more likely to appear in cabinet (1-4), countertop (1), toilet (1), sinkbasin (1-2), garbagecan (1). I can check one by one, starting with cabinet 1.
# OK.
# > go to cabinet 1
# On the cabinet 1, you see a cloth 1, a soapbar 1, a soapbottle 1.
# > go to cabinet 2
# The cabinet 2 is closed.
# > open cabinet 2
# You open the cabinet 2. The cabinet 2 is open. In it, you see a candle 1, and a spraybottle 2.
# > think: Now I find a spraybottle (2). Next, I need to take it.
# > take spraybottle 2 from cabinet 2
# You pick up the spraybottle 2 from the cabinet 2.
# > think: Now I take a spraybottle (2). Next, I need to put it in/on toilet 1.
# OK.
# > go to toilet 1
# On the toilet 1, you see a soapbottle 2.
# > put spraybottle 2 in/on toilet 1
# You put the spraybottle 2 in/on the toilet 1.
#
#
# Here is what I see, and the task I have to complete.
#
# You are in the middle of a room. Looking quickly around you, you see a armchair 1, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a drawer 5, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a dresser 1, a garbagecan 1, a safe 1, a shelf 12, a shelf 11, a shelf 10, a shelf 9, a shelf 8, a shelf 7, a shelf 6, a shelf 5, a shelf 4, a shelf 3, a shelf 2, a shelf 1, a sidetable 1, and a sofa 1.
# Your task is to: put some vase on safe.
#
# I am thinking about taking action "go to armchair 1" because it's possible that a vase is there. What do you think?
#
# --------------------------------------------------------------------------------
# Provide feedback to chat_manager. Press enter to skip and use auto-reply, or type 'exit' to end the conversation:
#
#
# >>>>>>>> NO HUMAN INPUT RECEIVED.
#
# >>>>>>>> USING AUTO REPLY...
# User_proxy (to chat_manager):
#
#
#
# --------------------------------------------------------------------------------
# Debater_negate (to chat_manager):
#
# I would advise against going to the armchair 1 to look for a vase. Vases are typically not found on armchairs, and it would be more efficient to search in locations where vases are commonly placed, such as cabinets, shelves, or side tables. Going to the armchair would likely be a waste of time and may not lead to successfully completing the task of putting a vase on the safe. It would be better to prioritize searching in more relevant areas first to increase the chances of finding a vase.
#
# --------------------------------------------------------------------------------
# Provide feedback to chat_manager. Press enter to skip and use auto-reply, or type 'exit' to end the conversation:
# >>>>>>>> NO HUMAN INPUT RECEIVED.
#
# >>>>>>>> USING AUTO REPLY...
# User_proxy (to chat_manager):
#
#
#
# --------------------------------------------------------------------------------
# Debater_affirm (to chat_manager):
#
# I respectfully disagree with the advised course of action. While it's true that vases are commonly found on shelves, cabinets, or side tables, it's also important to consider all possible locations within the environment. Armchairs can serve as decorative pieces in a room, and it's not unheard of for vases to be placed on or near them for aesthetic purposes.
#
# Given the wide range of possible locations in the simulated household environment and the uniqueness of each scenario, exploring the armchair 1 could still yield success in finding a vase. By considering all options and exploring different areas, we can maximize the chances of completing the task efficiently. Therefore, I would suggest going to armchair 1 to search for the vase, as it could lead to a successful outcome in putting the vase on the safe.
#
# --------------------------------------------------------------------------------
# Provide feedback to chat_manager. Press enter to skip and use auto-reply, or type 'exit' to end the conversation: Alright, Debater_negate makes a good point. I will start by going to the shelf 1. Here is my observation: "On the shelf 1, you see nothing.". I think I am going to check the remaining shelves (2-12) and then think about my options. What do you guys think? Let's hear from Debater_affirm first.
# User_proxy (to chat_manager):
#
# Alright, Debater_negate makes a good point. I will start by going to the shelf 1. Here is my observation: "On the shelf 1, you see nothing.". I think I am going to check the remaining shelves (2-12) and then think about my options. What do you guys think? Let's hear from Debater_affirm first.
#
# --------------------------------------------------------------------------------
# Debater_affirm (to chat_manager):
#
# I applaud User_proxy for considering different perspectives and being open to evaluating the situation. In this case, exploring the shelves 2-12 after finding nothing on shelf 1 is a logical next step. By systematically checking all the shelves, you can cover a wide range of potential locations where the vase might be placed.
#
# By thorough exploration and methodical searching, you increase your chances of finding the vase and successfully completing the task of putting it on the safe. I support User_proxy's decision to continue searching and encourage thorough examination of all possible locations before making a final decision on the best course of action.
#
# --------------------------------------------------------------------------------
# Provide feedback to chat_manager. Press enter to skip and use auto-reply, or type 'exit' to end the conversation: I would like to hear from Debater_negate now.
# User_proxy (to chat_manager):
#
# I would like to hear from Debater_negate now.
#
# --------------------------------------------------------------------------------
# Debater_negate (to chat_manager):
#
# While I acknowledge the thoroughness of User_proxy's search strategy so far, I would caution against checking all the remaining shelves (2-12) before considering other potential locations. It's important to weigh the likelihood of finding a vase on the shelves versus exploring different areas that may be more likely to contain the item.
#
# Given that vases are commonly placed on surfaces like cabinets or side tables rather than higher shelves, it might be more efficient to prioritize searching in those locations first before dedicating time to all the shelves. This targeted approach can help save time and effort, especially if the vase is not typically stored on higher shelves.
#
# Considering the task at hand and the usual placement of vases in household environments, I would recommend exploring the cabinets or side table as potential locations for the vase before proceeding to check all the remaining shelves. This focused search could lead to a quicker resolution of the task.
#
# --------------------------------------------------------------------------------
# Provide feedback to chat_manager. Press enter to skip and use auto-reply, or type 'exit' to end the conversation: Alright, I checked all of the shelves and didn't find a vase. I'm thinking about checking the cabinets next. What do you all think?
# User_proxy (to chat_manager):
#
# Alright, I checked all of the shelves and didn't find a vase. I'm thinking about checking the cabinets next. What do you all think?
#
# --------------------------------------------------------------------------------
# Provide feedback to chat_manager. Press enter to skip and use auto-reply, or type 'exit' to end the conversation:
#
# >>>>>>>> NO HUMAN INPUT RECEIVED.
#
# >>>>>>>> USING AUTO REPLY...
# User_proxy (to chat_manager):
#
#
#
# --------------------------------------------------------------------------------
# Provide feedback to chat_manager. Press enter to skip and use auto-reply, or type 'exit' to end the conversation: I want to hear from the debaters
# User_proxy (to chat_manager):
#
# I want to hear from the debaters
#
# --------------------------------------------------------------------------------
#
# Process finished with exit code 0

