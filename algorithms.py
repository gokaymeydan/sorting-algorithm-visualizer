# algorithms.py with metrics
import time
import math


def insertion_sort(arr):
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


def merge_sort(arr):
    a = arr.copy()
    steps = []
    comparisons = 0
    moves = 0
    start = time.perf_counter()

    def merge(left, mid, right):
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

    def sort(left, right):
        if left >= right:
            return
        mid = (left + right) // 2
        sort(left, mid)
        sort(mid + 1, right)
        merge(left, mid, right)

    if len(a) > 0:
        sort(0, len(a) - 1)

    end = time.perf_counter()
    metrics = {"comparisons": comparisons, "moves": moves, "seconds": end - start}
    return steps, metrics


def quick_sort(arr):
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


def counting_sort(arr, k=None):
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


def radix_sort_lsd(arr, base=10):
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

        # count
        for v in a:
            d = digit(v, exp)
            count[d] += 1

        # prefix sums
        for i in range(1, base):
            count[i] += count[i - 1]

        # build output(scan from right)
        out = [0] * len(a)
        for i in range(len(a) - 1, -1, -1):
            v = a[i]
            d = digit(v, exp)
            count[d] -= 1
            out[count[d]] = v

        for i, v in enumerate(out):
            a[i] = v
            moves += 1
            steps.append({"array": a.copy(), "active_index": i, "sorted_boundary": i})
        exp *= base

    seconds = time.perf_counter() - start
    metrics = {"comparisons": comparisons, "moves": moves, "seconds": seconds}
    return steps, metrics

# --- Heap Sort (max-heap, in-place) with metrics & step recording ---
# steps: her adımda {"array": a.copy(), "active_index": i, "sorted_boundary": b}
# - active_index: o karede yeni yazılan / swap’e giren indeks
# - sorted_boundary: heapsort’ta sıralı kuyruk (suffix) başlangıcı; j >= boundary -> "sorted"
# metrics:
# - comparisons: her a[l] > a[m] veya a[r] > a[m] kontrolü 1 karşılaştırma
# - moves: diziye her yazma 1; swap 2 move
def heap_sort(arr):
    a = arr.copy()
    steps = []
    comparisons = 0
    moves = 0

    heap_sorted = -1

    def snapshot(active_i, boundary):
        steps.append({"array": a.copy(), "active_index": active_i, "sorted_boundary": boundary})

    def swap(i, j):
        nonlocal moves
        if i == j:
            return
        a[i], a[j] = a[j], a[i]
        moves += 2
        snapshot(i, heap_sorted)
    
    def heapify(n, i):
        nonlocal comparisons
        while True:
            largest = i
            l = 2*i+1
            r = 2*i+2

            if l < n:
                comparisons += 1
                if a[l] > a[largest]:
                    largest = l
            if r < n:
                comparisons += 1
                if a[r] > a[largest]:
                    largest = r
            if largest == i:
                break

            swap(i, largest)
            i = largest

    start = time.perf_counter()

    n = len(a)
    if n <= 1:
        metrics = {"comparisons": 0, "moves": 0, "seconds": 0.0}
        return steps, metrics
    
    # build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(n,i)
    # extract max
    for end in range(n-1, 0, -1):
        swap(0, end)
        heap_sorted = end
        heapify(end, 0)
    
    seconds = time.perf_counter() - start
    metrics = {"comparisons": comparisons, "moves": moves, "seconds": seconds}
    return steps, metrics

def shell_sort(arr):
    a = arr.copy()
    steps = []
    comparisons = 0
    moves = 0

    def snap(active_i, boundary =-1):
        steps.append({"array": a.copy(), "active_index": active_i, "sorted_boundary":boundary})
    
    start = time.perf_counter()

    n = len(a)
    if n <= 1:
        return steps, {"comparisons":0, "moves":0, "seconds": 0.0}
    
    gap = n // 2
    while gap > 0:
        for i in range(gap,n):
            key = a[i]
            j = i - gap

            while j >= 0:
                comparisons += 1
                if a[j] > key:
                    a[j + gap] = a[j]
                    moves += 1
                    snap(j + gap)
                    j -= gap
                else:
                    break
            a[j + gap] = key
            moves += 1
            snap(j + gap)
        
        gap //= 2
    
    seconds = time.perf_counter() - start
    metrics = {"comparisons": comparisons, "moves": moves, "seconds": seconds}
    return steps, metrics

def bucket_sort(arr, num_buckets = None):
    a = arr.copy()
    steps = []
    comparisons = 0
    moves = 0

    if not a:
        return steps, {"comparisons": 0, "moves": 0, "seconds": 0.0}

    n = len(a)

    if num_buckets is None:
        num_buckets = max(1, int(math.sqrt(n)))

    start = time.perf_counter()

    maxv = max(a)

    # normlize values range between 0 and 1
    if maxv == 0:
        seconds = time.perf_counter() - start

        for i, v in enumerate(a):
            steps.append({"array": a.copy(), "active_index": i, "sorted_boundary":i})
        return steps, {"comparisons":0, "moves":0, "seconds": seconds}
    
    normalized = [x / (maxv + 1.0) for x in a]
    
    #create buckets
    buckets = [[] for _ in range(num_buckets)]

    #split values to buckets
    for v_norm, v_orig in zip(normalized, a):
        idx = int(v_norm * num_buckets)
        if idx >= num_buckets:
            idx = num_buckets - 1
        buckets[idx].append(v_orig)

    # sort buckets

    for b in buckets:
        for i in range(1,len(b)):
            key = b[i]
            j = i - 1
            while j >=0:
                comparisons +=1
                if b[j] > key:
                    b[j + 1] = b[j]
                    j -= 1
                else:
                    break
            b[j + 1] = key
    
    # save at main
    write_i = 0
    for b in buckets:
        for v in b:
            a[write_i] = v
            moves += 1
            steps.append({"array":a.copy(),"active_index":write_i,"sorted_boundary":write_i})
            write_i += 1
    
    seconds = time.perf_counter() - start
    metrics = {"comparisons": comparisons,"moves":moves,"seconds":seconds}
    return steps, metrics