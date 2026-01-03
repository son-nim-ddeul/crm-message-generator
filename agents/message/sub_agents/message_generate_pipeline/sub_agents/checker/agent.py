import logging
from collections.abc import AsyncGenerator
from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions

from ...types import MessageType

class EscalationChecker(BaseAgent):
    """Checks research evaluation and escalates to stop the loop if grade is 'pass'."""

    message_type: MessageType

    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        evaluation_result = ctx.session.state.get(f"{self.message_type.value}_evaluation")
        if evaluation_result and evaluation_result.get("grade") == "pass":
            logging.info(f"[{self.name}] Message evaluation passed. Escalating to stop loop.")
            yield Event(
                invocation_id=ctx.invocation_id,
                branch=ctx.branch,
                author=self.name, 
                actions=EventActions(escalate=True)
            )
        else:
            logging.info(f"[{self.name}] Message evaluation failed or not found. Loop will continue.")
            yield Event(
                invocation_id=ctx.invocation_id,
                branch=ctx.branch,
                author=self.name
            )
