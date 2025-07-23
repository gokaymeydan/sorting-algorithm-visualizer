import streamlit as st
import random
import time
from algorithms import insertion_sort
import matplotlib.pyplot as plt

st.title("Insertion Sort Visualizer")

option = st.radio("Choose input method:", ["Manual Input", "Random List"])

if option == "Manual Input":
    user_input = st.text_input("Enter numbers seperated by commas (like 5,3,1,4)")
    if user_input:
        data = list(map(int, user_input.split(',')))
else:
    length = st.slider("List length", 5,20,8)
    data = random.sample(range(1,30), length)

if 'data' in locals() and st.button("Visualize Insertion Sort"):
    steps = insertion_sort(data)

    st.write(f"Total steps: {len(steps)}")

    for i, step in enumerate(steps):
        fig, ax = plt.subplots()
        ax.bar(range(len(step)), step)
        ax.set_title(f"Step {i + 1}")
        st.pyplot(fig)
        time.sleep(0.3)