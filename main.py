from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import string

app = FastAPI()

# Allow CORS for the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to the specific origin of your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")

def load_data(filename: str):
    with open(filename, 'r') as file:
        lines = file.read().strip().split('\n\n')

    qa_pairs = {}
    for line in lines:
        question, answer = line.split('\n', 1)
        question = question.strip().lower().translate(str.maketrans('', '', string.punctuation))
        qa_pairs[question] = answer.strip()

    return qa_pairs

qa_pairs = load_data('data.txt')

class Message(BaseModel):
    text: str

@app.post("/chat/")
async def chat(message: Message):
    response = generate_response(message.text)
    return {"response": response}

def generate_response(message: str) -> str:
    message = message.strip().lower().translate(str.maketrans('', '', string.punctuation))
    # Find the best matching response
    for question in qa_pairs:
        if question in message:
            return qa_pairs[question]

    return "I'm not sure how to respond to that."

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
