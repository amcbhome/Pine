import streamlit as st

def is_feasible(x, y):
    """Check feasibility of (x,y) given constraints."""
    if x < 0 or y < 0:
        return False
    if 4*x + 4*y > 400:
        return False
    if 3*x + 5*y > 600:
        return False
    if 4*x + y > 200:
        return False
    if 3*x + 2*y > 300:
        return False
    return True

st.title("LP Feasibility Checker")

x = st.number_input("Enter units of Product X (x):", min_value=0.0, step=1.0)
y = st.number_input("Enter units of Product Y (y):", min_value=0.0, step=1.0)

if st.button("Check Feasibility"):
    if is_feasible(x, y):
        st.success(f"The point (x={x}, y={y}) is feasible.")
    else:
        st.error(f"The point (x={x}, y={y}) is NOT feasible.")
