from autogen.agentchat import (
    ConversableAgent,
    UserProxyAgent,
    AssistantAgent,
    GroupChat,
    GroupChatManager,
)





from fastapi import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from dotenv import load_dotenv
import os, uuid, asyncio

from app.models import AgentGroup


from app.crud.agent import user_get_agent, user_create_agent
from app.crud.agent_group import user_get_agent_group, user_create_agent_group
from app.crud.agent_group_member import user_get_agent_group_members, user_create_agent_group_member
from app.crud.agent_group_message import user_get_agent_group_messages, user_create_agent_group_message

load_dotenv()

config_gpt_4o = {
    "model": os.environ.get("GPT_4O_MODEL"),
    "api_type": "azure",
    "api_key": os.environ.get("GPT_4O_API_KEY"),
    "base_url": os.environ.get("GPT_4O_AZURE_ENDPOINT"),
    "api_version": os.environ.get("GPT_4O_API_VERSION"),
}


config_gpt_4_turbo = {
    "model": os.environ.get("GPT_4_TURBO_MODEL"),
    "api_type": "azure",
    "api_key": os.environ.get("GPT_4_TURBO_API_KEY"),
    "base_url": os.environ.get("GPT_4_TURBO_AZURE_ENDPOINT"),
    "api_version": os.environ.get("GPT_4_TURBO_API_VERSION"),
}


config_gpt_35_turbo = {
    "model": os.environ.get("GPT_35_TURBO_MODEL"),
    "api_type": "azure",
    "api_key": os.environ.get("GPT_35_TURBO_API_KEY"),
    "base_url": os.environ.get("GPT_35_TURBO_AZURE_ENDPOINT"),
    "api_version": os.environ.get("GPT_35_TURBO_API_VERSION"),
}


def create_default_agents() -> List[ConversableAgent]:
    # user_proxy = UserProxyAgent(
    #     name="Human Admin",
    #     system_message="A human admin. Give the task, and send instructions to writer to refine the blog post.",
    #     code_execution_config=False,
    # )

    planner = AssistantAgent(
        name="Planner",
        system_message="""Planner. Given a task, please determine what information is needed to complete the task.
        Please note that the information will all be retrieved using Python code. Please only suggest information that can be retrieved using Python code.
        """,
        llm_config={"config_list": [config_gpt_4_turbo]},
    )

    engineer = AssistantAgent(
        name="Engineer",
        llm_config={"config_list": [config_gpt_4_turbo], "cache_seed": None},
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
            llm_config={"config_list": [config_gpt_4_turbo], "cache_seed": None},
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
        group_name: str = "Awesome Agent Group",
        websocket: WebSocket = None,
        agent_configs: List[dict] = [],
        max_round: int = 20,
        speaker_selection_method: str = "auto",
    ):
        self.db = db
        self.user_id = user_id
        self.websocket = websocket
        self.max_round = max_round
        
        # If group_id is given and we can retrieve a group chat by that id that is indeed created by the user_id
        # We'll take the group_id and ignore agents and agent_configs
        if group_id: 
            self.group = self.retrieve_agent_group(group_id)
            if self.group:
                self.agents = self.retrieve_group_agents()
                self.messages = self.retrieve_group_messages()
        # Otherwise, we create a new agent group and its agents from agent_configs
        if not self.group_id:
            self.group = self.create_agent_group()
            self.agents = self.create_group_agents(self.group_id, agent_configs)
            self.messages = []
            
        # Initialize the group chat and group chat manager    
        self.initialize_agent_group()
        
    async def retrieve_agent_group(self, group_id: int):
        group = await user_get_agent_group(self.db, self.user_id, group_id)
        if group:
            return group
        return None
    
    async def retrieve_group_agents(self):
        group_members = await user_get_agent_group_members(self.db, self.user_id, self.group.id)
        agents = []
        for member in group_members:
            agent = await user_get_agent(self.db, self.user_id, member.agent_id)
            if agent:
                agents.append(agent)
        return agents
    
    async def retrieve_group_messages(self):
        messages = await user_get_agent_group_messages(self.db, self.user_id, self.group.id)
        return messages
    
    # async def create_agent_group(self) -> int:
    #     agent_group_ceate = AgentGroupCreate(
            
    
    # async def create_group_agents(self, group_id: int, agent_configs: List[dict]):
    #     pass
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        self.client_sent_queue = asyncio.Queue()
        self.client_received_queue = asyncio.Queue()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        self.user_proxy = UserProxyAgentWeb(
            name = "User",
            human_input_mode = "ALWAYS",
            system_message = "User. You are the user. You can provide input to the agents. Giving them tasks and provide feedbacks.",
            max_consecutive_auto_reply = 5,
            is_terminal_msg = lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config = False,
        )
        self.user_proxy.set_queues(self.client_sent_queue, self.client_received_queue)
        
        self.agents = [self.user_proxy] + (agents if agents else create_default_agents())

        self.groupchat = GroupChat(
            agents=self.agents,
            messages=messages,
            max_round=max_round,
            speaker_selection_method="auto",
        )

        self.groupchat_manager = GroupChatManager(
            groupchat=self.groupchat,
            llm_config={"config_list": [config_gpt_4_turbo], "cache_seed": None},
            human_input_mode="ALWAYS",
        )
        
    async def start(self, message):
        await self.user_proxy.a_initiate_chat(
            self.groupchat_manager,
            clear_history = True,
            message = message
        )
