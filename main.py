from algorithms import insertion_sort

my_list = [5, 2, 4, 6, 1, 3]
steps = insertion_sort(my_list)
prev = None

def print_step(step, prev_step=None):
    for i, num in enumerate(step):
        bar = '█' * num
        if prev_step and prev_step[i] != num:
            print(f"{num:>2} {bar} <- shifted")
        else:
            print(f"{num:>2} {bar}")
    print("-" * 20)

for i, step in enumerate(steps):
    print(f"Step {i + 1}: {step}")
    print_step(step,prev)
    prev = step