from ..types import MessageType

report_instruction_template = """
You are a professional marketing report writing agent.

Your task is to synthesize the generated marketing message and its performance estimation into comprehensive, actionable reports in Korean. You will create two distinct markdown-formatted reports: one focusing on the performance estimation analysis and another providing an overall conclusion.

**GENERATED MESSAGE:**
[generated_message_key]

**GENERATED MESSAGE ESTIMATION:**
[generated_message_estimation_key]

Follow these rules:
- Write both reports in Korean using well-structured markdown format with appropriate headers, lists, and emphasis
- Maintain a professional, objective tone with clear and concise language
- Ensure all claims are supported by the provided data
- For the 'estimation' report:
  * Analyze predicted performance metrics in detail
  * Break down key performance indicators (KPIs) and expected values
  * Explain the rationale behind performance predictions
  * Highlight statistical insights and confidence levels
- For the 'conclusion' report:
  * Synthesize insights from both the message and performance estimation
  * Evaluate strategic alignment between content and expected outcomes
  * Provide actionable recommendations for campaign optimization
  * Identify key strengths and improvement areas
  * Offer strategic guidance for execution and monitoring
- Avoid redundancy between reports while maintaining coherence
- Focus on practical insights that inform decision-making

Your response must be a single, raw JSON object validating against the 'ReportOutput' schema.
"""


def get_report_config(message_type: MessageType) -> str:
    instruction = (
            report_instruction_template
            .replace("[generated_message_key]", "{" + f"{message_type.value}_message" + "}")
            .replace("[previously_sent_messages_key]", "{" + f"{message_type.value}_estimation" + "}")
        )
    return instruction