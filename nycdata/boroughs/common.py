borough_number = {
    1: 'Manhattan',
    2: 'Bronx',
    3: 'Brooklyn',
    4: 'Queens',
    5: 'Staten Island',
}


def get_borough_number(name):
    """Try to find the borough number for the given name."""
    name = name.lower()
    for k, v in borough_number.items():
        if name == v.lower():
            return k
    return None
