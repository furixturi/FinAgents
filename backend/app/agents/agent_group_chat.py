from dotenv import load_dotenv

load_dotenv()

import os
from typing import List, Optional, Dict, Any, Tuple, Union
from enum import Enum

from fastapi import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from autogen.agentchat import (
    ConversableAgent,
    UserProxyAgent,
    AssistantAgent,
    GroupChat,
    GroupChatManager,
    Agent,
)
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent

from app.crud.agent import user_get_agent, user_create_agent
from app.crud.agent_group import user_get_agent_group, user_create_agent_group
from app.crud.agent_group_member import (
    user_get_agent_group_members,
    user_create_agent_group_member,
)
from app.crud.agent_group_message import (
    user_get_agent_group_messages,
    user_create_agent_group_message,
)

from app.schemas import (
    AIAgentCreate,
    AgentGroupCreate,
    AgentGroupMemberCreate,
    AgentGroupMessageCreate,
    MessageContent,
)
from app.models import AIAgent, AgentGroup, AgentGroupMember, AgentGroupMessage

from app.agents.agent_group_connection_manager import AgentGroupConnectionManager

DUMMY_GROUP_CONFIG = {
    "name": "Dummy Group",
    "max_round": 10,
    "speaker_selection_method": "round_robin",
}

DUMMY_GROUP_MANAGER_LLM = "gpt_4_turbo"

DUMMY_LLM_CONFIGS = {
    "gpt_4o": {
        "model": os.environ.get("GPT_4O_MODEL"),
        "api_type": "azure",
        "api_key": os.environ.get("GPT_4O_API_KEY"),
        "base_url": os.environ.get("GPT_4O_AZURE_ENDPOINT"),
        "api_version": os.environ.get("GPT_4O_API_VERSION"),
    },
    "gpt_4_turbo": {
        "model": os.environ.get("GPT_4_TURBO_MODEL"),
        "api_type": "azure",
        "api_key": os.environ.get("GPT_4_TURBO_API_KEY"),
        "base_url": os.environ.get("GPT_4_TURBO_AZURE_ENDPOINT"),
        "api_version": os.environ.get("GPT_4_TURBO_API_VERSION"),
    },
    "gpt_35_turbo": {
        "model": os.environ.get("GPT_35_TURBO_MODEL"),
        "api_type": "azure",
        "api_key": os.environ.get("GPT_35_TURBO_API_KEY"),
        "base_url": os.environ.get("GPT_35_TURBO_AZURE_ENDPOINT"),
        "api_version": os.environ.get("GPT_35_TURBO_API_VERSION"),
    },
}

DUMMY_AGENT_CONFIGS = [
    {
        "name": "Admin",
        "system_message": "A human admin. Give the task, and send instructions to writer to refine the blog post.",
        "code_execution_config": False,
        "agent_type": "UserProxyAgent",
    },
    {
        "name": "Planner",
        "system_message": """Planner. Given a task, please determine what information is needed to complete the task.
        Please note that the information will all be retrieved using Python code. Please only suggest information that can be retrieved using Python code.
        """,
        "llm_config": {"config_list": ["config_gpt_4_turbo"]},
        "agent_type": "AssistantAgent",
    },
    {
        "name": "Engineer",
        "llm_config": {"config_list": ["config_gpt_4_turbo"], "cache_seed": None},
        "system_message": """Engineer. You write python/bash to retrieve relevant information. Wrap the code in a code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor. 
        Always provide bash code block to install dependency first.
        Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
        If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
        Write code to print the output so that the others can access the result. When you use code to plot data, save the graph to an image file in the work dir and print out the file path. 
        """,
        "agent_type": "AssistantAgent",
    },
    {
        "name": "Writer",
        "llm_config": {"config_list": ["config_gpt_4_turbo"], "cache_seed": None},
        "system_message": """Writer. Please write finance report and documentation in markdown format (with relevant titles) and put the content in pseudo ```md``` code block. You will write it for a task based on previous chat history. Don't write any code. You can get code from Engineer and put them in markdown style code blocks in your report if necessary.""",
        "agent_type": "AssistantAgent",
    },
]


