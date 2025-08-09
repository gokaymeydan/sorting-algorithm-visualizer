# algorithms.py with metrics
import time

def insertion_sort_with_metrics(arr):
    a = arr.copy()
    steps = []
    comparisons = 0
    moves = 0
    start = time.perf_counter()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        # at least one comparison if entering the while loop
        while j >= 0:
            comparisons += 1
            if a[j] > key :
                a[j + 1] = a[j]
                moves += 1
                steps.append(
                    {"array": a.copy(), "active_index": j + 1,
                     "sorted_boundary": i}
                )
                j -= 1
            else:
                break
        a[j + 1] = key
        moves += 1
        steps.append(
            {"array": a.copy(), "active_index": j+1,
            "sorted_boundary": i}
        )
    end = time.perf_counter()
    metrics = {
        "comparisons": comparisons,
        "moves": moves,
        "seconds": end - start
    }
    return steps, metrics

def merge_sort_with_metrics(arr):
    a = arr.copy()
    steps = []
    comparisons = 0
    moves = 0
    start = time.perf_counter()

    def merge_with_metrics(left, mid, right):
        nonlocal comparisons, moves
        # Create copies of subarrays
        left_part = a[left: mid + 1]
        right_part = a[mid + 1: right + 1]
        i = j = 0
        k = left

        # Merge while both parts have elements
        while i < len(left_part) and j < len(right_part):
            comparisons += 1  # one comparison each loop
            if left_part[i] <= right_part[j]:
                a[k] = left_part[i]
                moves += 1
                steps.append({"array": a.copy(), "active_index": k, "sorted_boundary": right})
                i += 1
            else:
                a[k] = right_part[j]
                moves += 1
                steps.append({"array": a.copy(), "active_index": k, "sorted_boundary": right})
                j += 1
            k += 1

        # Copy remaining elements of left_part
        while i < len(left_part):
            a[k] = left_part[i]
            moves += 1
            steps.append({"array": a.copy(), "active_index": k, "sorted_boundary": right})
            i += 1
            k += 1

        # Copy remaining elements of right_part
        while j < len(right_part):
            a[k] = right_part[j]
            moves += 1
            steps.append({"array": a.copy(), "active_index": k, "sorted_boundary": right})
            j += 1
            k += 1
    
    def sort_with_metrics(left, right):
        if left >= right:
            return
        mid = (left + right) // 2
        sort_with_metrics(left, mid)
        sort_with_metrics(mid + 1, right)
        merge_with_metrics(left, mid, right)

    if len(a) > 0:
        sort_with_metrics(0, len(a) - 1)
    
    end = time.perf_counter()
    metrics = {
        "comparisons": comparisons,
        "moves": moves,
        "seconds": end - start
    }
    return steps, metrics