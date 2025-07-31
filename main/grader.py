from pydantic import BaseModel,Field
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

class GradeDocument(BaseModel):
    "Binary score for relevance check on retrieved documents and answer the user question based on documents"
    binary_score:str=Field(
        description='documents are relevant to the question , "yes" or "no"'
    )
    answer:str=Field(
        description="The answer to the user question, Which is based on the given sources ."
    )

llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash-lite')

structured_llm_grader=llm.with_structured_output(GradeDocument)

system="""
    you are a grader assessing relevance of a retrieved document to a user question. if the document contain keywords or semantic meaning 
    related to the user question . The goal is to filter out erroeneous retrieval.
    Give a binary score 'yes' or 'No' score to indicate whether the document is relevant to the question and generates concise answer to the 
    question if the document is relevant based on the given query

"""

grade_prompt=ChatPromptTemplate.from_messages([
    ("system",system),
    ("human","Retrieved document : \n\n {documents} \n\n User question {question}")
]
)

retrieval_grader=grade_prompt | structured_llm_grader

from pydantic import BaseModel,Field
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

class GradeDocument(BaseModel):
    "Binary score for relevance check on retrieved documents and answer the user question based on documents"
    binary_score:str=Field(
        description='documents are relevant to the question , "yes" or "no"'
    )
    answer:str=Field(
        description="The answer to the user question, Which is based on the given sources ."
    )

llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash-lite')

structured_llm_grader=llm.with_structured_output(GradeDocument)

system="""
    you are a grader assessing relevance of a retrieved document to a user question. if the document contain keywords or semantic meaning 
    related to the user question . The goal is to filter out erroeneous retrieval.
    Give a binary score 'yes' or 'No' score to indicate whether the document is relevant to the question and generates concise answer to the 
    question if the document is relevant based on the given query

"""

grade_prompt=ChatPromptTemplate.from_messages([
    ("system",system),
    ("human","Retrieved document : \n\n {documents} \n\n User question {question}")
]
)

retrieval_grader=grade_prompt | structured_llm_grader

def grader_node(state):
    print("---Grader---")
    document=state['documents']
    question=state['question']
    # Pass a dict with keys matching prompt variables, not a list of messages
    result=retrieval_grader.invoke({
        "documents": document,
        "question": question
    })
    print("grading result",result)

    state["grading_result"]=result.answer
    # Optionally update messages if needed, but do not pass messages to invoke
    return state
