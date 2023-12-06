# Define the data
data = [
    {'Piece': 'piece1', 'moves': [{'position': (
        4, 3), 'captures': ['piece3', 'piece4'], 'partialRoute': [(2, 1), (4, 3)]}]},
    {'Piece': 'Piece2', 'moves': [
        {'position': (3, 3), 'captures': ['piece3'], 'partialRoute': [(1, 6), (3, 3)]}]}
]

# Define the move to be removed
move_to_remove = (2, 1)

# Function to process the data based on the move


def process_moves(data, move):
    new_data = []
    for item in data:
        new_moves = []
        for move_entry in item['moves']:
            if move in move_entry['partialRoute']:
                # Remove the move from partialRoute
                new_partial_route = [
                    m for m in move_entry['partialRoute'] if m != move]
                move_entry['partialRoute'] = new_partial_route
                new_moves.append(move_entry)
        if new_moves:
            # Only add items that contain the move in their partialRoute
            new_data.append({'Piece': item['Piece'], 'moves': new_moves})
    return new_data


# Process the data with the given move
output = process_moves(data, move_to_remove)
print(output)
