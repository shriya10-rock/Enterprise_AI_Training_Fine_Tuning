import openai
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Set OpenAI API Key
OPENAI_API_KEY = "your_openai_api_key"  # Replace with your actual OpenAI API key
openai.api_key = OPENAI_API_KEY

# Load a Pretrained Sentence Transformer Model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Business-Specific Knowledge Base
business_qa = [
    {"question": "How can AI optimize financial forecasting?", "answer": "AI analyzes historical data and detects patterns to predict future financial trends with high accuracy."},
    {"question": "What are AI use cases in HR and talent acquisition?", "answer": "AI helps screen resumes, conduct initial candidate assessments, and improve hiring decisions with predictive analytics."},
    {"question": "How does reinforcement learning improve AI decision-making?", "answer": "Reinforcement Learning helps AI agents learn optimal decision-making by receiving rewards based on actions taken in simulated environments."},
    {"question": "What are best practices for AI automation in enterprises?", "answer": "Best practices include continuous model evaluation, human feedback loops, and ethical AI implementation."}
]

# Convert Questions into Embeddings (Vector Representation)
questions = [q["question"] for q in business_qa]
question_embeddings = model.encode(questions)

# Store Embeddings in FAISS (Vector Search Database)
dimension = question_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(question_embeddings))

# Function to Retrieve the Most Relevant Business Knowledge
def retrieve_relevant_knowledge(user_query):
    query_embedding = model.encode([user_query])
    _, closest_match = index.search(np.array(query_embedding), 1)
    return business_qa[closest_match[0][0]]["answer"]

# Function to Improve GPT-4o Response Using Retrieval
def get_gpt4o_response(user_input):
    retrieved_knowledge = retrieve_relevant_knowledge(user_input)
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI expert trained in enterprise AI automation."},
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": f"Relevant knowledge retrieved: {retrieved_knowledge}"}
        ]
    )
    
    return response["choices"][0]["message"]["content"]

# Example Test
user_input = "Explain how AI can improve enterprise workflows."
response = get_gpt4o_response(user_input)
print("GPT-4o Response with Retrieval:", response)
