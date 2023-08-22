from prometheus_client import Counter, Histogram

# Declare google prometheus metrics
prom_namespace_okta = "symphony_module_okta"

INCOMING_MESSAGES = Counter(
    name="collected_messages",
    documentation="Number of messages collected from OKTA",
    namespace=prom_namespace_okta,
    labelnames=["intake_key"],
)

# Declare common prometheus metrics
prom_namespace = "symphony_module_common"

OUTCOMING_EVENTS = Counter(
    name="forwarded_events",
    documentation="Number of events forwarded to SEKOIA.IO",
    namespace=prom_namespace,
    labelnames=["intake_key"],
)

EVENTS_LAG = Histogram(
    name="events_lags",
    documentation="The delay, in seconds, from the date of the last event",
    namespace=prom_namespace,
    labelnames=["intake_key"],
)

FORWARD_EVENTS_DURATION = Histogram(
    name="events_forward_duration",
    documentation="Duration to collect and forward events from OKTA",
    namespace=prom_namespace,
    labelnames=["intake_key"],
)