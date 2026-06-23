import requests
import json

QUESTIONS_PATH = "./data/questions.json"

url = "http://127.0.0.1:8000/rag_chat"

with open(QUESTIONS_PATH, "r") as fp:
    questions = json.load(fp)

total_entries = 0
total_satisfied = 0

for question in questions:
    data = {
        "user": "Wet0zelott",
        "message": question["question"]
    }

    response = requests.post(url, json=data)

    # eval response
    entries = 0
    satisfied = 0

    if "must_contain" in question.keys():
        entries += len(question["must_contain"])
        for musts in question["must_contain"]:
            satisfied += 1 if musts in response.json()["message"] else 0
        
    if "any_of" in question.keys():
        entries += len(question["any_of"])
        for anys in question["any_of"]:
            satisfied += 1 if any(a in response.json()["message"] for a in anys) else 0
    
    total_entries += entries
    total_satisfied += satisfied
    
    print("===========================================================")
    print("question:", question["question"])
    print("answer:", response.json()["message"])
    print("score:", (satisfied / entries) * 100, "%")

print("\n\ntotal score:", (total_satisfied / total_entries) * 100, "%")