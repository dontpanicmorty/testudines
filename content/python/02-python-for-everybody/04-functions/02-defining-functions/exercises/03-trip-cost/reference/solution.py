def trip_cost(distance_km, litres_per_100km, price_per_litre):
    litres_used = distance_km / 100 * litres_per_100km
    return litres_used * price_per_litre
