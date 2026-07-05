import json
import time
import requests

from datetime import datetime
from pathlib import Path

URL = "http://127.0.0.1:8000/rag_chat"

questions_filepath = Path("./evaluation/questions.json")
results_filepath = Path("./evaluation/results.json")


if not questions_filepath.exists():
    raise FileNotFoundError("questions file not found.", questions_filepath)

with open(questions_filepath, "r") as fp:
    questions = json.load(fp)

total_entries = 0
total_satisfied = 0
total_time = []
questions_details = []

for i, question in enumerate(questions):
    print(f"run {i+1}/{len(questions)}", end="\r")
    data = {
        "user": "Wet0zelott",
        "message": question["question"]
    }

    start = time.time()
    response = requests.post(URL, json=data)
    response.raise_for_status()
    end = time.time()

    total_time.append(end - start)    

    # eval response
    entries = 0
    satisfied = 0

    if "must_contain" in question.keys():
        entries += len(question["must_contain"])
        for musts in question["must_contain"]:
            satisfied += 1 if musts.lower() in response.json()["message"].lower() else 0
        
    if "any_group" in question.keys():
        entries += len(question["any_group"])
        for anys in question["any_group"]:
            satisfied += 1 if any(a.lower() in response.json()["message"].lower() for a in anys) else 0
    
    details = {
        "question": question["question"],
        "answer": response.json()["message"],
        "retrieval_sources": response.json()["sources"],
        "score": round((satisfied / entries) * 100, 2)
    }
    questions_details.append(details)

    total_entries += entries
    total_satisfied += satisfied



result = {
    "run_id": str(datetime.now()),
    "llm_model": response.json()["llm_model"],
    "retrieval_model": response.json()["retrieval_model"],
    "chunk_size": response.json()["chunk_size"],
    "top_k": response.json()["top_k"],
    "context_builder": response.json()["context_builder"],
    "ranking": response.json()["ranking"],
    "median_runtime": round(total_time[int(len(total_time) / 2)], 2),
    "score": round((total_satisfied / total_entries) * 100, 2),
    "questions_details": questions_details
}

print("\ndone.")
    

# save in json
results = []

if results_filepath.exists():
    with open(results_filepath, "r", encoding='utf8') as fp:
        results = json.load(fp)

results.append(result)

with open(results_filepath, "w", encoding='utf8') as fp:
    json.dump(results, fp, indent=4)

print("saved.")


# print (ranking)
results.sort(reverse=True, key=lambda e: e["score"])

print("Ranking Top 3 ==========================")
for r in results[:3]:
    print(
        str(r["run_id"]),
        str(r["score"]) + " %",
        str(r["median_runtime"]) + " sec",
        str(r["llm_model"]) + " + " + str(r["retrieval_model"]),
        sep="\t"
    )

print("========================================")