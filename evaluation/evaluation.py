import argparse
import json
from pathlib import Path
from typing import Any, Sequence

from evaluation.metrics.mrr_metric import MRRMetric
from evaluation.metrics.precision_metric import PrecisionMetric
from evaluation.metrics.recall_metric import RecallMetric
from evaluation.metrics.score_metric import ScoreMetric
from evaluation.model.question import Experiment, Question
from evaluation.reporter import ExperimentReporter
from evaluation.runner import Runner
from evaluation.utils.helpers import load_configuration


def load_questions(
    questions_filepath: str | Path,
    retrieval_model: str,
) -> list[Question]:
    filepath = Path(questions_filepath)

    if not filepath.is_file():
        raise FileNotFoundError(f"Questions file not found: {filepath}")

    with filepath.open(encoding="utf-8") as file:
        question_data = json.load(file)

    if not isinstance(question_data, list):
        raise ValueError("Questions file must contain a JSON list.")

    return [
        create_question(data, retrieval_model, index)
        for index, data in enumerate(question_data, start=1)
    ]


def create_question(
    data: Any,
    retrieval_model: str,
    index: int,
) -> Question:
    if not isinstance(data, dict):
        raise ValueError(f"Question {index} must be a JSON object.")

    question_data = dict(data)
    question_data["expected_chunks"] = resolve_expected_chunks(
        question_data.get("expected_chunks", []),
        retrieval_model,
        index,
    )

    return Question.model_validate(question_data)


def resolve_expected_chunks(
    expected_chunks: Any,
    retrieval_model: str,
    question_index: int,
) -> list[str]:
    if isinstance(expected_chunks, list):
        return expected_chunks

    if not isinstance(expected_chunks, dict):
        raise ValueError(
            f"'expected_chunks' of question {question_index} "
            "must be a list or an object."
        )

    possible_keys = (
        f"AiJourney_{retrieval_model}",
        retrieval_model,
    )

    for key in possible_keys:
        if key in expected_chunks:
            chunks = expected_chunks[key]
            if not isinstance(chunks, list):
                raise ValueError(
                    f"Expected chunks for '{key}' in question "
                    f"{question_index} must be a list."
                )
            return chunks

    available_keys = ", ".join(expected_chunks) or "none"
    raise ValueError(
        f"No expected chunks found for retrieval model "
        f"'{retrieval_model}' in question {question_index}. "
        f"Available keys: {available_keys}"
    )


def create_experiment(
    config_filepath: str | Path,
    questions_filepath: str | Path,
) -> Experiment:
    configuration = load_configuration(str(config_filepath))
    questions = load_questions(
        questions_filepath,
        configuration.retrieval_model,
    )

    return Experiment(
        configuration=configuration,
        questions=questions,
    )


def create_runner(experiment: Experiment) -> Runner:
    return Runner(
        experiment=experiment,
        metrics=[
            ScoreMetric(),
            RecallMetric(),
            PrecisionMetric(),
            MRRMetric(),
        ],
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Evaluate a RAG configuration against a question dataset."
    )
    parser.add_argument(
        "--config",
        required=True,
        type=Path,
        help="Path to the TOML configuration.",
    )
    parser.add_argument(
        "--questions",
        required=True,
        type=Path,
        help="Path to the questions JSON file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("evaluation/results"),
        help=(
            "Directory for result files "
            "(default: evaluation/results)."
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    experiment = create_experiment(args.config, args.questions)
    result = create_runner(experiment).run()
    result_filepath = ExperimentReporter(args.output_dir).report(result)
    print(f"\nResult saved to {result_filepath}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
