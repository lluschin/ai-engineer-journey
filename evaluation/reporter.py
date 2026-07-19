from pathlib import Path

from evaluation.model.question import ExperimentResult


class ExperimentReporter:

    def __init__(self, output_directory: str | Path):
        self.output_directory = Path(output_directory)

    def report(self, result: ExperimentResult) -> Path:
        serialized_result = result.model_dump_json(indent=2)
        self.print_summary(result)

        self.output_directory.mkdir(parents=True, exist_ok=True)
        result_filepath = self.output_directory / f"{result.run_id}.json"
        result_filepath.write_text(
            serialized_result + "\n",
            encoding="utf-8",
        )

        return result_filepath

    def print_summary(self, result: ExperimentResult) -> None:
        rows: list[tuple[str, str]] = [
            ("run_id", result.run_id),
            ("question_count", str(len(result.question_results))),
        ]
        rows.extend(
            (
                f"configuration.{name}",
                self.format_value(value),
            )
            for name, value in result.configuration.model_dump().items()
        )
        rows.extend(
            (
                f"metrics.{name}",
                self.format_value(value),
            )
            for name, value in result.metrics.items()
        )

        if result.median_runtime is not None:
            rows.extend(
                (
                    f"median_runtime.{name}",
                    self.format_value(value),
                )
                for name, value in result.median_runtime.model_dump().items()
            )

        key_width = max(len("Member"), *(len(key) for key, _ in rows))
        value_width = max(len("Value"), *(len(value) for _, value in rows))
        separator = f"+-{'-' * key_width}-+-{'-' * value_width}-+"

        print(separator)
        print(f"| {'Member':<{key_width}} | {'Value':<{value_width}} |")
        print(separator)
        for key, value in rows:
            print(f"| {key:<{key_width}} | {value:<{value_width}} |")
        print(separator)

    @staticmethod
    def format_value(value: object) -> str:
        if value is None:
            return "-"
        if isinstance(value, float):
            return f"{value:.6f}"
        return str(value)
