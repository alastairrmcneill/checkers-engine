# Original data
data = {
    (2, 5): ["Color: Black, Row: 1, Col: 6"],
    (4, 3): ["Color: Black, Row: 3, Col: 4", "Color: Black, Row: 1, Col: 6"],
    (6, 1): ["Color: Black, Row: 5, Col: 2", "Color: Black, Row: 3, Col: 4", "Color: Black, Row: 1, Col: 6"],
    (6, 5): ["Color: Black, Row: 5, Col: 4", "Color: Black, Row: 3, Col: 4", "Color: Black, Row: 1, Col: 6"],
}

# Function to check if a value is contained within another value


def is_value_contained(main_value, other_values):
    for value in other_values:
        if main_value != value and all(item in value for item in main_value):
            return True
    return False


# Filtering the data to only include key-value pairs where the value is not contained within another value
filtered_data = {key: value for key, value in data.items(
) if not is_value_contained(value, data.values())}

for data in filtered_data:
    print(f"{data}: {filtered_data[data]}")


"""
Can I save the move in a structure like 
Move1 = {final_square: (3,4),
        partial_squares: [(2,1)],
        captured_pieces: [Piece(), Piece()]}
        
Move2 = {final_square: (3,4),
        partial_squares: [(2,5)],
        captured_pieces: [Piece(), Piece()]}
        
moves = [
    Move1
    Move2
]

check if selected squre is in move[0].partial_squares or move[0].final_square o rmove[1].partial_squares or move[1].final_square

if its in a certain move set 

"""
