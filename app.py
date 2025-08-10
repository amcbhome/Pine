import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("Draggable Point in Feasible Region")

# Constraints
pine_avail = 400  # fixed for this example
varnish_limit = 200

# Feasible region boundaries
x_vals = np.linspace(0, 100, 200)
y_pine = (pine_avail - 4*x_vals) / 6
y_varn = varnish_limit - 4*x_vals
y_upper = np.minimum(y_pine, y_varn)
y_upper = np.clip(y_upper, 0, np.max(y_upper))

# Create polygon points for feasible region
feasible_x = np.concatenate([x_vals, x_vals[::-1]])
feasible_y = np.concatenate([np.zeros_like(x_vals), y_upper[::-1]])

# Initial point (start at optimum from LP)
from scipy.optimize import linprog
c = [-40, -30]
A = [[4,6],[4,1]]
b = [pine_avail, varnish_limit]
bounds = [(0,None),(0,None)]
res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')
x_init, y_init = res.x if res.success else (10,10)

# Plotly figure
fig = go.Figure()

# Feasible region polygon
fig.add_trace(go.Scatter(
    x=feasible_x,
    y=feasible_y,
    fill="toself",
    fillcolor="rgba(0,200,200,0.2)",
    line=dict(color="royalblue"),
    name="Feasible Region",
    hoverinfo='skip'
))

# Constraint lines
fig.add_trace(go.Scatter(x=x_vals, y=y_pine, mode='lines', name='4x+6y ≤ Pine'))
fig.add_trace(go.Scatter(x=x_vals, y=y_varn, mode='lines', name='4x + y ≤ 200'))

# Draggable point
fig.add_trace(go.Scatter(
    x=[x_init],
    y=[y_init],
    mode='markers',
    marker=dict(size=15, color='red'),
    name='Decision Variable (x,y)',
    dragmode='xy',
    uid='drag_point'
))

fig.update_layout(
    dragmode='closest',
    xaxis=dict(range=[0, max(x_vals)], title='x (units Product X)'),
    yaxis=dict(range=[0, max(y_upper)*1.1], title='y (units Product Y)'),
    height=600,
    title="Drag the red point inside the feasible region"
)

dragged_point = st.plotly_chart(fig, use_container_width=True)

# Streamlit can't capture drag events directly, but we can use plotly_events (external) or a workaround:
st.markdown("""
**Instructions:**

- Drag the **red point** on the plot (in a separate browser window/tab that supports Plotly dragging)
- Currently, Streamlit cannot capture drag events live inside the app.
- To get fully interactive drag & update, you need a Dash app or a web app using Plotly Dash or another JS framework.
""")

# Alternatively: Provide input boxes to enter x,y manually to simulate dragging

x_input = st.number_input("Enter x:", value=float(x_init), min_value=0.0, max_value=float(max(x_vals)))
y_input = st.number_input("Enter y:", value=float(y_init), min_value=0.0, max_value=float(max(y_upper)*1.1))

# Check constraints
pine_val = 4*x_input + 6*y_input
varn_val = 4*x_input + y_input
profit = 40*x_input + 30*y_input

st.write(f"Profit = £{profit:.0f}")
st.write(f"Pine constraint (4x+6y ≤ {pine_avail}): {pine_val:.0f} {'✔️' if pine_val <= pine_avail else '❌'}")
st.write(f"Varnish constraint (4x+y ≤ {varnish_limit}): {varn_val:.0f} {'✔️' if varn_val <= varnish_limit else '❌'}")
