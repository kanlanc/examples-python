from restack_ai.workflow import workflow, log, workflow_info
from dataclasses import dataclass, field
from .child import ChildWorkflow, ChildInput

@dataclass
class ParentInput:
    child: bool = field(default=True)

@workflow.defn()
class ParentWorkflow:
    @workflow.run
    async def run(self, input: ParentInput):
        if input.child:
            # use the parent run id to create child workflow ids
            parent_workflow_id = workflow_info().workflow_id

            log.info("Start ChildWorkflow and dont wait for result")
            result = await workflow.child_start(ChildWorkflow, input=ChildInput(name="world"), workflow_id=f"{parent_workflow_id}-child-start")
            
            log.info("Start ChildWorkflow and wait for result")
            result = await workflow.child_execute(ChildWorkflow, input=ChildInput(name="world"), workflow_id=f"{parent_workflow_id}-child-execute")
            log.info("ChildWorkflow completed", result=result)
            return "ParentWorkflow completed"
        
        else:
            log.info("ParentWorkflow without starting or executing child workflow")
            return "ParentWorkflow completed"
