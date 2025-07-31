from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv 
load_dotenv()

system = """You are a pharmaceutical business analyst with expertise in regulatory affairs and clinic
Instructions:
1. Assess relevance: Determine if the content provides insight that helps answer the question.
2. Extract insights: If relevant, extract the key clinical, regulatory, or commercial milestone menti
3. Provide clear and concise answers without citations or legends.
4. Synthesize where needed: If multiple documents reinforce or complement a point, synthesize the inf
5. Avoid redundancy: Prioritize precision and avoid repeating similar points across sources.
Final Output Format:
- Structure your response in short paragraphs or bullet points for readability.
- Ensure the answer is crisp, professional, and aligned with the needs of strategic pharmaceutical de
- Do not include citations or a Legend in the response.
  Ready?"""
prompt=ChatPromptTemplate.from_messages (
    [
("system", system), 
("human","Question: \n\n {question} \n\n Context: {doc_content}"),
    ]
)
llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash-lite' )
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv 
load_dotenv()

system = """You are a pharmaceutical business analyst with expertise in regulatory affairs and clinic
Instructions:
1. Assess relevance: Determine if the content provides insight that helps answer the question.
2. Extract insights: If relevant, extract the key clinical, regulatory, or commercial milestone menti
3. Provide clear and concise answers without citations or legends.
4. Synthesize where needed: If multiple documents reinforce or complement a point, synthesize the inf
5. Avoid redundancy: Prioritize precision and avoid repeating similar points across sources.
Final Output Format:
- Structure your response in short paragraphs or bullet points for readability.
- Ensure the answer is crisp, professional, and aligned with the needs of strategic pharmaceutical de
- Do not include citations or a Legend in the response.
  Ready?"""
prompt=ChatPromptTemplate.from_messages (
    [
("system", system), 
("human","Question: \n\n {question} \n\n Context: {doc_content}"),
    ]
)
llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash-lite' )

def generate(state):
    """Generate Answer
    Args:
        state (dict): The current graph state
    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """
    print("---GENERATE---")
    question = state["question" ]
    documents = state["documents"]
    # Only use final question and documents for generation, ignore messages list
    prompt_str = prompt.format(question=question, doc_content=documents)
    generation_response = llm.invoke(prompt_str)
    # Extract only the content part if the response is an object
    if hasattr(generation_response, 'content'):
        generation = generation_response.content
    elif isinstance(generation_response, dict) and 'content' in generation_response:
        generation = generation_response['content']
    else:
        generation = generation_response
    # Check if generation indicates vagueness or inability to understand
    if "unable to understand" in generation.lower() or "vague" in generation.lower():
        state['unable_to_understand'] = True
        state['generation'] = "unable to understand the question please explain"
    else:
        state['unable_to_understand'] = False
        state['generation'] = generation
    return state
