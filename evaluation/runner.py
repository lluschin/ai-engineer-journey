from datetime import datetime
from statistics import mean, median

from evaluation.model.question import (
    Experiment,
    ExperimentResult,
    Question,
    QuestionResult,
    Runtime,
)
from evaluation.utils import helpers

from src.utils.models.stage_model import StageIdx


class Runner:

    def __init__(self, experiment: Experiment):
        self.experiment = experiment

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

        for metric in self.experiment.metrics:
            question_result.metrics[metric.name] = metric.evaluate(question_result)

        return question_result

    def aggregate_metrics(
        self,
        results: list[QuestionResult],
    ) -> dict[str, float | None]:
        aggregated: dict[str, float | None] = {}

        for metric in self.experiment.metrics:
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

        def median_for(stage_name: str) -> float | None:

            values: list[float] = list()
            for result in results:
                for stage in result.chat_response.stages:
                    if stage.name == stage_name:
                        if stage.runtime < 0.0:
                            print("WARNING: runtime value out of bounce in stage", stage_name)
                        else:
                            values.append(stage.runtime)
            
            return median(values) if values else None

        total_runtime = [r.request_runtime for r in results]
        total_runtime = median(total_runtime)

        stage_runtimes = {
            stages: median_for(stages)
            for stages in (
                StageIdx.QUERY_EXPANDER,
                StageIdx.RETRIEVAL_STAGE,
                StageIdx.RANKING_STAGE,
                StageIdx.COMPRESSOR_STAGE,
                StageIdx.CONTEXT_BUILDER,
                StageIdx.LLM_STAGE,
            )
        }

        return Runtime(
            total_runtime=total_runtime,
            stage_runtimes=stage_runtimes,
        )
