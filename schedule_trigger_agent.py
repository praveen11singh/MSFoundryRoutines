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
    routine_name="daily-summary",
    description="Runs a daily summary agent on weekday mornings.",
    enabled=True,
    triggers={
        "weekday-morning": {
            "type": "schedule",
            "cron_expression": "0 7 * * 1-5",  # required
            "time_zone": "UTC",                 # required
        }
    },
    action={
        "type": "invoke_agent_responses_api",
        "agent_name": agent_name,  # required
        # "conversation_id": "...",  # optional
    },
)

print(f"Routine created: {routine.name}, enabled={routine.enabled}")

# To use the Invocations API action instead:
# action={
#     "type": "invoke_agent_invocations_api",
#     "agent_name": agent_name,  # required
#     # "session_id": "...",      # optional
# }