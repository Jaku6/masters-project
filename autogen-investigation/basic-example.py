from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
import os


# Setting configurations for autogen
config_list = config_list_from_json(
    env_or_file="OAI_CONFIG_LIST",
    file_location="D:\Repos\masters-project\\autogen-investigation",
    filter_dict={
        "model": {
            "gpt-4",
        }
    }
)
assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})
user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding", "use_docker": True})
user_proxy.initiate_chat(assistant, message="What time is it?")
