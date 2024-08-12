import requests

def request_chat(api_endpoint, data):
    response = requests.post(api_endpoint, json=data)

    if response.status_code == 200:
        response_data =  response.json()
        # print(response_data)
        # print(f"{response_data["message"]}\n")
        return response_data
    print('Failed to get a response from Ollama API')
    return

api_endpoint = 'http://localhost:11434/api/chat'
data = {
    "model": "llama2",
    "messages": [
    ],
    "stream": False
}

chatbot_name = input("What would you like to name the bot?")
while True:
    # capture user input
    prompt = input("You: ")
    print(prompt)

    # update messages
    data["messages"].append({"role": "user", "content": prompt})
    print(data["messages"])

    # send chat to llm
    chat = request_chat(api_endpoint, data)
    data["messages"].append(chat["message"])

    # show response
    print(f"{chatbot_name}: {chat["message"]["content"]}")