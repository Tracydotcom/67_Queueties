# INSERTION SORT OF NUMERICAL SORTING

def insertion_sort(arr):
    for i in range(1, len(arr)): # iterating from second element, as it is considered unsorted. first is always sorted.
        j = i
        while arr[j-1] > arr[j] and j>0: #checks if left element is greater than current
            arr[j-1], arr[j] = arr[j], arr[j-1] #swaps if left is greater
            j -= 1 #go further to the left
            if j == 0: #breaks if it reaches the start of the array
                break

#INSERTION SORT FOR ALPHABETICAL SORTING

# def insertion_sort_alpha(arr):
#     for i in range(1, len(arr)): # iterating from second element, as it is considered unsorted. first is always sorted.
#         j = i
#         while arr[j-1].lower() > arr[j].lower() and j>0: #checks if left element is greater than current (case insensitive)
#             arr[j-1], arr[j] = arr[j], arr[j-1] #swaps if left is greater
#             j -= 1 #go further to the left
#             if j == 0: #breaks if it reaches the start of the array
#                 break


if __name__ == "__main__":
    user = input("Enter numbers separated by spaces: ")
    arr = list(map(int, user.split()))
    insertion_sort(arr)
    print("Sorted array is:", arr)
    
    # user_alpha = input("Enter words separated by spaces: ")
    # arr_alpha = user_alpha.split()
    # insertion_sort_alpha(arr_alpha)
    # print("Sorted words are:", arr_alpha)