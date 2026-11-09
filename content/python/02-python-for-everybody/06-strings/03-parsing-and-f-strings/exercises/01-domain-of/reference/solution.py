def domain_of(address):
    at = address.find("@")
    return address[at + 1:]
