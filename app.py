from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import json
from langchain_core.messages import HumanMessage

app = FastAPI()

# Maintain conversation history in memory (simple implementation)
conversation_history = []

# Simulated backend logic (replace this with real LangGraph logic)
async def get_answer(question):
    from main.graph import revoke_graph
    global conversation_history
    # Append user question as HumanMessage
    conversation_history.append(HumanMessage(content=question))
    # Pass conversation history to revoke_graph
    response = await revoke_graph(question, messages=conversation_history)
    # Extract string content if response is AIMessage
    if hasattr(response, 'content'):
        bot_content = response.content
    else:
        bot_content = str(response)
    # Append bot response as HumanMessage
    conversation_history.append(HumanMessage(content=bot_content))
    return response

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Pharma Chatbot</title>
            <style>
                body {
                    font-family: 'Segoe UI', sans-serif;
                    background-color: #f0f2f5;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    flex-direction: column;
                    height: 100vh;
                }

                .chat-container {
                    flex: 1;
                    display: flex;
                    flex-direction: column;
                    padding: 20px;
                    overflow-y: auto;
                }

                .message {
                    max-width: 70%;
                    padding: 10px 15px;
                    margin: 10px 0;
                    border-radius: 10px;
                    line-height: 1.5;
                }

                .user {
                    background-color: #dcf8c6;
                    align-self: flex-end;
                    text-align: right;
                }

                .bot {
                    background-color: #ffffff;
                    align-self: flex-start;
                    border: 1px solid #ccc;
                }

                .input-box {
                    display: flex;
                    padding: 15px;
                    background-color: #ffffff;
                    border-top: 1px solid #ccc;
                }

                input[type="text"] {
                    flex: 1;
                    padding: 10px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    font-size: 16px;
                }

                button {
                    padding: 10px 20px;
                    margin-left: 10px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-size: 16px;
                    cursor: pointer;
                }

                button:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>
            <div class="chat-container" id="chat"></div>
            <div class="input-box">
                <input type="text" id="question" placeholder="Type your question..." />
                <button onclick="sendMessage()">Send</button>
            </div>

            <script>
                async function sendMessage() {
                    const input = document.getElementById('question');
                    const question = input.value.trim();
                    if (!question) return;

                    appendMessage(question, 'user');
                    input.value = '';
                    
                    try {
                        const response = await fetch('/ask', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ question })
                        });

                        const data = await response.json();
                        appendMessage(data.answer, 'bot');
                    } catch (err) {
                        appendMessage('Error getting response.', 'bot');
                    }
                }

                function appendMessage(text, sender) {
                    const chat = document.getElementById('chat');
                    const msg = document.createElement('div');
                    msg.className = 'message ' + sender;
                    msg.innerText = text;
                    chat.appendChild(msg);
                    chat.scrollTop = chat.scrollHeight;
                }
            </script>
        </body>
    </html>
    """

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    question = data.get("question", "")
    answer = await get_answer(question)
    return {"answer": str(answer)}
