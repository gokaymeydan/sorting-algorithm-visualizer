# insertion sort


def insertion_sort(arr):
    steps = []  # keep all steps here

    for j in range(1, len(arr)):
        key = arr[j]
        i = j - 1

        while i >= 0 and arr[i] > key:
            arr[i + 1] = arr[i]
            i -= 1
            steps.append(arr.copy())

        arr[i + 1] = key
        steps.append(arr.copy())  # save every moment

    return steps
