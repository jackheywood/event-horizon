from event_horizon.aggregates.light_aggregate import LightAggregate

# Not a real event store just yet, holding aggregates in memory just
# to prove out the command/handler/event/aggregate pattern
aggregates = {}


def get_aggregate(aggregate_id: str) -> LightAggregate:
    return aggregates[aggregate_id]


def save_aggregate(aggregate: LightAggregate):
    aggregates[aggregate.aggregate_id] = aggregate
