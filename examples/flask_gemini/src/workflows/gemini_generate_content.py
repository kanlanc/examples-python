from restack_ai.workflow import workflow, import_functions
from restack_ai import log
from dataclasses import dataclass
from datetime import timedelta

with import_functions():
    from src.functions.function import gemini_generate, FunctionInputParams

@dataclass
class WorkflowInputParams:
    user_content: str

@workflow.defn(name="GeminiGenerateWorkflow")
class GeminiGenerateWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        log.info("Workflow input", input=input)
        result = await workflow.step(gemini_generate, FunctionInputParams(user_content=input.user_content), start_to_close_timeout=timedelta(seconds=120))
        log.info("Workflow result", result=result)
        return result
