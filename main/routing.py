from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI

from pydantic import BaseModel,Field
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from typing import Literal

load_dotenv()

class RouteQuery(BaseModel):
    """
    Route a user query to the most relevant data source
    """
    datasource:Literal['vectorStore','transformQuery']=Field(
        description="choose where the query should go: vectorStore or transformQuery"
    )

llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite")

system="""
you are a routing system . your job is to classify user question into exactly one of the following .

possible values for 'datasource':
1."vectorStore"- if the question is well structured and model able to understand .
2."transformQuery"-for a unclear, vauge , or misspelled questions.

Examples:

User:what is diabetes?
->{{"datasource":vectorStore}}
User:what is disis?
->{{"datasource":"transform_query"}}

Rules:
-Do not include explanation or extra text.

-If the question is unclear , deafault to :{{datasource:"transform_query"}}
"""
route_prompt=ChatPromptTemplate.from_messages([
    ("system",system),
    ("human",'{question}')
])

structured_llm_router=route_prompt|llm.with_structured_output(RouteQuery)

def route_question(state):
    print("--route question--")
    source = structured_llm_router.invoke({"question":state['question']})

    state['datasource']=source

    if source.datasource=="vectorStore":
        print("---Route question to RAG---")

        return "vectorStore"
    if source.datasource=='transformQuery':
        print("---Route question to transform query---")

        return 'transformQuery'
