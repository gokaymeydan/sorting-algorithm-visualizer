import random
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import streamlit as st

from algorithms import insertion_sort

st.title("Insertion Sort Visualizer")

option = st.radio("Choose input method:", ["Manual Input", "Random List"])

if option == "Manual Input":
    user_input = st.text_input("Enter numbers seperated by commas (like 5,3,1,4)")
    if user_input:
        data = list(map(int, user_input.split(",")))
else:
    length = st.slider("List length", 5, 20, 8)
    data = random.sample(range(1, 30), length)

if "data" in locals() and st.button("Visualize Insertion Sort"):
    steps = insertion_sort(data)

    st.write(f"Total steps: {len(steps)}")

    frames = []
    for i, step in enumerate(steps):
        array = step["array"]
        active_index = step["active_index"]
        sorted_boundary = step["sorted_boundary"]

        colors = []
        for j in range(len(array)):
            if j == active_index:
                colors.append("red")
            elif j <= sorted_boundary:
                colors.append("green")
            else:
                colors.append("gray")
        
        frames.append(go.Frame(
            data=[go.Scatter(
                x=list(range(len(array))),
                y=array,
                mode="markers+text",
                marker=dict(size=40, color=colors),
                text=array,
                textposition="middle center"
            )],
            name=f"Step {i+1}"
        ))
    initial = steps[0]
    initial_colors = [
        "red" if j == initial["active_index"] else
        "green" if j <= initial["sorted_boundary"] else "gray"
        for j in range(len(initial["array"]))
    ]

    fig = go.Figure(
        data=[go.Scatter(
            x=list(range(len(initial["array"]))),
            y=initial["array"],
            mode="markers+text",
            marker=dict(size=40, color=initial_colors),
            text=initial["array"],
            textposition="middle center"
        )],
        layout=go.Layout(
            title="Insertion Sort Animation",
            xaxis=dict(range=[-0.5, len(initial["array"]) - 0.5]),
            yaxis=dict(range=[0, max(max(s['array']) for s in steps) + 5]),
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play", method="animate", args=[None])],
                showactive=False
            )],
            sliders=[{
                "steps": [{
                    "args": [[f"Step {i+1}"], {"frame": {"duration": 500, "redraw": True}}],
                    "label": f"{i+1}",
                    "method": "animate"
                } for i in range(len(frames))],
                "transition": {"duration": 0},
                "x": 0, "y": -0.1,
                "currentvalue": {"prefix": "Step: "}
            }]
        ),
        frames=frames
    )

    st.plotly_chart(fig)