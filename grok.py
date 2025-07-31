import os
from dotenv import load_dotenv
from xai import XAIClient

# Load environment variables from .env file
load_dotenv()

# # Initialize the xAI client with the API key
# client = XAIClient(api_key=os.getenv("XAI_API_KEY"))

# Function to invoke Grok LLM
def invoke_grok(prompt):
    try:
        response = client.chat.completions.create(
            model="grok-3",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
if __name__ == "__main__":
    prompt = "Hello, Grok! What's the capital of France?"
    result = invoke_grok(prompt)
    print(result)