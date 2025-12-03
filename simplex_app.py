import streamlit as st
import numpy as np
import pandas as pd

# -----------------------------------------------------------
# Simplex Functions
# -----------------------------------------------------------

def print_tableau_str(tableau, iteration, var_names):
    """Returns tableau text instead of printing."""
    output = f"\n--- Iteration {iteration} ---\n"
    rows, cols = tableau.shape

    # Header row
    output += " ".join([f"{name:>8}" for name in var_names]) + f"{' RHS':>8}\n"
    output += "-" * (10 * len(var_names)) + "\n"

    # Rows
    for i in range(rows):
        for j in range(cols):
            output += f"{tableau[i,j]:8.2f} "
        output += "\n"
    output += "-" * 50 + "\n"
    return output


def simplex(c, A, b):
    """
    Simplex Method (Maximization)
    A x <= b , x >= 0
    """
    m, n = A.shape
    tableau = np.zeros((m + 1, n + m + 1))

    slack_names = [f"s{i+1}" for i in range(m)]
    var_names = [f"x{i+1}" for i in range(n)] + slack_names

    tableau[:m, :n] = A
    tableau[:m, n:n + m] = np.eye(m)
    tableau[:m, -1] = b
    tableau[-1, :n] = -c

    iteration = 0
    steps = print_tableau_str(tableau, iteration, var_names + ["RHS"])

    # SIMPLEX LOOP
    while True:
        col = np.argmin(tableau[-1, :-1])

        if tableau[-1, col] >= 0:
            break  # OPTIMAL

        ratios = []
        for i in range(m):
            if tableau[i, col] > 0:
                ratios.append(tableau[i, -1] / tableau[i, col])
            else:
                ratios.append(np.inf)

        row = np.argmin(ratios)
        if ratios[row] == np.inf:
            raise Exception("Unbounded solution detected.")

        pivot = tableau[row, col]
        tableau[row, :] /= pivot

        for i in range(m + 1):
            if i != row:
                tableau[i, :] -= tableau[i, col] * tableau[row, :]

        iteration += 1
        steps += print_tableau_str(tableau, iteration, var_names + ["RHS"])

    # EXTRACT OPTIMAL SOLUTION
    x_opt = np.zeros(n + m)
    basis_variables = []

    for j in range(n + m):
        col = tableau[:m, j]
        if np.count_nonzero(col) == 1 and np.sum(col) == 1:
            row = np.where(col == 1)[0][0]
            x_opt[j] = tableau[row, -1]
            basis_variables.append((var_names[j], tableau[row, -1]))

    z_opt = tableau[-1, -1]

    return x_opt[:n], x_opt, z_opt, basis_variables, steps, var_names


# -----------------------------------------------------------
# STREAMLIT UI
# -----------------------------------------------------------

st.title("📌 Simplex Method Solver (Maximization)")
st.write("Enter any number of variables and constraints.")

num_vars = st.number_input("Number of Decision Variables", min_value=1, value=2)
num_cons = st.number_input("Number of Constraints", min_value=1, value=3)

st.write("### Objective Function")
c_input = st.text_input("Coefficients c (comma-separated)", "3, 5")
c = np.array([float(x.strip()) for x in c_input.split(",")])

st.write("### Constraint Matrix A (each row comma-separated)")
default_A = "\n".join([",".join(["1"] * num_vars) for _ in range(num_cons)])
A_input = st.text_area("Enter A matrix:", default_A)

A = np.array([[float(x.strip()) for x in row.split(",")] 
              for row in A_input.split("\n") if row.strip() != ""])

b_input = st.text_input("Enter b values (comma-separated)", ",".join(["10"] * num_cons))
b = np.array([float(x.strip()) for x in b_input.split(",")])

# -----------------------------------------------------------
# Solve Button
# -----------------------------------------------------------
if st.button("Solve Simplex"):
    try:
        x_basic, x_full, z_opt, basis, steps, var_names = simplex(c, A, b)

        st.success("Optimal Solution Found!")

        # ✔ Show variable names & values
        st.write("### 🔹 Optimal Values of Decision Variables (x1, x2, ...):")
        df_x = pd.DataFrame({
            "Variable": [f"x{i+1}" for i in range(num_vars)],
            "Value": x_basic
        })
        st.table(df_x)

        # ✔ Show slack variable values
        st.write("### 🔹 Slack Variables (s1, s2, ...):")
        df_slack = pd.DataFrame({
            "Variable": [f"s{i+1}" for i in range(num_cons)],
            "Value": x_full[num_vars:]
        })
        st.table(df_slack)

        # ✔ Show Z
        st.write("### 🔹 Optimal Objective Value (Z):")
        st.success(f"Z = {z_opt:.4f}")

        # ✔ Basic variables
        st.write("### 🔹 Final Basic Variables:")
        st.write(pd.DataFrame(basis, columns=["Variable", "Value"]))

        # ✔ Show all iterations
        st.write("### 🔹 Simplex Tableau (All Iterations):")
        st.text(steps)

    except Exception as e:
        st.error(str(e))
