import random
import time

import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

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
base = st.selectbox("Radix base", [2, 4, 8, 10, 16], index=3)
st.write(f"Input array: {data}")

if st.button("Run Comparison"):
    data_insertion = data.copy()
    data_merge = data.copy()
    data_quick = data.copy()
    data_counting = data.copy()
    data_radix = data.copy()
    data_heap = data.copy()

    steps_insertion, metrics_insertion = alg.insertion_sort(data_insertion)
    steps_merge, metrics_merge = alg.merge_sort(data_merge)
    steps_quick, metrics_quick = alg.quick_sort(data_quick)
    steps_counting, metrics_counting = alg.counting_sort(data_counting)
    steps_radix, metrics_radix = alg.radix_sort_lsd(data_radix, base=base)
    steps_heap, metrics_heap = alg.heap_sort(data_heap)

    def create_animation(steps, title, color_fn):
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
                height=320,
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

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            create_animation(steps_insertion, "Insertion Sort", insertion_colors),
            use_container_width=True,
        )
    with c2:
        st.plotly_chart(
            create_animation(steps_merge, "Merge Sort", merge_colors),
            use_container_width=True,
        )
    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(
            create_animation(steps_quick, "Quick Sort", quick_colors),
            use_container_width=True,
        )
    with c4:
        st.plotly_chart(
            create_animation(steps_counting, "Counting Sort", counting_colors),
            use_container_width=True,
        )
    c5, c6 = st.columns(2)
    with c5:
        st.plotly_chart(
            create_animation(steps_radix, "Radix Sort (LSD)", radix_colors),
            use_container_width=True,
        )
    with c6:
        st.plotly_chart(
            create_animation(steps_heap, "Heap Sort", heap_colors),
            use_container_width=True,
        )

    df = pd.DataFrame(
        [
            {
                "Algorithm": "Insertion",
                "Time_ms": metrics_insertion["seconds"] * 1000,
                "Comparisons": metrics_insertion["comparisons"],
                "Moves": metrics_insertion["moves"],
                "Frames": len(steps_insertion),
            },
            {
                "Algorithm": "Merge",
                "Time_ms": metrics_merge["seconds"] * 1000,
                "Comparisons": metrics_merge["comparisons"],
                "Moves": metrics_merge["moves"],
                "Frames": len(steps_merge),
            },
            {
                "Algorithm": "Quick",
                "Time_ms": metrics_quick["seconds"] * 1000,
                "Comparisons": metrics_quick["comparisons"],
                "Moves": metrics_quick["moves"],
                "Frames": len(steps_quick),
            },
            {
                "Algorithm": "Counting",
                "Time_ms": metrics_counting["seconds"] * 1000,
                "Comparisons": metrics_counting["comparisons"],
                "Moves": metrics_counting["moves"],
                "Frames": len(steps_counting),
            },
            {
                "Algorithm": "Radix (LSD, base=" + str(base) + ")",
                "Time_ms": metrics_radix["seconds"] * 1000,
                "Comparisons": metrics_radix["comparisons"],
                "Moves": metrics_radix["moves"],
                "Frames": len(steps_radix),
            },
            {
                "Algorithm": "Heap Sort",
                "Time_ms": metrics_heap["seconds"] * 1000,
                "Comparisons": metrics_heap["comparisons"],
                "Moves": metrics_heap["moves"],
                "Frames": len(steps_heap),
            }
        ]
    )
    st.subheader("Summary Table")
    st.dataframe(df.style.format({"Time_ms": "{:.2f}"}), use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download CSV", data=csv, file_name="sorting_summary.csv", mime="text/csv"
    )
