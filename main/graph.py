from langgraph.graph import StateGraph, START, END,add_messages
# Import your functions
from main.routing import route_question
from main.transform import transform_query
from main.retrieve import retrieve_node
from main.grader import grader_node
from main.generate import generate
from main.web_search import webSearch
from typing import Annotated, TypedDict, List
from langchain_core.documents import Document
from main.routing2 import second_route
import httpx

client=httpx.Client(verify=False)
# Step 1: Define Graph
# Initialize Graph
class GraphState(TypedDict):
    """
    Represents the state of our graph.
    Attributes:
        question: question generation: LL generation documents: list of documents
        question: str
        documents: List[Document]"""
    question: str
    documents: List[Document]
    generation:str
    grading_result: str 
    unable_to_understand: bool
    messages:Annotated[list,add_messages]
builder = StateGraph(GraphState)
builder.add_node("transform_query_node", transform_query)
builder.add_node ("web_search_node", webSearch)
builder.add_node("retrieve_node", retrieve_node)
#builder. add_node("synthesizer_node", synthesizer)
builder.add_node("grade_documents", grader_node)
builder.add_node( "generate_node", generate)
#builder. add_node("second_route", second_route)
# Add edges with conditions
builder.add_conditional_edges(
    START,
    route_question,
    {
    "vectorStore":"retrieve_node",
    'transformQuery':"transform_query_node"
    },
)
builder.add_edge("transform_query_node", "retrieve_node")
builder.add_edge("web_search_node", "generate_node")
builder.add_conditional_edges ("grade_documents", second_route, {
"generate":"generate_node",
"web_search": "web_search_node"
})
#builder. add_edge("grade_documents", "synthesizer_node")
builder.add_edge("retrieve_node", "grade_documents")
#builder. add
#builder. set_entry_point("route_question")
builder.set_finish_point("generate_node")
# Build final graph
print("before graph")
app = builder.compile()

config={
    "configurable":{
        "thread_id":1
    }
}

async def revoke_graph(question, messages=None):
    print("entered graph")
    if messages is None:
        messages = []
    # Check if app.invoke is a coroutine function
    import inspect
    if inspect.iscoroutinefunction(app.invoke):
        result = await app.invoke({'question': question, 'messages': messages}, config=config)
    else:
        # Fallback to synchronous call
        result = app.invoke({'question': question, 'messages': messages}, config=config)
    print("result", result['generation'])
    return result['generation']
#revoke_graph("which tablet used for stomach pain?")
