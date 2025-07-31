from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI 
from dotenv import load_dotenv
from pydantic import Field, BaseModel 
from langchain_core.messages import HumanMessage
load_dotenv()

class GradeDocument (BaseModel):
    answer: str = Field(
    description="""reframe the vauge question into better question""",
    )

llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash-lite')
structured_llm=llm.with_structured_output (GradeDocument)
def transform_query(state):
    print("--- Transform Query---1")
    question=state['question']
    system="""You are a question rewriter that converts an input question to a better version for vector store retrieval.
     Look at the input and try to reason about the underlying meaning , If u still not understand the question route it to 
     
     
     """
    messages = state.get('messages', [])
    messages.append(HumanMessage(content=system))
    messages.append(HumanMessage(content=question))
    response=structured_llm.invoke(messages)
    rewritten_question = response.answer
    # Check if rewritten question indicates vagueness or inability to understand
    if "unable to understand" in rewritten_question.lower() or "vague" in rewritten_question.lower():
        state['unable_to_understand'] = True
        state['question'] = "unable to understand the question please explain"
    else:
        state['unable_to_understand'] = False
        state['question'] = rewritten_question
    state['messages'] = messages
    return state
