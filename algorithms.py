# insertion sort


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
