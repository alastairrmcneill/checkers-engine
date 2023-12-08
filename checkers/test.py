def find_last_unique_sum_index(list_of_lists):
    sums = [sum(lst) for lst in list_of_lists]
    unique_sum_index = -1

    for i, current_sum in enumerate(sums):
        if all(current_sum != previous_sum for previous_sum in sums[:i]):
            unique_sum_index = i

    return unique_sum_index


# Example usage
list_of_lists = [[1, 2, 3], [3, 2, 1], [
    4, 0, 2], [4, 0, 3], [4, 0, 3], [4, 1, 5], [4, 2, 4]]
index = find_last_unique_sum_index(list_of_lists)
# This will print the index of the last list with a unique sum
print(len(list_of_lists)-index)
