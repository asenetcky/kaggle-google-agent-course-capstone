from google.genai import types
from google.adk.apps.app import EventsCompactionConfig

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
