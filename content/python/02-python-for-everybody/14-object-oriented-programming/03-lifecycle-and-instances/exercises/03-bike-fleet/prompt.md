Define two types.

`Bike(bike_id)` has attributes `bike_id` and `rented` (starts `False`).

`Fleet()` manages bikes:

- `add(bike)` registers a bike.
- `rent(bike_id)` marks it rented and returns `True`; returns `False` if it is already rented or the id is unknown.
- `bring_back(bike_id)` marks it available and returns `True`; returns `False` if the id is unknown or it was not rented.
- `available()` returns the sorted list of ids not currently rented.

The fleet should hold the very same `Bike` objects that were added, so `bike.rented` reflects fleet actions.
