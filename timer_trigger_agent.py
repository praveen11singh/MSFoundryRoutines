import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv
load_dotenv()

endpoint = os.environ["PROJECT_ENDPOINT"]
agent_name = os.environ["AGENT_NAME"]

client = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())

# Using Responses API action
routine = client.beta.routines.create_or_update(
    routine_name="once-on-release-day",
    description="Runs the agent once on release day.",
    enabled=True,
    triggers={
        "release-day": {
            "type": "timer",
            "at": "2026-09-01T09:00:00Z",  # required
            # "time_zone": "UTC",           # optional; required when 'at' has no UTC offset
        }
    },
    action={
        "type": "invoke_agent_responses_api",
        "agent_name": agent_name,
    },
)

print(f"Routine created: {routine.name}, enabled={routine.enabled}")

# To use the Invocations API action instead:
# action={
#     "type": "invoke_agent_invocations_api",
#     "agent_name": agent_name,  # required
#     # "session_id": "...",      # optional
# }