## For reference only
def create_default_agents() -> List[ConversableAgent]:
    user_proxy = UserProxyAgent(
        name="Human Admin",
        system_message="A human admin. Give the task, and send instructions to writer to refine the blog post.",
        code_execution_config=False,
    )

    planner = AssistantAgent(
        name="Planner",
        system_message="""Planner. Given a task, please determine what information is needed to complete the task.
        Please note that the information will all be retrieved using Python code. Please only suggest information that can be retrieved using Python code.
        """,
        llm_config={"config_list": [DUMMY_LLM_CONFIGS["config_gpt_4_turbo"]]},
    )

    engineer = AssistantAgent(
        name="Engineer",
        llm_config={
            "config_list": [DUMMY_LLM_CONFIGS["config_gpt_4_turbo"]],
            "cache_seed": None,
        },
        system_message="""Engineer. You write python/bash to retrieve relevant information. Wrap the code in a code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor. 
        Always provide bash code block to install dependency first.
        Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
        If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
        Write code to print the output so that the others can access the result. When you use code to plot data, save the graph to an image file in the work dir and print out the file path. 
        """,
    )

    writer = (
        AssistantAgent(
            name="Writer",
            llm_config={
                "config_list": [DUMMY_LLM_CONFIGS["config_gpt_4_turbo"]],
                "cache_seed": None,
            },
            system_message="""Writer. Please write finance report and documentation in markdown format (with relevant titles) and put the content in pseudo ```md``` code block. You will write it for a task based on previous chat history. Don't write any code. You can get code from Engineer and put them in  markdown style code blocks in your report if necessary.""",
        ),
    )

    # os.makedirs("paper", exist_ok=True)
    # code_executor = UserProxyAgent(
    #     name = "Executor",
    #     system_message = "Executor. Execute the code written by the engineer and report the result.",
    #     description = "Executor should always be called after the engineer has written the code to be executed.",
    #     human_input_mode = "ALWAYS",
    #     code_execution_config = {
    #         "last_n_messages": 3,
    #         "executor": LocalCommandLineCodeExecutor(work_dir="paper"),
    #     },
    # )

    return [
        user_proxy,
        planner,
        engineer,
        writer,
        # code_executor
    ]


