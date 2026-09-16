import os
import argparse
import json
from pathlib import Path
from ollama import Client

from src.utils.registry import ServiceRegistry


def parse_args() -> list[Path]:
    def check_filepath(filepath: Path):
        if not filepath.exists():
            parser.error(f"file \"{filepath}\" was not found.")
    
        if not filepath.is_file():
            parser.error(f"\"{filepath}\" needs to be a file.")

    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        required=True,
        help="configuration file for RAG features.",
        )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        required=True,
        help="base file for annotating questions.",
        )
    parser.add_argument(
            "-o",
            "--output",
            type=Path,
            required=True,
            help="output filepath to create.",
        )

    args = parser.parse_args()
    check_filepath(args.config)
    check_filepath(args.input)

    return [args.config, args.input, args.output]


def annotate():
    configFilePath, inputFilePath, outputFilePath = parse_args()

    registry = ServiceRegistry()
    registry.load_settings_file(str(configFilePath))

    with open(inputFilePath, 'r') as fp:
        inputQuestions = json.load(fp)

    client = Client()
    
    for i, question in enumerate(inputQuestions):
        if not "expected_chunks" in question:
            question["expected_chunks"] = {}

        collectionName = registry.retrieval_service.qdrant.collection_name
        if collectionName in question["expected_chunks"]:
            continue

        question["expected_chunks"][collectionName] = []

        while True:
            points, offset = registry.retrieval_service.get_next_entries()

            # check points
            for j, point in enumerate(points):
                os.system('clear')
                print(f'questions - {i+1} / {len(inputQuestions)}')
                print(f'chunks - {j+1} / {len(points)}')
                print(question['question'], f'({len(question['expected_chunks'][collectionName])})', end='\n\n')
                print(point.payload['Infotext'], end='\n\n')
        
                prompt = f"""
                look at the following chunk and check if it answers the given question fully or partially.
                Just answer with "yes" if the chunk answers the question fully or partially, otherwise answer with "no"
        
                question:
                {question['question']}
        
                chunk:
                {point.payload['Infotext']}
                """
        
                response = client.chat(
                    model='qwen3:8b',
                    messages=[{'role': 'user', 'content': prompt}]
                )
        
                aws = response.message.content
                aws = aws.strip().lower()
        
                print("AI says", aws)
                import time; time.sleep(1)
        
                if aws == 'yes':
                    question['expected_chunks'][collectionName].append(point.id)


            if offset is None:
                break#


    with open(outputFilePath, "w", encoding="utf-8") as fp:
        json.dump(inputQuestions, fp, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    annotate()