from solution import Event, ListSink, Sink, route

e: Event = {"user_id": 1, "name": "click", "value": 2.5}
sink: Sink = ListSink()
n: int = route([e], sink, min_value=1.0)
m: int = route([e], sink)
bad_id: Event = {"user_id": "x", "name": "n", "value": 1.0}  # type: ignore
bad_value: Event = {"user_id": 1, "name": "n", "value": "high"}  # type: ignore
