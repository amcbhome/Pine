import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

st.set_page_config(layout="wide")
st.title("Optimal Production with Pine = 4x + 6y and Sweep of Pine Availability")

# -----------------------
# Controls
# -----------------------
pine_avail = st.slider("Pine Availability (max 4x + 6y):", min_value=100, max_value=800, step=10, value=400)
sweep_min, sweep_max = st.slider("Sweep range for pine availability:", 100, 800, (100, 800), step=10)

# -----------------------
# Solve current LP
# Max  P = 40x + 30y  -> minimize -40x -30y
# Constraints:
#   4x + 6y <= pine_avail
#   4x +  y <= 200
#   x >=0, y >=0
# -----------------------
c = [-40, -30]
A = [
    [4, 6],   # Pine: 4x + 6y ≤ pine_avail
    [4, 1],   # Varnish: 4x + y ≤ 200
]
b = [pine_avail, 200]
bounds = [(0, None), (0, None)]

res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

col1, col2 = st.columns((1, 1))

with col1:
    st.header("Current optimum")
    if res.success:
        x_opt, y_opt = res.x
        max_profit = 40*x_opt + 30*y_opt
        st.success(f"Optimal production: x = {x_opt:.4f}, y = {y_opt:.4f}")
        st.info(f"Maximum profit: P = {max_profit:.2f}")
    else:
        st.error("No feasible solution for current pine availability.")
        x_opt = y_opt = max_profit = None

    # Plot feasible region + optimal point
    x_vals = np.linspace(0, max(150, (sweep_max//1)), 400)
    y_pine = (pine_avail - 4*x_vals) / 6         # from 4x + 6y = pine_avail -> y = (pine - 4x)/6
    y_varn = 200 - 4*x_vals                     # from 4x + y = 200 -> y = 200 - 4x
    y_upper = np.minimum(y_pine, y_varn)
    y_upper = np.maximum(y_upper, 0)

    fig1, ax1 = plt.subplots(figsize=(6,5))
    mask = y_upper > 0
    ax1.fill_between(x_vals[mask], 0, y_upper[mask], alpha=0.5, label='Feasible region')
    ax1.plot(x_vals, y_pine, label=f'4x + 6y = {pine_avail} (Pine)')
    ax1.plot(x_vals, y_varn, label='4x + y = 200 (Varnish)')

    if res.success:
        # isoprofit line at optimum
        y_profit = (max_profit - 40*x_vals) / 30
        valid = (y_profit >= 0) & (y_profit <= max(y_upper)*1.1)
        ax1.plot(x_vals[valid], y_profit[valid], linestyle='--', label=f'Isoprofit (P={max_profit:.2f})')
        ax1.plot(x_opt, y_opt, marker='o', markersize=8, label=f'Optimum ({x_opt:.2f}, {y_opt:.2f})')
        ax1.annotate(f"P={max_profit:.2f}", xy=(x_opt, y_opt), xytext=(x_opt+3, y_opt+3),
                     arrowprops=dict(arrowstyle="->", lw=0.8))
    ax1.set_xlim(0, max(100, x_vals.max()))
    ax1.set_ylim(0, max(100, y_upper.max()*1.2))
    ax1.set_xlabel('x (units of Product X)')
    ax1.set_ylabel('y (units of Product Y)')
    ax1.set_title('Feasible Region and Optimal Point')
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

with col2:
    st.header("Sweep: optimum vs Pine availability")
    pine_range = np.arange(sweep_min, sweep_max + 1, 10)
    x_opts = []
    y_opts = []
    profits = []
    feasible_flags = []

    for p in pine_range:
        b_sweep = [p, 200]
        r = linprog(c, A_ub=A, b_ub=b_sweep, bounds=bounds, method='highs')
        if r.success:
            x_s, y_s = r.x
            x_opts.append(x_s)
            y_opts.append(y_s)
            profits.append(40*x_s + 30*y_s)
            feasible_flags.append(True)
        else:
            x_opts.append(np.nan)
            y_opts.append(np.nan)
            profits.append(np.nan)
            feasible_flags.append(False)

    # Plot 1: x_opt vs pine
    fig2, ax2 = plt.subplots(figsize=(6,3))
    ax2.plot(pine_range, x_opts)
    ax2.set_xlabel('Pine availability')
    ax2.set_ylabel('Optimal x')
    ax2.set_title('Optimal x vs Pine availability')
    ax2.grid(True)
    st.pyplot(fig2)

    # Plot 2: y_opt vs pine
    fig3, ax3 = plt.subplots(figsize=(6,3))
    ax3.plot(pine_range, y_opts)
    ax3.set_xlabel('Pine availability')
    ax3.set_ylabel('Optimal y')
    ax3.set_title('Optimal y vs Pine availability')
    ax3.grid(True)
    st.pyplot(fig3)

    # Plot 3: profit vs pine
    fig4, ax4 = plt.subplots(figsize=(6,3))
    ax4.plot(pine_range, profits)
    ax4.set_xlabel('Pine availability')
    ax4.set_ylabel('Max profit')
    ax4.set_title('Maximum profit vs Pine availability')
    ax4.grid(True)
    st.pyplot(fig4)

st.markdown(
    """
    **Notes**
    - Objective: maximize P = 40x + 30y  
    - Constraints: 4x + 6y ≤ Pine_avail, 4x + y ≤ 200, x,y ≥ 0  
    - The sweep shows how the LP solution changes as pine availability varies.
    """
)
