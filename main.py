from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor #agents function got deprecated, installed langchain-classic
from tools import search_data_tool, wiki_data_tool, save_data_tool

load_dotenv()

#model for the response output
class PromptResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools: list[str]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash", #limited prompts // subject to change
    max_retries=1,
    )
#basic prompt and answer 
# response= llm.invoke("what is the meaning of success?") 
# print(response)

response_parser= PydanticOutputParser(pydantic_object=PromptResponse)
prompt= ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a helpful AI assistant.
            Answer the user query and use neccessary tools. 
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=response_parser.get_format_instructions())

tools= [search_data_tool,wiki_data_tool, save_data_tool] 
agent = create_tool_calling_agent(
    llm = llm,
    prompt= prompt,
    tools=tools
)

agent_executor= AgentExecutor(agent=agent, tools=tools,verbose=True)
query=input("What would you like to search today? \n")
raw_response= agent_executor.invoke({"query":query})
# print(raw_response)

try:
    structured_response= response_parser.parse(raw_response.get("output")[0]["text"])
    print(structured_response)
except Exception as e:
    print("Error: Could not parse response",e,"Raw Response -", raw_response)

