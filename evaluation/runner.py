from datetime import datetime
from statistics import mean, median

from evaluation.metrics.metric import Metric
from evaluation.model.question import (
    Experiment,
    ExperimentResult,
    Question,
    QuestionResult,
    Runtime,
)
from evaluation.utils import helpers


class Runner:

    def __init__(self, experiment: Experiment, metrics: list[Metric]):
        self.experiment = experiment
        self.metrics = metrics

    def run(self) -> ExperimentResult:
        helpers.activate_configuration(self.experiment.configuration)

        experiment_result = ExperimentResult(
            run_id=datetime.now().astimezone().strftime(
                "%Y%m%dT%H%M%S.%f%z"
            ),
            configuration=self.experiment.configuration,
        )

        for i,question in enumerate(self.experiment.questions, start=1):
            print(f"process question {i}/{len(self.experiment.questions)}", end="\r")
            question_result = self.process_question(question)
            experiment_result.question_results.append(question_result)
        print()

        experiment_result.metrics = self.aggregate_metrics(
            experiment_result.question_results
        )
        experiment_result.median_runtime = self.aggregate_runtimes(
            experiment_result.question_results
        )

        return experiment_result

    def process_question(self, question: Question) -> QuestionResult:
        question_result = helpers.execute_question(question)

        for metric in self.metrics:
            question_result.metrics[metric.name] = metric.evaluate(question_result)

        return question_result

    def aggregate_metrics(
        self,
        results: list[QuestionResult],
    ) -> dict[str, float | None]:
        aggregated: dict[str, float | None] = {}

        for metric in self.metrics:
            values = [
                result.metrics[metric.name]
                for result in results
                if result.metrics.get(metric.name) is not None
            ]
            aggregated[metric.name] = mean(values) if values else None

        return aggregated

    def aggregate_runtimes(
        self,
        results: list[QuestionResult],
    ) -> Runtime | None:
        if not results:
            return None

        def median_for(field_name: str) -> float | None:
            values = [
                value
                for result in results
                if (value := getattr(result.runtime, field_name)) is not None
                and value >= 0
            ]
            return median(values) if values else None

        total_runtime = median_for("total_runtime")
        if total_runtime is None:
            return None

        return Runtime(
            total_runtime=total_runtime,
            query_expansion_runtime=median_for("query_expansion_runtime"),
            retrieval_runtime=median_for("retrieval_runtime"),
            reranking_runtime=median_for("reranking_runtime"),
            context_building_runtime=median_for("context_building_runtime"),
            llm_call_runtime=median_for("llm_call_runtime"),
        )
