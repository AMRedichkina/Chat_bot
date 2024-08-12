import os
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.tools import Tool
from langchain_community.graphs import Neo4jGraph
from langchain_community.chat_message_histories import Neo4jChatMessageHistory
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain import hub
from langchain_core.prompts import PromptTemplate
from utils import get_session_id
from llm import llm
from graph import graph
from tools.vector import get_book_plot
from tools.cypher import cypher_qa


chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a book expert providing information about books."),
        ("human", "{input}"),
    ]
)

book_chat = chat_prompt | llm | StrOutputParser()

tools = [
    Tool.from_function(
        name="General Chat",
        description="For general books chat not covered by other tools",
        func=book_chat.invoke,
    ),
    Tool.from_function(
        name="Books Plot Search",
        description="For when you need to find information about books based on a plot or find the book if it's not covered by other tools",
        func=get_book_plot,
    ),
    Tool.from_function(
        name="Book information",
        description="Search for books based on author, genre, rating, year, recommend the book (you have to find one random book) or provide detailed book information using Cypher queries",
        func=cypher_qa,
    )
]


def get_memory(session_id):
    return Neo4jChatMessageHistory(session_id=session_id, graph=graph)


agent_prompt = PromptTemplate.from_template("""
The chatbot, modeled as a librarian, should display traits such as attentiveness, thoroughness, and a deep passion for literature.
Your responses should only include information about books that are present in the Neo4j database. Just like a librarian who might share interesting facts or stories about a book in the Neo4j database or author, the chatbot should be able to weave narratives that engage the user, enhancing the interaction with cultural and historical context where appropriate.
Do not answer any questions using your pre-trained knowledge, only use the information available in the Neo4j database.
Do not answer any questions that do not relate to books, authors, or genres.

Do not answer any questions using your pre-trained knowledge, only use the information provided in the context from the database.

TOOLS:
------

You have access to the following tools:

{tools}

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```

Begin!

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}
""")

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
