import os

from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from autogen.cache import Cache
from autogen.coding import DockerCommandLineCodeExecutor, LocalCommandLineCodeExecutor

config_list = [
    {"model": "moonshot-v1-8k",
     "api_key": "sk-WiIqICuVCznmZG88WcftcK8tljjiJTFg0ZiNqAsPmLfwaIcr",
     "base_url": "https://api.moonshot.cn/v1",
     "api_type": "openai"
     },
    {"model": "moonshot-v1-32k",
     "api_key": "sk-WiIqICuVCznmZG88WcftcK8tljjiJTFg0ZiNqAsPmLfwaIcr",
     "base_url": "https://api.moonshot.cn/v1",
     "api_type": "openai"
     },
]
# You can also use the following method to load the config list from a file or environment variable.
# config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

os.makedirs("coding", exist_ok=True)
# Use DockerCommandLineCodeExecutor if docker is available to run the generated code.
# Using docker is safer than running the generated code directly.
# code_executor = DockerCommandLineCodeExecutor(work_dir="coding")
code_executor = LocalCommandLineCodeExecutor(work_dir="coding")

user_proxy = UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    code_execution_config={"executor": code_executor},
)

writing_assistant = AssistantAgent(
    name="writing_assistant",
    system_message="你是一名写作助理，负责撰写引人入胜的博客文章。您尝试根据用户的要求写出最好的博客文章。如果用户提供了评论或要求，请根据评论或要求的提示尝试修改之前写出的版本。",
    llm_config={"config_list": config_list, "cache_seed": None},
)

reflection_assistant = AssistantAgent(
    name="reflection_assistant",
    system_message="对写作内容提出评论或建议。提供详细的建议，包括长度、深度、风格等要求等等",
    llm_config={"config_list": config_list, "cache_seed": None},
)


def reflection_message(recipient, messages, sender, config):
    print("Reflecting...")
    return f"对以下写作进行反思和评论: \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}"


nested_chat_queue = [
    {
        "recipient": reflection_assistant,
        "message": reflection_message,
        "max_turns": 1,
    },
]
user_proxy.register_nested_chats(
    nested_chat_queue,
    trigger=writing_assistant,
    # position=4,
)

# Use Cache.disk to cache the generated responses.
# This is useful when the same request to the LLM is made multiple times.
with Cache.disk(cache_seed=42) as cache:
    user_proxy.initiate_chat(
        writing_assistant,
        message="写一篇关于人工智能最新更新的引人入胜的博客文章。这篇博客对普通观众来说是引人入胜且易于理解的。段落应超过3段，但不超过1000字。",
        max_turns=2,
        cache=cache,
    )
