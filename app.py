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
show_metrics = st.checkbox("Show metrics (use *_with_metrics)", value=True)
length = st.slider("List length", 5, 20, 8)
data = random.sample(range(1, 30), length)
st.write(f"Input array: {data}")

if st.button("Compare Insertion Sort vs Merge Sort vs Quick Sort"):
    data_insertion = data.copy()
    data_merge = data.copy()
    data_quick = data.copy()
    data_counting = data.copy()

    if show_metrics:
        steps_insertion, metrics_insertion = alg.insertion_sort_with_metrics(data_insertion)
        steps_merge, metrics_merge = alg.merge_sort_with_metrics(data_merge)
        steps_quick, metrics_quick = alg.quick_sort_with_metrics(data_quick)
        steps_counting, metrics_counting = alg.counting_sort_with_metrics(data_counting)
    else:
        steps_insertion = getattr(
            alg, "insertion_sort", alg.insertion_sort_with_metrics
        )(data_insertion)
        if isinstance(steps_insertion, tuple):
            steps_insertion = steps_insertion[0]
        steps_merge = getattr(alg, "merge_sort", alg.merge_sort_with_metrics)(
            data_merge
        )
        if isinstance(steps_merge, tuple):
            steps_merge = steps_merge[0]
            steps_quick = getattr(alg, "quick_sort", alg.quick_sort_with_metrics)(
                data_quick
            )
        if isinstance(steps_quick, tuple):
            steps_quick = steps_quick[0]
        metrics_insertion = None
        metrics_merge = None
        metrics_quick = None
        metrics_counting = None

    st.subheader("Comparison Results")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Insertion Sort")
        if metrics_insertion is not None:
            render_metrics(metrics_insertion)

    with col2:
        st.markdown("### Merge Sort")
        if metrics_merge is not None:
            render_metrics(metrics_merge)

    with col3:
        st.markdown("### Quick Sort")
        if metrics_quick is not None:
            render_metrics(metrics_quick)

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
                            marker=dict(size=40, color=colors),
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
                    marker=dict(size=40, color=initial_colors),
                    text=initial["array"],
                    textposition="middle center",
                )
            ],
            layout=go.Layout(
                height=400,
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

    st.plotly_chart(
        create_animation(steps_insertion, "Insertion Sort", insertion_colors)
    )
    st.plotly_chart(create_animation(steps_merge, "Merge Sort", merge_colors))
    st.plotly_chart(create_animation(steps_quick, "Quick Sort", quick_colors))

    if show_metrics:
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
            ]
        )
        st.subheader("Summary Table")
        st.dataframe(df.style.format({"Time_ms": "{:.2f}"}), use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download CSV", data=csv, file_name="sorting_summary.csv", mime="text/csv"
        )
