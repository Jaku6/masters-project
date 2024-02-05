from autogen import AssistantAgent, UserProxyAgent
import os

config_list = [
    {
        "model": "gpt-3.5-turbo-0125",
        "api_key": os.getenv('OPENAI_API_KEY')
    }
]
assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})
user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding", "use_docker": True})
user_proxy.initiate_chat(assistant, message="What time is it?")
