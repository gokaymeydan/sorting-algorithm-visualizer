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
            if a[j] > key:
                a[j + 1] = a[j]
                moves += 1
                steps.append(
                    {"array": a.copy(), "active_index": j + 1, "sorted_boundary": i}
                )
                j -= 1
            else:
                break
        a[j + 1] = key
        moves += 1
        steps.append({"array": a.copy(), "active_index": j + 1, "sorted_boundary": i})
    end = time.perf_counter()
    metrics = {"comparisons": comparisons, "moves": moves, "seconds": end - start}
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
        left_part = a[left : mid + 1]
        right_part = a[mid + 1 : right + 1]
        i = j = 0
        k = left

        # Merge while both parts have elements
        while i < len(left_part) and j < len(right_part):
            comparisons += 1  # one comparison each loop
            if left_part[i] <= right_part[j]:
                a[k] = left_part[i]
                moves += 1
                steps.append(
                    {"array": a.copy(), "active_index": k, "sorted_boundary": right}
                )
                i += 1
            else:
                a[k] = right_part[j]
                moves += 1
                steps.append(
                    {"array": a.copy(), "active_index": k, "sorted_boundary": right}
                )
                j += 1
            k += 1

        # Copy remaining elements of left_part
        while i < len(left_part):
            a[k] = left_part[i]
            moves += 1
            steps.append(
                {"array": a.copy(), "active_index": k, "sorted_boundary": right}
            )
            i += 1
            k += 1

        # Copy remaining elements of right_part
        while j < len(right_part):
            a[k] = right_part[j]
            moves += 1
            steps.append(
                {"array": a.copy(), "active_index": k, "sorted_boundary": right}
            )
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
    metrics = {"comparisons": comparisons, "moves": moves, "seconds": end - start}
    return steps, metrics


def quick_sort_with_metrics(arr):
    a = arr.copy()
    steps = []
    comparisons = 0
    moves = 0

    def swap(i, j, *, active_i=None, sorted_b=None):
        nonlocal moves
        if i == j:
            return
        (
            a[i],
            a[j],
        ) = (
            a[j],
            a[i],
        )
        moves += 2
        steps.append(
            {
                "array": a.copy(),
                "active_index": i if active_i is None else active_i,
                "sorted_boundary": -1 if sorted_b is None else sorted_b,
            }
        )

    def partition(low, high):
        nonlocal comparisons, moves
        pivot = a[high]
        i = low - 1
        # compare high-1 and pivot
        for j in range(low, high):
            comparisons += 1
            if a[j] <= pivot:
                i += 1
                swap(i, j, active_i=j)
        # put pivot back to place
        swap(i + 1, high, active_i=i + 1, sorted_b=i + 1)
        return i + 1

    def qs(low, high):
        if low < high:
            p = partition(low, high)
            qs(low, p - 1)
            qs(p + 1, high)

    start = time.perf_counter()
    if a:
        qs(0, len(a) - 1)
    seconds = time.perf_counter() - start

    metrics = {"comparisons": comparisons, "moves": moves, "seconds": seconds}
    return steps, metrics


def counting_sort_with_metrics(arr, k=None):
    a = arr.copy()
    steps = []
    comparisons = 0
    moves = 0

    if not a:
        return steps, {"comparisons": 0, "moves": 0, "seconds": 0.0}

    if k is None:
        k = max(a) + 1

    start = time.perf_counter()

    # count
    count = [0] * k
    for v in a:
        count[v] += 1
    # prefix sum
    for i in range(1, k):
        count[i] += count[i - 1]

    out = [0] * len(a)
    for v in reversed(a):
        count[v] -= 1
        out[count[v]] = v

    for i, v in enumerate(out):
        a[i] = v
        moves += 1
        steps.append({"array": a.copy(), "active_index": i, "sorted_boundary": i})

    seconds = time.perf_counter() - start
    metrics = {"comparisons": comparisons, "moves": moves, "seconds": seconds}
    return steps, metrics


def radix_sort_lsd_with_metrics(arr, base=10):
    a = arr.copy()
    steps = []
    comparisons = 0
    moves = 0

    if not a:
        return steps, {"comparisons": 0, "moves": 0, "seconds": 0.0}
    if base < 2:
        raise ValueError("radix base must be >= 2")

    start = time.perf_counter()

    def digit(x, exp):
        return (x // exp) % base

    exp = 1
    maxv = max(a)

    # for each digit place
    while maxv // exp > 0:
        # stable counting sort by current digit
        count = [0] * base
        for v in a:
            d = digit(v, exp)
            count[d] += 1

        # prefix sums -> positions
        for i in range(1, base):
            count[i] += count[i - 1]
        # build output stably(scan from right)
        out = [0] * len(a)
        
        for v in reversed(a):
            d = digit(v, exp)
            idx = count[d] - 1
            out[idx] = v
            count[d] = idx

        for i, v in enumerate(out):
            a[i] = v
            moves += 1
            steps.append(
                {"array": a.copy(), "active_index": i, "sorted_boundary": i}
            )
        exp *= base

    seconds = time.perf_counter() - start
    metrics = {"comparisons": comparisons, "moves": moves, "seconds": seconds}
    return steps, metrics
