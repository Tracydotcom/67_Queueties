def insertion_sort(arr):
    for i in range(1, len(arr)): 
        j = i
        while arr[j-1] > arr[j] and j>0: 
            arr[j-1], arr[j] = arr[j], arr[j-1] 
            j -= 1 
            if j == 0: 
                break

if __name__ == "__main__":
    user = input("Enter numbers separated by spaces: ")
    arr = list(map(int, user.split()))
    insertion_sort(arr)
    print("Sorted array is:", arr)
    
