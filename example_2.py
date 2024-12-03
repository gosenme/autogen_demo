import autogen
from autogen import AssistantAgent, UserProxyAgent

llm_config = {"model": "moonshot-v1-8k",
              "api_key": "sk-WiIqICuVCznmZG88WcftcK8tljjiJTFg0ZiNqAsPmLfwaIcr",
              "base_url": "https://api.moonshot.cn/v1",
              "api_type": "openai"
              }
assistant = AssistantAgent("assistant", llm_config=llm_config)
user_proxy = UserProxyAgent(
    "user_proxy", code_execution_config={"executor": autogen.coding.LocalCommandLineCodeExecutor(work_dir="coding")}
)
user_proxy.initiate_chat(
    assistant,
    message="Plot a chart of NVDA and TESLA stock price change YTD.",
)