class AgentGroupChat:
    def __init__(
        self,
        db: AsyncSession,
        user_id: int,
        group_id: int = None,
        group_manager_llm: str = "",
        agent_configs: List[dict] = None,
        llm_configs: dict = None,
        group_config: dict = {},
        websocket: WebSocket = None,
        websocket_conn_manager: AgentGroupConnectionManager = None,
        dummy: bool = False,
    ):
        self.db = db
        self.user_id = user_id
        self.websocket = websocket
        self.websocket_conn = websocket_conn_manager

        if not dummy and not (
            group_id or (group_manager_llm and agent_configs and llm_configs)
        ):
            raise ValueError(
                "Either a valid group_id of a group created by the user, or a set of group_manager_llm, agent_configs, and llm_configs must be provided"
            )

        self.group_manager_llm = group_manager_llm
        self.group_config = group_config
        self.agent_configs = agent_configs
        self.llm_configs = llm_configs

        self.group_data: AgentGroup = None
        self.agents_data: List[AIAgent] = []
        self.messages_data: List[AgentGroupMessage] = []

        self.agent_name_to_id: Dict[str, int] = {}

        self.autogen_agents = []
        self.autogen_messages = []
        self.autogen_agent_group_chat = None
        self.autogen_agent_group_chat_manager = None
        self.user_proxy = None

    @classmethod
    async def create(
        cls,
        db: AsyncSession,
        user_id: int,
        group_id: int = None,
        group_manager_llm: str = "",
        agent_configs: List[dict] = None,
        llm_configs: dict = None,
        group_config: dict = {},
        websocket: WebSocket = None,
        websocket_conn_manager: AgentGroupConnectionManager = None,
        dummy: bool = False,
    ):
        instance = cls(
            db,
            user_id,
            group_id,
            group_manager_llm,
            agent_configs,
            llm_configs,
            group_config,
            websocket,
            websocket_conn_manager,
            dummy,
        )
        if dummy:
            group_manager_llm = DUMMY_GROUP_MANAGER_LLM
            group_config = DUMMY_GROUP_CONFIG
            agent_configs = DUMMY_AGENT_CONFIGS
            llm_configs = DUMMY_LLM_CONFIGS
            instance.llm_configs = llm_configs

        if group_id:
            instance.group_data = await instance._a_retrieve_agent_group_data(group_id)
            if instance.group_data:
                instance.agents_data = await instance._a_retrieve_group_agents_data(
                    group_id
                )
                instance.messages_data = await instance._a_retrieve_group_messages_data(
                    group_id
                )
            else:
                raise ValueError(f"Agent group with id {group_id} not found")
        else:
            instance.group_data = await instance._a_create_and_store_agent_group_data(
                group_config
            )
            instance.agents_data = await instance._a_create_and_store_group_agents_data(
                agent_configs, instance.group_data.id
            )

        instance.autogen_agents = [
            instance._create_autogen_agent(agent_data)
            for agent_data in instance.agents_data
        ]
        instance.autogen_messages = [
            instance._create_autogen_message(message_data)
            for message_data in instance.messages_data
        ]
        instance.autogen_agent_group_chat, instance.autogen_agent_group_chat_manager = (
            instance._initialize_agent_group_chat()
        )
        return instance

    @property
    def group_id(self):
        return self.group_id

    # CRUD to create and store new data of agent, agent_group, agent_group_messages to db
    async def _a_create_and_store_agent_group_data(self, group_config) -> AgentGroup:
        return await user_create_agent_group(
            db=self.db,
            agent_group_create=AgentGroupCreate(
                created_by=self.user_id, **group_config
            ),
        )

    async def _a_create_and_store_group_agents_data(
        self, agent_configs: List[dict], group_id
    ) -> List[AIAgent]:
        agents_data = []
        for agent_config in agent_configs:
            agent_data = await user_create_agent(
                db=self.db,
                agent_create=AIAgentCreate(user_id=self.user_id, **agent_config),
            )
            # also create and store the new membership
            _ = await user_create_agent_group_member(
                db=self.db,
                agent_group_member_create=AgentGroupMemberCreate(
                    group_id=group_id, agent_id=agent_data.id
                ),
            )
            agents_data.append(agent_data)
        return agents_data

    # CRUD to retireve data of agent, agent_group, agent_group_messages from db with given group_id
    async def _a_retrieve_agent_group_data(self, group_id: int):
        group_data = await user_get_agent_group(self.db, self.user_id, group_id)
        if group_data:
            return group_data
        return None

    async def _a_retrieve_group_agents_data(self, group_id: int):
        group_members = await user_get_agent_group_members(
            self.db, self.user_id, group_id
        )
        agents_data = []
        for member in group_members:
            agent_data = await user_get_agent(self.db, self.user_id, member.agent_id)
            if agent_data:
                agents_data.append(agent_data)
        return agents_data

    async def _a_retrieve_group_messages_data(self, group_id: int):
        messages_data = await user_get_agent_group_messages(
            self.db, self.user_id, group_id
        )
        return messages_data

    # Use the data to create autogen agents, messages, groupchat, groupchat_manager
    def _create_autogen_agent(self, agent_data: AIAgent):
        agent_name = agent_data.name
        if agent_name in self.agent_name_to_id:
            raise ValueError(f"Agent name {agent_name} is not unique")
        agent_id = agent_data.id
        self.agent_name_to_id[agent_name] = agent_id

        agent_constructors = {
            "ConversableAgent": ConversableAgent,
            "UserProxyAgent": UserProxyAgent,
            "AssistantAgent": AssistantAgent,
            "GPTAssistantAgent": GPTAssistantAgent,
        }
        agent_config = agent_data.to_dict()

        # 1. Check if the agent type is valid
        agent_type = (
            agent_config["agent_type"].value
            if isinstance(agent_config["agent_type"], Enum)
            else agent_config["agent_type"]
        )
        
        if agent_type not in agent_constructors:
            raise ValueError(f"Invalid agent type: {agent_type}")

        # 2. Craft agent_config that is compatible with AutoGen

        ## llm_config["config_list"] example:
        # config_list = [
        #     {
        #         "model": "gpt-4",
        #         "api_key": os.environ.get("AZURE_OPENAI_API_KEY"),
        #         "api_type": "azure",
        #         "base_url": os.environ.get("AZURE_OPENAI_API_BASE"),
        #         "api_version": "2024-02-01",
        #     },
        #     {
        #         "model": "gpt-3.5-turbo",
        #         "api_key": os.environ.get("OPENAI_API_KEY"),
        #         "api_type": "openai",
        #         "base_url": "https://api.openai.com/v1",
        #     },
        #     {
        #         "model": "llama-7B",
        #         "base_url": "http://127.0.0.1:8080",
        #     },
        # ]

        if "llm_config" in agent_config and agent_config["llm_config"] is not None:
            if not self.llm_configs:
                raise ValueError(
                    f"Cannot create AutoGen agent with LLM since the requested llm_config model name ${agent_config["llm_config"]} is not found in the provided llm configs: {self.llm_configs}"
                )
            llm_config = agent_config["llm_config"]
            if isinstance(llm_config, str):
                agent_config["llm_config"] = self.llm_configs.get(llm_config)
            elif isinstance(llm_config.get("config_list"), list):
                agent_config["llm_config"]["config_list"] = [
                    {"model": model_name, **self.llm_configs.get(model_name)}
                    for model_name in llm_config["config_list"]
                ]
        
        attributes_to_filter = [
            "name",
            "system_message",
            "is_termination_msg",
            "max_consecutive_auto_reply",
            "human_input_mode",
            "function_map",
            "code_execution_config",
            "llm_config",
            "default_auto_reply",
            "description",
            "chat_messages"
        ]

        agent_config = {
            attr: agent_config[attr] for attr in attributes_to_filter if (attr in agent_config and agent_config[attr] is not None)
        }

        # 3. Create the agent and return it
        if agent_type == "UserProxyAgent" and self.user_proxy:
            raise ValueError("Only one UserProxyAgent is allowed")

        autogen_agent: ConversableAgent = agent_constructors[agent_type](**agent_config)
        if agent_type == "UserProxyAgent":
            self.user_proxy: UserProxyAgent = autogen_agent
            self.user_proxy_data = agent_data

        # 4. register a callback hook so that the agent save every message to db before sending it
        autogen_agent.register_hook(
            "process_message_before_send", self.a_agent_save_message_and_send_ws
        )

        return autogen_agent

    async def a_agent_save_message_and_send_ws(
        self, sender: Agent, message: Union[Dict, str], recipient: Agent, silent=False
    ) -> Union[Dict, str]:
        """
        This is a hook function to be registered on an AutoGen ConverableAgent with register_hook() function.
        It will be appended to the agent's hooklist["process_message_before_send"].
        It must return the message to be processed further and to be sent by the sender agent.

        message (dict or str): message to be sent.
            The message could contain the following fields:
            - content (str or List): Required, the content of the message. (Can be None)
            - function_call (str): the name of the function to be called.
            - name (str): the name of the function to be called.
            - role (str): the role of the message, any role that is not "function"
                will be modified to "assistant".
            - context (dict): the context of the message, which will be passed to
                [OpenAIWrapper.create](../oai/client#create).
                For example, one agent can send a message A as:
        ```python
        {
            "content": lambda context: context["use_tool_msg"],
            "context": {
                "use_tool_msg": "Use tool X if they are relevant."
            }
        }
        """
        if sender.name not in self.agent_name_to_id:
            raise ValueError(f"Agent {sender.name} is not in the agent chat group")

        message_dict = message
        if isinstance(message_dict, str):
            message_dict = {
                "content": message,
                "role": "user" if sender.name == self.user_proxy.name else "assistant",
                "name": sender.name,
            }

        message_create = AgentGroupMessageCreate(
            group_id=self.group_data.id,
            sender_id=self.agent_name_to_id[sender.name],
            message=MessageContent(**message_dict),
        )

        _ = await user_create_agent_group_message(self.db, message_create)

        if self.websocket_conn and self.websocket:
            self.websocket_conn.send_message_to_client(message_dict, self.websocket)

        return message

    def _create_autogen_message(self, message_data: AgentGroupMessage):
        # Example message_data.message
        # {'content': 'Today is 2024-06-22. Write a blogpost about the stock price performance of Nvidia in the past month.',
        #   'role': 'user',
        #   'name': 'Admin'},
        # {'content': 'To write a blog post about the stock price performance of Nvidia in the past month, we would need the following information retrieved via Python code:\n\n1. Historical stock price data for Nvidia for the past month.\n2. Specific date range within the past month for analysis.\n3. Opening and closing prices of Nvidia stock for each trading day in the past month.\n4. Highest and lowest prices of Nvidia stock in the past month.\n5. Any significant events or news related to Nvidia that could have impacted its stock price in the past month.\n6. Calculations or analysis on the percent change in stock price over the past month.\n7. Visualization of Nvidia stock price performance in the past month (optional).',
        #   'role': 'user',
        #   'name': 'Planner'},
        return message_data.message

    def _initialize_agent_group_chat(self):
        agent_group_chat = GroupChat(
            name=self.group_data.name,
            agents=self.autogen_agents,
            messages=self.autogen_messages,
            max_round=self.group_data.max_round,
            speaker_selection_method=self.group_data.speaker_selection_method,
        )

        agent_group_chat_manager = GroupChatManager(
            groupchat=agent_group_chat,
            human_input_mode="TERMINATE",
            llm_config={
                "config_list": [self.llm_configs[self.group_manager_llm]],
                "cache_seed": None,
            },
        )
        return agent_group_chat_manager, agent_group_chat

    def start_chat(self, user_message: str):
        autogen_message = {
            "content": user_message,
            "role": "user",
            "name": self.user_proxy.name,
        }

        self.user_proxy.a_initiate_chat(
            self.autogen_agent_group_chat_manager, message=autogen_message
        )
