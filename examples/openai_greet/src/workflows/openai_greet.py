from restack_ai.workflow import workflow, import_functions
from restack_ai import log
from dataclasses import dataclass
from datetime import timedelta

with import_functions():
    from src.functions.function import openai_greet, FunctionInputParams

@dataclass
class WorkflowInputParams:
    name: str

@workflow.defn(name="OpenaiGreetWorkflow")
class OpenaiGreetWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        user_content = f"Greet this person {input.name}"


        greet_message = await workflow.step(
            openai_greet,
            FunctionInputParams(
                user_content=user_content,
            ),
            start_to_close_timeout=timedelta(seconds=120)
        )
        log.info("Greet message", greet_message=greet_message)
        return greet_message
