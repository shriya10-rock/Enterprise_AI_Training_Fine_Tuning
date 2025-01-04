import openai
import json

# Set up OpenAI API Key
OPENAI_API_KEY = "your_openai_api_key"  # Replace with your actual OpenAI API key
openai.api_key = OPENAI_API_KEY

# Create Business-Specific Training Data
training_data = [
    {"prompt": "How should AI handle customer complaints?", "response": "AI should first acknowledge the complaint, show empathy, and provide actionable solutions."},
    {"prompt": "How does AI improve financial forecasting?", "response": "AI analyzes historical data to detect patterns, helping businesses predict future financial trends."},
    {"prompt": "What are best practices for AI automation in enterprises?", "response": "Best practices include continuous model evaluation, human feedback loops, and ethical AI implementation."},
    {"prompt": "How does reinforcement learning improve AI decision-making?", "response": "Reinforcement Learning enables AI models to learn optimal strategies by rewarding desirable behaviors over time."}
]

# Save training data as JSONL
with open("training_data.jsonl", "w") as f:
    for entry in training_data:
        f.write(json.dumps(entry) + "\n")

# Function to Generate GPT-4o Responses Using Training Data
def get_gpt4o_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI expert trained in enterprise AI automation."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]

# Test the Model Fine-Tuning
test_prompt = "How should AI handle customer complaints?"
response = get_gpt4o_response(test_prompt)
print(f"GPT-4o Response: {response}")
