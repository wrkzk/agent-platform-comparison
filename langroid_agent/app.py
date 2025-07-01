#!/usr/bin/env python3

import langroid as lr
from langroid.agent.special import DocChatAgent, DocChatAgentConfig

# Define what document to use
documents =[
    "files/PlanCoverageInformation.pdf"
]

# Agent configuration
config = DocChatAgentConfig(
    name = "retrieval-agent",
    llm = lr.language_models.OpenAIGPTConfig(
        chat_model = lr.language_models.OpenAIChatModel.GPT4o,
        chat_context_length = 32_000,
        temperature = 0.2,
        stream = True,
    ),
    system_message = "Concisely answer my questions the documents. Start by asking me what I want to know.",
    doc_paths = documents,
)

# Run the agent
agent = DocChatAgent(config)
agent.ingest()
task = lr.Task(agent)
task.run()
