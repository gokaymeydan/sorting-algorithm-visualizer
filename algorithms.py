def insertion_sort(arr):
    steps = []  # keep all steps here
    a = arr.copy()

    for i in range(1, len(a)):
        key = a[i]
        j = i - 1

        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            steps.append(
                {"array": a.copy(), "active_index": j + 1, "sorted_boundary": i}
            )
            j -= 1
        a[j + 1] = key
        steps.append(
            {"array": a.copy(), "active_index": j + 1, "sorted_boundary": i}
        )  # save every moment
    return steps


def merge_sort(arr):
    steps = []
    a = arr.copy()
    merge_sort_recursive(a, 0, len(a) - 1, steps)
    return steps


def merge_sort_recursive(arr, left, right, steps):
    if left < right:
        mid = (left + right) // 2
        merge_sort_recursive(arr, left, mid, steps)
        merge_sort_recursive(arr, mid + 1, right, steps)
        merge(arr, left, mid, right, steps)


def merge(arr, left, mid, right, steps):
    left_part = arr[left : mid + 1]
    right_part = arr[mid + 1 : right + 1]

    i = j = 0
    k = left

    while i < len(left_part) and j < len(right_part):
        if left_part[i] <= right_part[j]:
            arr[k] = left_part[i]
            steps.append(
                {"array": arr.copy(), "active_index": k, "sorted_boundary": right}
            )
            i += 1
        else:
            arr[k] = right_part[j]
            steps.append(
                {"array": arr.copy(), "active_index": k, "sorted_boundary": right}
            )
            j += 1
        k += 1

    while i < len(left_part):
        arr[k] = left_part[i]
        steps.append({"array": arr.copy(), "active_index": k, "sorted_boundary": right})
        i += 1
        k += 1

    while j < len(right_part):
        arr[k] = right_part[j]
        steps.append({"array": arr.copy(), "active_index": k, "sorted_boundary": right})
        j += 1
        k += 1
