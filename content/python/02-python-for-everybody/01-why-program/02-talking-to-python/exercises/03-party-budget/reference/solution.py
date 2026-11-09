def party_budget(guests, cost_per_guest, venue_fee):
    total = guests * cost_per_guest
    total = total + venue_fee
    total = total + total / 10
    return total
