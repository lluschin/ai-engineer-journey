import json
import time
import requests
import statistics

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
    
    retrieval_model = response.json()["retrieval_model"]
    used_sources = response.json()["used_sources"]
    retrieval_sources = response.json()["sources"][:used_sources]
 
    collection_name = "AiJourney_" + retrieval_model
    expected_chunks = question["expected_chunks"][collection_name]
    relevant_chunks = [r for r in retrieval_sources if r in expected_chunks]

    recall = -1
    precision = -1
    mrr = None

    if expected_chunks:
        recall = len(relevant_chunks) / len(expected_chunks)

        mrr = 0

        for rank, chunk in enumerate(retrieval_sources, start=1):
            if chunk in expected_chunks:
                mrr = 1.0 / rank
                break

    if retrieval_sources:
        precision = len(relevant_chunks) / len(retrieval_sources)

    details = {
        "question": question["question"],
        "answer": response.json()["message"],
        "used_sources": used_sources,
        "retrieval_sources": retrieval_sources,
        "score": round((satisfied / entries) * 100, 2),
        "recall@k": recall,
        "precision@k": precision,
        "mrr": mrr
    }
    questions_details.append(details)

    total_entries += entries
    total_satisfied += satisfied




macro_recall = [q["recall@k"] for q in questions_details if q["recall@k"] >= 0]
macro_recall = sum(macro_recall) / len(macro_recall)

macro_precision = [q["precision@k"] for q in questions_details if q["precision@k"] >= 0]
macro_precision = sum(macro_precision) / len(macro_precision)

macro_mrr = [q["mrr"] for q in questions_details if q["mrr"] >= 0]
macro_mrr = sum(macro_mrr) / len(macro_mrr)

result = {
    "run_id": str(datetime.now()),
    "llm_model": response.json()["llm_model"],
    "retrieval_model": response.json()["retrieval_model"],
    "chunk_size": response.json()["chunk_size"],
    "top_k": response.json()["top_k"],
    "context_builder": response.json()["context_builder"],
    "ranking": response.json()["ranking"],
    "median_runtime": statistics.median(total_time),
    "score": round((total_satisfied / total_entries) * 100, 2),
    "MacroRecall": macro_recall,
    "MacroPrecision": macro_precision,
    "MacroMRR": macro_mrr,
    "questions_details": questions_details
}

print("\ndone.")

def print_run(r):
    print(
        str(r["run_id"]) + " " + str(r["llm_model"]) + " + " + str(r["retrieval_model"]),
        "Answer Score:\t" + str(r["score"]) + " %",
        "Median Runtime" + str(r["median_runtime"]) + " sec",
        f"Macro Recall@{str(r["top_k"])}" + str(r["MacroRecall"]),
        f"Macro Precision@{str(r["top_k"])}" + str(r["MacroPrecision"]),
        "Macro MRR" + str(r["MacroMRR"]),
    )

print_run(result)

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
    print_run(r)
    print("\n\n")
print("========================================")