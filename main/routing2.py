from pydantic import BaseModel
from typing import Literal
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain.prompts import ChatPromptTemplate 
from dotenv import load_dotenv
load_dotenv()
class RoutingDecision(BaseModel):
    """Decision to route the question based on grader output"""
    route:Literal["generate", "web_search"]
system="""
    You are a decision-making assistant in a question-answering system.
    Your job is to look at :
    1. A User question.
    2.A grading Summary that explains how relevant or useful the retrieved conten is.
    Based on these, you must decide if the information is :
    ###Input:
    Question: {{question}}
    Grader Summary: {{grader_summary}}
    ###Output:
    Improve Code Share Code Link
    Grader Summary: {{grader_summary}}
    ###Output:
    {{"route: "generate}} OR {{"route": "websearch}}"""
llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash-lite')
grade_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("human", "question: \n {question} \n\n User summary: {summary}"),
])


router=grade_prompt| llm.with_structured_output(RoutingDecision)
def second_route(state):
    print("--- SECOND ROUTE ---")
    #print("/n/n state inside second route", state)
    question = state["question" ]
    summary=state["grading_result"]
    path = router.invoke({
        "question": question,
        "summary": summary
    })
    if path.route == "web_search":
        print("---TO WEB SEARCH---")
        return "web_search"
    else :
        print("---Generate---")
        return "generate"
