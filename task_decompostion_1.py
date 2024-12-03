import os
from datetime import datetime
from typing import Callable, Dict, Literal, Optional, Union

from typing_extensions import Annotated

from autogen import (
    Agent,
    AssistantAgent,
    ConversableAgent,
    GroupChat,
    GroupChatManager,
    UserProxyAgent,
    config_list_from_json,
    register_function,
)
from autogen.agentchat.contrib import agent_builder
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
     }
]

task = (
    f"今天是 {datetime.now().date()} ，写一篇关于英伟达过去一个月股价表现的博客文章。"
)
## print(task)

# Create planner agent.
planner = AssistantAgent(
    name="计划人",
    llm_config={
        "config_list": config_list,
        "cache_seed": None,  # Disable legacy cache.
    },
    system_message="你是一个有用的AI助手，你可以将一个复杂的任务分解成3到5个子任务，并最终将任务完成。"
                   "若你觉得计划的任务不够好，可以提出更好的计划，如果执行任务的过程中出现错误，则要分析错误并解决。",
)

# Create a planner user agent used to interact with the planner.
planner_user = UserProxyAgent(
    name="规划使用者",
    human_input_mode="NEVER",
    code_execution_config=False,
)


# The function for asking the planner.


def task_planner(question: Annotated[str, "Question to ask the planner."]) -> str:
    with Cache.disk(cache_seed=4) as cache:
        planner_user.initiate_chat(planner, message=question, max_turns=1, cache=cache)
    # return the last message received from the planner
    return planner_user.last_message()["content"]


# Create assistant agent.
assistant = AssistantAgent(
    name="助手",
    system_message="你是一个有用的AI助手。你可以通过计划人，将一个复杂的任务分解成若干个子任务。务必完成这些分解后的子任务。"
                   "必要时，你可以基于markdown的代码块格式给出代码，我会执行这些代码。"
                   "你要要为用户提供一个最终解决方案。只有当子任务全部完成时，才返回 “TERMINATE”字样表示终止。",
    llm_config={
        "config_list": config_list,
        "cache_seed": None,  # Disable legacy cache.
    },
)

# Setting up code executor.
os.makedirs("planning", exist_ok=True)
# Use DockerCommandLineCodeExecutor to run code in a docker container.
# code_executor = DockerCommandLineCodeExecutor(work_dir="planning")
code_executor = LocalCommandLineCodeExecutor(work_dir="planning")

# Create user proxy agent used to interact with the assistant.
user_proxy = UserProxyAgent(
    name="用户代理",
    human_input_mode="ALWAYS",
    is_termination_msg=lambda x: "content" in x
                                 and x["content"] is not None
                                 and x["content"].rstrip().endswith("TERMINATE"),
    code_execution_config={"executor": code_executor},
)

# Register the function to the agent pair.
register_function(
    task_planner,
    caller=assistant,
    executor=user_proxy,
    name="task_planner",
    description="一个能够帮助你将一项复杂任务分解成子任务的任务规划器工具。",
)

# Use Cache.disk to cache LLM responses. Change cache_seed for different responses.
with Cache.disk(cache_seed=1) as cache:
    # the assistant receives a message from the user, which contains the task description
    user_proxy.initiate_chat(
        assistant,
        message=task,
        cache=cache,
    )
