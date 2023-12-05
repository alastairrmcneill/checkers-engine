# Defining the data
data = [
    {'Piece': "piece1", 'moves': [
        {'position': (2, 1), 'captures': ["piece3"], 'partialRoute': [(2, 1)]},
        {'position': (4, 3), 'captures': [
            "piece3", "piece4"], 'partialRoute': [(2, 1), (4, 3)]}
    ]},
    {'Piece': "Piece2", 'moves': [
        {'position': (1, 6), 'captures': ["piece3"], 'partialRoute': [(1, 6)]},
        {'position': (3, 3), 'captures': [
            "piece3"], 'partialRoute': [(1, 6), (3, 3)]}
    ]}
]

# Function to check if a route is contained within another route


def is_route_contained(route, other_routes):
    for other_route in other_routes:
        if route != other_route and all(point in other_route for point in route):
            return True
    return False

# Function to filter the moves based on 'partialRoute'


def filter_moves(data):
    for piece_data in data:
        piece_data['moves'] = [move for move in piece_data['moves'] if not is_route_contained(
            move['partialRoute'], [other_move['partialRoute'] for other_move in piece_data['moves']])]
    return data


# Applying the function to the data
output = filter_moves(data)
for pieceMove in output:
    print(pieceMove)
