import random
import time

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st

from algorithms import insertion_sort, merge_sort

st.title("Insertion Sort vs Merge Sort Visualizer")

# --- Veri Girişi ---
st.subheader("Input Configuration")
length = st.slider("List length", 5, 20, 8)
data = random.sample(range(1, 30), length)
st.write(f"Input array: {data}")

if st.button("Compare Insertion Sort vs Merge Sort"):
    data_insertion = data.copy()
    data_merge = data.copy()

    steps_insertion = insertion_sort(data_insertion)

    steps_merge = merge_sort(data_merge)

    st.subheader("Comparison Results")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Insertion Sort")
        st.write(f"Total steps: {len(steps_insertion)}")

    with col2:
        st.markdown("### Merge Sort")
        st.write(f"Total steps: {len(steps_merge)}")

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
            "red" if j == active_index else "green" if j <= sorted_boundary else "gray"
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

    st.plotly_chart(
        create_animation(steps_insertion, "Insertion Sort", insertion_colors)
    )

    st.plotly_chart(create_animation(steps_merge, "Merge Sort", merge_colors))

    st.subheader("About the Algorithms")
    st.markdown("**Insertion Sort**")
    st.markdown(
        """
    - Simple comparison-based sorting algorithm  
    - Builds the sorted array one element at a time  
    - In-place and stable  
    - Best case: Θ(n) when the array is already sorted  
    - Worst case: Θ(n²) when the array is reverse sorted  
    """
    )

    st.markdown("**Merge Sort**")
    st.markdown(
        """
    - Divide-and-conquer algorithm  
    - Recursively splits the array and merges sorted halves  
    - Stable but not in-place  
    - Consistently performs in Θ(n log n) time in all cases  
    - Requires additional memory for merging  
    """
    )
