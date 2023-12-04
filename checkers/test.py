def filter_routes(test):
    # Convert the list of strings to a set of frozensets for comparison
    route_sets = {key: frozenset(value) for key, value in test.items()}

    # Find the unique routes (not a subset of any other route)
    unique_routes = {key: list(value) for key, value in route_sets.items()
                     if not any(value < other_value for other_key, other_value in route_sets.items() if other_key != key)}

    return unique_routes


test = {
    (2, 1): ["Color: Black, Row: 1, Col: 2"],
    (4, 3): ["Color: Black, Row: 3, Col: 2", "Color: Black, Row: 1, Col: 2"],
    (6, 1): ["Color: Black, Row: 5, Col: 2", "Color: Black, Row: 3, Col: 2", "Color: Black, Row: 1, Col: 2"],
    (6, 5): ["Color: Black, Row: 5, Col: 4", "Color: Black, Row: 3, Col: 2", "Color: Black, Row: 1, Col: 2"],
    (2, 5): ["Color: Black, Row: 1, Col: 4"],
    (4, 7): ["Color: Black, Row: 3, Col: 6", "Color: Black, Row: 1, Col: 4"]
}

filtered_test = filter_routes(test)

for key, value in filtered_test.items():
    print(f"{key}: {value}")
