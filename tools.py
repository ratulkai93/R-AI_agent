from langchain_community.tools import WikipediaQueryRun,DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import Tool #langchain.tool is deprecated -> used langchain_core.tools
from datetime import datetime 

#func to add timestamp to output txt file
def data_to_txt(data: str, filename: str = "search_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Search Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {filename}"

#saving data to txt file tool
save_data_tool= Tool(
    name= "save_data_to_file",
    func=data_to_txt,
    description= "Saves structured data to a text file."
)

#for web search tool using ddg
search= DuckDuckGoSearchRun()
search_data_tool= Tool(
    name= "duckduckgo search",
    func= search.run, 
    description= "Search the web for info.",
)
#for wiki result
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wiki_data_tool= WikipediaQueryRun(api_wrapper=api_wrapper)

