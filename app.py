import random
import time

import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import statistics

import algorithms as alg

st.title("Sorting Algorithm Visualizer")

def render_metrics(m):
    if not m:
        return
    ms = m.get("seconds", 0.0) * 1000.0
    comps = m.get("comparisons", 0)
    moves = m.get("moves", 0)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Time (ms)", f"{ms:.2f}")
    with c2:
        st.metric("Comparisons", f"{comps:,}")
    with c3:
        st.metric("Moves", f"{moves:,}")

st.subheader("Input Configuration")
length = st.slider("List length", 5, 20, 8)
data = random.sample(range(1, 30), length)
st.write(f"Input array: {data}")

benchmark_mode = st.checkbox("Benchmark mode", value = False)
runs = st.slider("Benchmark runs", min_value=5,max_value=100,value=30,step=5) if benchmark_mode else None


if st.button("Run Comparison"):
    if benchmark_mode:
        algo_list = [
            ("Insertion Sort", lambda arr:alg.insertion_sort(arr)),
            ("Merge Sort", lambda arr:alg.merge_sort(arr)),
            ("Quick Sort", lambda arr:alg.quick_sort(arr)),
            ("Counting Sort", lambda arr:alg.counting_sort(arr)),
            ("Radix Sort (LSD)", lambda arr: alg.radix_sort_lsd(arr, base=10)),
            ("Heap Sort", lambda arr:alg.heap_sort(arr)),
            ("Shell Sort", lambda arr:alg.shell_sort(arr)),
            ("Bucket Sort", lambda arr:alg.bucket_sort(arr)),
        ]
        rows = []
        for name, fn in algo_list:
            times_ms = []
            comps = []
            moves = []

            for _ in range(runs):
                arr_copy = data.copy()
                steps, m = fn(arr_copy)
                times_ms.append(m["seconds"] * 1000)
                comps.append(m["comparisons"])
                moves.append(m["moves"])
            
            avg_ms = statistics.mean(times_ms)
            std_ms = statistics.pstdev(times_ms) if len(times_ms) > 1 else 0.0
            avg_comps = statistics.mean(comps)
            avg_moves = statistics.mean(moves)

            sorted_ok = (steps[-1]["array"] == sorted(data)) if steps else False

            rows.append({
                "Algorithm": name,
                "Avg_ms": avg_ms,
                "Std_ms": std_ms,
                "Avg_Comparisons": avg_comps,
                "Avg_Moves": avg_moves,
                "Sorted OK (last run)": sorted_ok,
                "Runs": runs,
            })

        df_bench = pd.DataFrame(rows).sort_values("Avg_ms", ascending=True)

        st.subheader(f"Benchmark (runs = {runs})")
        st.dataframe(
            df_bench.style.format({
                "Avg_ms": "{:.3f}",
                "Std_ms": "{:.3f}",
                "Avg_Comparisons": "{:.1f}",
                "Avg_Moves": "{:.1f}",
            }),
            use_container_width=True,
        )
        csv_bench = df_bench.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Benchmark CSV",
            data=csv_bench,
            file_name=f"benchmark_runs_{runs}.csv",
            mime="text/csv",
        )

        st.stop()

    data_insertion = data.copy()
    data_merge = data.copy()
    data_quick = data.copy()
    data_counting = data.copy()
    data_radix = data.copy()
    data_heap = data.copy()
    data_shell = data.copy()
    data_bucket = data.copy()

    steps_insertion, metrics_insertion = alg.insertion_sort(data_insertion)
    steps_merge, metrics_merge = alg.merge_sort(data_merge)
    steps_quick, metrics_quick = alg.quick_sort(data_quick)
    steps_counting, metrics_counting = alg.counting_sort(data_counting)
    steps_radix, metrics_radix = alg.radix_sort_lsd(data_radix, base=10)
    steps_heap, metrics_heap = alg.heap_sort(data_heap)
    steps_shell, metrics_shell = alg.shell_sort(data_shell)
    steps_bucket, metrics_bucket = alg.bucket_sort(data_bucket)


    def create_animation(steps, title, color_fn):
        if not steps:
            return go.Figure(
                layout=go.Layout(
                    width=900,
                    height=420,
                    title=title,
                    xaxis=dict(visible=False),
                    yaxis=dict(visible=False),
                    annotations=[dict(text="No steps to display", showarrow=False)],
                )
            )
        frames = []
        for i, step in enumerate(steps):
            array = step["array"]
            active_index = step.get("active_index", -1)
            sorted_boundary = step.get("sorted_boundary", -1)

            colors = color_fn(len(array), active_index, sorted_boundary)

            frames.append(
                go.Frame(
                    data=[
                        go.Scatter(
                            x=list(range(len(array))),
                            y=array,
                            mode="markers+text",
                            marker=dict(size=28, color=colors),
                            text=array,
                            textposition="middle center",
                        )
                    ],
                    name=f"Step {i+1}",
                )
            )

        initial = steps[0]
        initial_colors = color_fn(
            len(initial["array"]),
            initial.get("active_index", -1),
            initial.get("sorted_boundary", -1),
        )

        fig = go.Figure(
            data=[
                go.Scatter(
                    x=list(range(len(initial["array"]))),
                    y=initial["array"],
                    mode="markers+text",
                    marker=dict(size=28, color=initial_colors),
                    text=initial["array"],
                    textposition="middle center",
                )
            ],
            layout=go.Layout(
                width=900,
                height=420,
                title=title,
                xaxis=dict(range=[-0.5, len(initial["array"]) - 0.5]),
                yaxis=dict(range=[0, max(max(s["array"]) for s in steps) + 5]),
                updatemenus=[
                    dict(
                        type="buttons",
                        buttons=[dict(label="Play", method="animate", args=[None])],
                        showactive=False,
                    )
                ],
                sliders=[
                    {
                        "steps": [
                            {
                                "args": [
                                    [f"Step {i+1}"],
                                    {"frame": {"duration": 500, "redraw": True}},
                                ],
                                "label": f"{i+1}",
                                "method": "animate",
                            }
                            for i in range(len(frames))
                        ],
                        "transition": {"duration": 0},
                        "x": 0,
                        "y": -0.1,
                        "currentvalue": {"prefix": "Step: "},
                    }
                ],
            ),
            frames=frames,
        )
        return fig

    def insertion_colors(length, active_index, sorted_boundary):
        return [
            (
                "red"
                if j == active_index
                else "green" if j <= sorted_boundary else "gray"
            )
            for j in range(length)
        ]

    def merge_colors(length, active_index, sorted_boundary):
        return [
            (
                "purple"
                if j == active_index
                else "blue" if j <= sorted_boundary else "gray"
            )
            for j in range(length)
        ]

    def quick_colors(length, active_index, sorted_boundary):
        return [
            (
                "orange"
                if j == active_index
                else "green" if j == sorted_boundary else "gray"
            )
            for j in range(length)
        ]

    def counting_colors(length, active_index, sorted_boundary):
        return [
            (
                "purple"
                if j == active_index
                else "green" if j == sorted_boundary else "gray"
            )
            for j in range(length)
        ]

    def radix_colors(length, active_index, sorted_boundary):
        return [
            (
                "purple"
                if j == active_index
                else "green" if j <= sorted_boundary else "gray"
            )
            for j in range(length)
        ]
    
    def heap_colors(length, active_index, sorted_boundary):
        return [
            (
                "orange"
                if j == active_index
                else "green" if (sorted_boundary != -1 and j >= sorted_boundary)
                else "gray"
            )
            for j in range(length)
        ]
    def shell_colors(length, active_index, sorted_boundary):
        return [
            (
                "orange"
                if j == active_index
                else "gray"
            )
            for j in range(length)
        ]
    def bucket_colors(length, active_index, sorted_boundary):
        return [
            (
                "purple"
                if j == active_index
                else "green" if j <= sorted_boundary
                else "gray"
            )
            for j in range(length)
        ]


    tab_ins, tab_mer, tab_quick, tab_count, tab_radix, tab_heap, tab_shell, tab_bucket = st.tabs(
        ["Insertion","Merge","Quick","Counting","Radix (LSD)","Heap", "Shell", "Bucket"]
    )

    with tab_ins:
        st.plotly_chart(
            create_animation(steps_insertion, "Insertion Sort", insertion_colors),
            use_container_width=True,
        )
    with tab_mer:
        st.plotly_chart(
            create_animation(steps_merge, "Merge Sort", merge_colors),
            use_container_width=True,
        )
    with tab_quick:
        st.plotly_chart(
            create_animation(steps_quick, "Quick Sort", quick_colors),
            use_container_width=True,
        )
    with tab_count:
        st.plotly_chart(
            create_animation(steps_counting, "Counting Sort", counting_colors),
            use_container_width=True,
        )
    with tab_radix:
        st.plotly_chart(
            create_animation(steps_radix, "Radix Sort (LSD)", radix_colors),
            use_container_width=True,
        )
    with tab_heap:
        st.plotly_chart(
            create_animation(steps_heap, "Heap Sort", heap_colors),
            use_container_width=True,
        )
    with tab_shell:
        st.plotly_chart(
            create_animation(steps_shell, "Shell Sort", shell_colors),
            use_container_width=True,
        )
    with tab_bucket:
        st.plotly_chart(
            create_animation(steps_bucket, "Bucket Sort", bucket_colors),
            use_container_width=True,
        )

    df = pd.DataFrame(
        [
            {
                "Algorithm": "Insertion Sort",
                "Time_ms": metrics_insertion["seconds"] * 1000,
                "Comparisons": metrics_insertion["comparisons"],
                "Moves": metrics_insertion["moves"],
                "Frames": len(steps_insertion),
                "Sorted OK": steps_insertion[-1]["array"] == sorted(data)
            },
            {
                "Algorithm": "Merge Sort",
                "Time_ms": metrics_merge["seconds"] * 1000,
                "Comparisons": metrics_merge["comparisons"],
                "Moves": metrics_merge["moves"],
                "Frames": len(steps_merge),
                "Sorted OK": steps_merge[-1]["array"] == sorted(data)
            },
            {
                "Algorithm": "Quick Sort",
                "Time_ms": metrics_quick["seconds"] * 1000,
                "Comparisons": metrics_quick["comparisons"],
                "Moves": metrics_quick["moves"],
                "Frames": len(steps_quick),
                "Sorted OK": steps_quick[-1]["array"] == sorted(data)
            },
            {
                "Algorithm": "Counting Sort",
                "Time_ms": metrics_counting["seconds"] * 1000,
                "Comparisons": metrics_counting["comparisons"],
                "Moves": metrics_counting["moves"],
                "Frames": len(steps_counting),
                "Sorted OK": steps_counting[-1]["array"] == sorted(data)
            },
            {
                "Algorithm": "Radix Sort(LSD)",
                "Time_ms": metrics_radix["seconds"] * 1000,
                "Comparisons": metrics_radix["comparisons"],
                "Moves": metrics_radix["moves"],
                "Frames": len(steps_radix),
                "Sorted OK": steps_radix[-1]["array"] == sorted(data)
            },
            {
                "Algorithm": "Heap Sort",
                "Time_ms": metrics_heap["seconds"] * 1000,
                "Comparisons": metrics_heap["comparisons"],
                "Moves": metrics_heap["moves"],
                "Frames": len(steps_heap),
                "Sorted OK": steps_heap[-1]["array"] == sorted(data)
            },
            {
                "Algorithm": "Shell Sort",
                "Time_ms": metrics_shell["seconds"] * 1000,
                "Comparisons": metrics_shell["comparisons"],
                "Moves": metrics_shell["moves"],
                "Frames": len(steps_shell),
                "Sorted OK": steps_shell[-1]["array"] == sorted(data)
            },
            {
                "Algorithm": "Bucket Sort",
                "Time_ms": metrics_bucket["seconds"] * 1000,
                "Comparisons": metrics_bucket["comparisons"],
                "Moves": metrics_bucket["moves"],
                "Frames": len(steps_bucket),
                "Sorted OK": steps_bucket[-1]["array"] == sorted(data)
            }
        ]
    )
    st.subheader("Summary Table")
    st.dataframe(df.style.format({"Time_ms": "{:.2f}"}), use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download CSV", data=csv, file_name="sorting_summary.csv", mime="text/csv"
    )
