import os
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.tools import Tool
from langchain_community.graphs import Neo4jGraph
from langchain_community.chat_message_histories import Neo4jChatMessageHistory
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain import hub
from utils import get_session_id
from llm import llm
from graph import graph
from tools.vector import get_movie_plot


chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a book expert providing information about books."),
        ("human", "{input}"),
    ]
)

movie_chat = chat_prompt | llm | StrOutputParser()

tools = [
    Tool.from_function(
        name="General Chat",
        description="For general books chat not covered by other tools",
        func=movie_chat.invoke,
    ),
    Tool.from_function(
        name="Books Plot Search",
        description="For when you need to find information about books based on a plot",
        func=get_movie_plot,
    )
]


def get_memory(session_id):
    return Neo4jChatMessageHistory(session_id=session_id, graph=graph)


agent_prompt = hub.pull("hwchase17/react-chat")
agent = create_react_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
    )

chat_agent = RunnableWithMessageHistory(
    agent_executor,
    get_memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)

def generate_response(user_input):
    """
    Create a handler that calls the Conversational agent
    and returns a response to be rendered in the UI
    """

    response = chat_agent.invoke(
        {"input": user_input},
        {"configurable": {"session_id": get_session_id()}},)

    return response['output']
