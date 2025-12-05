from google.adk.apps.app import EventsCompactionConfig
from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=4,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

events_compaction_config = EventsCompactionConfig(
    compaction_interval=3,
    overlap_size=1,
)

# basic eval criteria
# perfect tool trajectory is expected
# text should match - but the nature of random projects means
# this can be more lax
eval_config = {
    "criteria": {
        "tool_trajectory_avg_score": 1.0,
        "response_match_score": 0.2,
    }
}
