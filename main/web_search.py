from langchain_tavily import TavilySearch
from langchain_core.documents import Document

from dotenv import load_dotenv

load_dotenv()

web_search_tool=TavilySearch(k=6)

from langchain_tavily import TavilySearch
from langchain_core.documents import Document

from dotenv import load_dotenv

load_dotenv()

web_search_tool=TavilySearch(k=6)

def webSearch(state):
    """
    Web search based on the re-pharsed question.
    Args:
        state(dict): the current graph state

    Returns:
        state(dict): updates documents key with appended web results
    """
    print("----websearch----")
    global tries

    tries=0

    question=state['question']
    messages = state.get('messages', [])

    docs=web_search_tool.invoke({'query':question})

    print("docs in websearch",docs)

    new_state = {
        **state,
        'documents': docs,
        'question': question,
        'mode': 'web',
        'messages': messages
    }

    return new_state

