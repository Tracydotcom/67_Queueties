def quicksort(array):
    if len(array) <= 1: # if the array has only one element or none, then it is already sorted
        return array
    
    pivot = array[len(array) // 2] # Pivot is the variable that holds the median of the array
    left = [x for x in array if x < pivot]
    middle = [x for x in array if x == pivot]
    right = [x for x in array if x > pivot]

    return (quicksort(left) + middle + quicksort(right))

