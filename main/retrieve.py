from main.vectorStore import  retriever
from main.vectorStore import  retriever

def retrieve_node(state):
    print("---RETRIEVE ---")
    question = state["question"]                             
    print("question",question)
    messages = state.get('messages', [])
    documents = retriever.invoke(question)
    print("documents",documents)
    new_state={
        **state,
        "documents": documents,
        "question": question,
        "messages": messages
    }
    return new_state
