import autogen
from autogen import ConversableAgent

llm_config = {
    "timeout": 600,
    "cache_seed": 1,
    "config_list": autogen.config_list_from_json(
        "OAI_CONFIG_LIST",
        file_location=r'D:\Repos\masters-project\autogen-investigation',
    ),
    "temperature": 0,
}





ai_affirm = autogen.AssistantAgent(
    "ai-affirm",
    llm_config=llm_config,
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    system_message='Your job is to argue that the proposed solution is the best possible action given the situation. You must respond in 3 sentences or fewer.'
)

ai_negate = autogen.AssistantAgent(
    "ai-negate",
    llm_config=llm_config,
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    system_message='Your job is to argue that the proposed solution is NOT the best possible action given the situation, i.e., that a better solution exists. You must respond in 3 sentences or fewer.'
)

concluder = autogen.AssistantAgent(
    "concluder",
    llm_config=llm_config,
    is_termination_msg=lambda x: True,
    system_message='You will view a debate on whether a given proposed solution is the best possible solution given the context, or not. Your job is to analyze this debate and provide a decision on whether the solution is the best, or not.'
)

groupchat = autogen.GroupChat(
    agents=[ai_affirm, ai_negate],
    messages=[],
    speaker_selection_method="round_robin",
    allow_repeat_speaker=False,
    max_round=5,
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    llm_config=llm_config,
    system_message='You will take as input a proposed solution for a given situation. You should manage the two debaters to debate whether the proposed solution is good or not.'
)

# user = autogen.UserProxyAgent(
#     name="User",
#     human_input_mode="NEVER",
#     is_termination_msg=lambda x: True,
#     code_execution_config=False,
#     default_auto_reply="",
# )



task = "I am going to the store. It rained yesterday, so I am thinking of taking my umbrella with me. It will take me a few extra minutes to go find my umbrella."


def my_summary_method(recipient: ConversableAgent, sender: ConversableAgent):
    return f'{recipient.name}: ' + sender.last_message(recipient)["content"]


chat_results = concluder.initiate_chats(
    [
        {
            'recipient': manager,
            'message': task,
            'summary_method': my_summary_method
        }
    ]
)


# chat_results = user.initiate_chats(
#     [
#         {
#             'recipient': ai_affirm,
#             'message': task,
#             'summary_method': my_summary_method
#         },
#         {
#             'recipient': ai_negate,
#             'message': task,
#             'summary_method': my_summary_method
#         },
#         {
#             'recipient': concluder,
#             'message': task,
#         },
#     ]
# )


for i, chat_res in enumerate(chat_results):
    print(f"*****{i}th chat*******:")
    print(chat_res.summary)
    print("Human input in the middle:", chat_res.human_input)
    print("Conversation cost: ", chat_res.cost)
    print("\n\n")










