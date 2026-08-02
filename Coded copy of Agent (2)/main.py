from datetime import (
    datetime,
    timezone
)
from langchain_core.messages import (
    HumanMessage,
    SystemMessage
)
from pydantic import (
    BaseModel,
    Field
)
from pydantic import (
    ConfigDict
)
from typing import (
    Sequence
)
from uipath.agent.react import (
    AGENT_SYSTEM_PROMPT_TEMPLATE
)
from uipath_langchain.agent.react import (
    create_agent
)
from uipath_langchain.chat.chat_model_factory import (
    get_chat_model
)
from utils import (
    interpolate_legacy_message
)



# LLM Model Configuration
llm = get_chat_model(
    model='gpt-5.4',
    temperature=0.0,
    max_tokens=128000,
    agenthub_config="agentsruntime",
)
    

# Collect all tools
tools = []


# Input/Output Models
class AgentInput(BaseModel):
    model_config = ConfigDict(extra='allow')


class AgentOutput(BaseModel):
    model_config = ConfigDict(extra='allow')
    content: str | None = Field(None, description="Output content")

# Agent Messages Function
def create_messages(state: AgentInput) -> Sequence[SystemMessage | HumanMessage]:
    # Apply system prompt template
    current_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    system_prompt_content = """You are an agentic assistant."""
    system_prompt_content = interpolate_legacy_message(system_prompt_content, state.model_dump())
    enhanced_system_prompt = (
        AGENT_SYSTEM_PROMPT_TEMPLATE
        .replace('{{systemPrompt}}', system_prompt_content)
        .replace('{{currentDate}}', current_date)
        .replace('{{agentName}}', 'Mr Assistant')
    )

    return [
        SystemMessage(content=enhanced_system_prompt),
        HumanMessage(content=interpolate_legacy_message("""What is the current date?""", state.model_dump())),
    ]

# Create agent graph
graph = create_agent(model=llm, messages=create_messages, tools=tools, input_schema=AgentInput, output_schema=AgentOutput)