import requests

QUESTIONS_PATH = "./data/demo_questions.txt"

url = "http://127.0.0.1:8000/rag_chat"

with open(QUESTIONS_PATH, "r") as fp:
    questions = [q.strip() for q in fp.readlines()]

for question in questions:
    data = {
        "user": "Wet0zelott",
        "message": question
    }

    response = requests.post(url, json=data)
    print(question)
    print(response.json())
    print()