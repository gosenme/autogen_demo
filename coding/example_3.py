import os

from autogen import ConversableAgent

agent = ConversableAgent(
    "chatbot",
    llm_config={
        "config_list": [{"model": "moonshot-v1-8k",
                         "api_key": "sk-WiIqICuVCznmZG88WcftcK8tljjiJTFg0ZiNqAsPmLfwaIcr",
                         "base_url": "https://api.moonshot.cn/v1",
                         "api_type": "openai"
                         }]},
    code_execution_config=False,  # Turn off code execution, by default it is off.
    function_map=None,  # No registered functions, by default it is None.
    human_input_mode="NEVER",  # Never ask for human input.
)

reply = agent.generate_reply(messages=[{"content": "给我讲个笑话吧", "role": "user"}])
print(reply)

cathy = ConversableAgent(
    "cathy",
    system_message="Your name is Cathy and you are a part of a duo of comedians.",
    llm_config={"config_list": [{"model": "moonshot-v1-8k",
                                 "api_key": "sk-WiIqICuVCznmZG88WcftcK8tljjiJTFg0ZiNqAsPmLfwaIcr",
                                 "base_url": "https://api.moonshot.cn/v1",
                                 "api_type": "openai"
                                 }]},
    human_input_mode="NEVER",  # Never ask for human input.
)

joe = ConversableAgent(
    "joe",
    system_message="Your name is Joe and you are a part of a duo of comedians.",
    llm_config={"config_list": [{"model": "moonshot-v1-8k",
                                 "api_key": "sk-WiIqICuVCznmZG88WcftcK8tljjiJTFg0ZiNqAsPmLfwaIcr",
                                 "base_url": "https://api.moonshot.cn/v1",
                                 "api_type": "openai"
                                 }]},
    human_input_mode="NEVER",  # Never ask for human input.
)

result = joe.initiate_chat(cathy, message="Cathy, 给我讲个笑话.", max_turns=2)
