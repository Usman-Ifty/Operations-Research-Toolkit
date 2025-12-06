# ============================================================
#  LP + INTEGER LP SOLVER (MAXIMIZATION) USING BIG-M SIMPLEX
#  Supports <=, >=, =  constraints
#  Includes Branch & Bound for integer programming
#  No external libraries required.
# ============================================================

EPS = 1e-9
MAX_ITER = 100
BIG_M = 10000.0   # Penalty for artificial variables (tuned for exam-scale problems)


# ------------------------------------------------------------
# Utility: pretty printing of tableau
# ------------------------------------------------------------
def print_tableau(tableau, var_names, iter_no):
    rows = len(tableau)
    cols = len(tableau[0])

    print(f"\n================ SIMPLEX ITERATION {iter_no} ================")

    header = ""
    for name in var_names:
        header += f"{name:>10}"
    header += f"{'RHS':>10}"
    print(header)
    print("-" * (12 * (len(var_names) + 1)))

    for i in range(rows):
        line = ""
        for j in range(cols):
            line += f"{tableau[i][j]:>10.4f}"
        print(line)

    print("-" * (12 * (len(var_names) + 1)))
    print("=============================================================")


# ------------------------------------------------------------
# Canonicalize constraints: make RHS >= 0
# constraint = {"a": [...], "sense": "<=/>=/=", "b": ...}
# ------------------------------------------------------------
def canonicalize_constraints(constraints):
    canon = []
    for cons in constraints:
        a = cons["a"][:]
        sense = cons["sense"]
        b = cons["b"]

        if b < 0:
            # Multiply entire row by -1; flip sense for <=, >=
            a = [-x for x in a]
            b = -b
            if sense == "<=":
                sense = ">="
            elif sense == ">=":
                sense = "<="
            # "=" stays "="

        canon.append({"a": a, "sense": sense, "b": b})
    return canon


# ------------------------------------------------------------
# BIG-M SIMPLEX SOLVER
#   Maximize Z = c^T x
#   constraints: list of {a, sense ('<=','>=','='), b}
#   Returns: (status, x_opt (only original vars), Z_opt, var_names)
#   status: "optimal", "infeasible", "unbounded", "iterations_exceeded"
# ------------------------------------------------------------
def big_m_simplex(c, constraints, verbose=False):
    # Canonicalize RHS >= 0
    cons = canonicalize_constraints(constraints)
    m = len(cons)
    n = len(c)

    # Count slack, surplus, artificial
    n_slack = sum(1 for con in cons if con["sense"] == "<=")
    n_surplus = sum(1 for con in cons if con["sense"] == ">=")
    n_art = sum(1 for con in cons if con["sense"] in (">=", "="))

    total_vars = n_slack + n_surplus + n_art + n
    # Column offsets
    slack_start = n
    surplus_start = slack_start + n_slack
    art_start = surplus_start + n_surplus
    art_end = art_start + n_art

    # Build variable names
    var_names = []
    for i in range(n):
        var_names.append(f"x{i+1}")
    for i in range(n_slack):
        var_names.append(f"s{i+1}")
    for i in range(n_surplus):
        var_names.append(f"u{i+1}")
    for i in range(n_art):
        var_names.append(f"a{i+1}")

    # Build initial tableau
    tableau = []
    basic_vars = [None] * m  # store basic variable column index for each row

    # indices for each type
    slack_idx = 0
    surplus_idx = 0
    art_idx = 0

    for i, con in enumerate(cons):
        row = [0.0] * (total_vars + 1)  # +1 for RHS
        a = con["a"]
        sense = con["sense"]
        b = con["b"]

        # original vars
        for j in range(n):
            row[j] = a[j]

        if sense == "<=":
            # add slack
            col = slack_start + slack_idx
            row[col] = 1.0
            basic_vars[i] = col
            slack_idx += 1

        elif sense == ">=":
            # surplus (-1) + artificial
            col_surplus = surplus_start + surplus_idx
            row[col_surplus] = -1.0
            surplus_idx += 1

            col_art = art_start + art_idx
            row[col_art] = 1.0
            basic_vars[i] = col_art
            art_idx += 1

        elif sense == "=":
            # artificial only
            col_art = art_start + art_idx
            row[col_art] = 1.0
            basic_vars[i] = col_art
            art_idx += 1

        row[-1] = b
        tableau.append(row)

    # OBJECTIVE ROW (Big-M):
    #   max Z = c^T x - M * sum(artificial)
    #   we store -c_j in objective row for original vars
    obj = [0.0] * (total_vars + 1)

    # original variables part: -c_j
    for j in range(n):
        obj[j] = -c[j]

    # artificial variables: coefficient is -M, so in table row we put +M
    for j in range(art_start, art_end):
        obj[j] = BIG_M

    # Now adjust for artificials being basic initially
    # For each artificial basic in row i, do: obj = obj - M * row_i
    for i in range(m):
        basic = basic_vars[i]
        if basic is not None and art_start <= basic < art_end:
            for j in range(total_vars + 1):
                obj[j] -= BIG_M * tableau[i][j]

    tableau.append(obj)

    # ---- Simplex iterations ----
    if verbose:
        print_tableau(tableau, var_names, 0)

    iter_no = 0
    while True:
        last = tableau[-1]
        # Choose entering variable: most negative coefficient
        entering = min(range(total_vars), key=lambda j: last[j])
        if last[entering] >= -EPS:
            # optimal reached
            break

        # Ratio test for leaving variable
        ratios = []
        for i in range(m):
            col_val = tableau[i][entering]
            if col_val > EPS:
                ratios.append(tableau[i][-1] / col_val)
            else:
                ratios.append(float("inf"))

        pivot_row = min(range(m), key=lambda i: ratios[i])
        if ratios[pivot_row] == float("inf"):
            return "unbounded", None, None, var_names

        # Pivot operation
        pivot = tableau[pivot_row][entering]
        tableau[pivot_row] = [x / pivot for x in tableau[pivot_row]]

        for i in range(m + 1):
            if i != pivot_row:
                factor = tableau[i][entering]
                tableau[i] = [
                    tableau[i][j] - factor * tableau[pivot_row][j]
                    for j in range(total_vars + 1)
                ]

        basic_vars[pivot_row] = entering

        iter_no += 1
        if iter_no > MAX_ITER:
            return "iterations_exceeded", None, None, var_names

        if verbose:
            print_tableau(tableau, var_names, iter_no)

    # ---- Extract solution ----
    solution = [0.0] * total_vars
    for j in range(total_vars):
        # Check if column j is basic
        col = [tableau[i][j] for i in range(m)]
        ones = sum(1 for v in col if abs(v - 1.0) < 1e-8)
        zeros = sum(1 for v in col if abs(v) < 1e-8)
        if ones == 1 and zeros == m - 1:
            row_idx = [i for i, v in enumerate(col) if abs(v - 1.0) < 1e-8][0]
            solution[j] = tableau[row_idx][-1]

    # Check artificial variables: if any artificial > 0 → infeasible
    infeasible = False
    for j in range(art_start, art_end):
        if solution[j] > 1e-6:
            infeasible = True
            break

    if infeasible:
        return "infeasible", None, None, var_names

    Z_opt = tableau[-1][-1]

    # Return only original x's
    x_opt = solution[:n]
    return "optimal", x_opt, Z_opt, var_names


# ------------------------------------------------------------
# Helpers: input
# ------------------------------------------------------------
def read_float_list(prompt, count=None):
    while True:
        try:
            vals = list(map(float, input(prompt).split()))
            if count is not None and len(vals) != count:
                print(f"❌ ERROR: expected {count} values.")
                continue
            return vals
        except:
            print("❌ INVALID input. Try again.")


def read_constraints(m, n):
    constraints = []
    print("\nENTER constraints in the form:")
    print("  A Row i: (a1 a2 ... an)")
    print("  then: b[i] and sense (LE/GE/EQ), e.g. 7 LE or 3 GE or 5 EQ\n")

    for i in range(m):
        a = read_float_list(f"A Row {i+1}: ", count=n)
        while True:
            parts = input(f"b[{i+1}] and sense (LE/GE/EQ): ").split()
            if len(parts) != 2:
                print("❌ Format must be: number LE/GE/EQ")
                continue
            try:
                b_val = float(parts[0])
                sense_raw = parts[1].upper()
                if sense_raw in ("LE", "<="):
                    sense = "<="
                elif sense_raw in ("GE", ">="):
                    sense = ">="
                elif sense_raw in ("EQ", "="):
                    sense = "="
                else:
                    print("❌ Sense must be LE, GE, or EQ.")
                    continue
                break
            except:
                print("❌ Invalid b or sense. Try again.")

        constraints.append({"a": a, "sense": sense, "b": b_val})

    return constraints


# ------------------------------------------------------------
# INTEGER CHECKS
# ------------------------------------------------------------
def is_integer(val, eps=1e-6):
    return abs(val - round(val)) < eps


def all_integer(x):
    return all(is_integer(v) for v in x)


# ------------------------------------------------------------
# BRANCH & BOUND (maximization, x >= 0, integer)
# ------------------------------------------------------------
def branch_and_bound(c, base_constraints):
    best_val = float("-inf")
    best_sol = None

    # Stack of subproblems: each is list of constraints
    stack = [base_constraints]

    while stack:
        cons = stack.pop()

        status, x_relax, z_relax, _ = big_m_simplex(c, cons, verbose=False)

        if status != "optimal":
            continue  # infeasible or unbounded or iterations exceeded → prune

        if z_relax <= best_val + 1e-6:
            continue  # bound not better → prune

        if all_integer(x_relax):
            if z_relax > best_val:
                best_val = z_relax
                best_sol = [round(v) for v in x_relax]
            continue

        # Branch on first fractional variable
        k = None
        for i, v in enumerate(x_relax):
            if not is_integer(v):
                k = i
                break

        if k is None:
            continue  # numeric weirdness

        xk = x_relax[k]
        floor_val = int(xk // 1)
        ceil_val = int(-(-xk // 1))  # ceil

        # LEFT: x_k <= floor(xk)
        left_cons = [dict(a=con["a"][:], sense=con["sense"], b=con["b"]) for con in cons]
        a_left = [0.0] * len(x_relax)
        a_left[k] = 1.0
        left_cons.append({"a": a_left, "sense": "<=", "b": float(floor_val)})

        # RIGHT: x_k >= ceil(xk)
        right_cons = [dict(a=con["a"][:], sense=con["sense"], b=con["b"]) for con in cons]
        a_right = [0.0] * len(x_relax)
        a_right[k] = 1.0
        right_cons.append({"a": a_right, "sense": ">=", "b": float(ceil_val)})

        stack.append(left_cons)
        stack.append(right_cons)

    if best_sol is None:
        return "no_integer_solution", None, None
    else:
        return "optimal", best_sol, best_val


# ------------------------------------------------------------
# MENU
# ------------------------------------------------------------
def menu():
    while True:
        print("\n=======================================")
        print("   OR TOOLKIT (BIG-M SIMPLEX + B&B)")
        print("=======================================")
        print("1) Solve LP (Max) with Simplex")
        print("2) Solve Integer LP (Max) with Branch & Bound")
        print("3) Exit")
        print("=======================================")

        choice = input("Choose option: ").strip()

        if choice == "1":
            n = int(input("\nNumber of variables: "))
            m = int(input("Number of constraints: "))

            c = read_float_list("Objective coefficients (Max Z): ", count=n)
            constraints = read_constraints(m, n)

            print("\n⚙ Solving LP using Big-M Simplex...\n")
            status, x_opt, Z_opt, var_names = big_m_simplex(c, constraints, verbose=True)

            print("\n================ LP RESULT ================")
            if status == "optimal":
                for i, v in enumerate(x_opt):
                    print(f"x{i+1} = {v}")
                print(f"Z = {Z_opt}")
            elif status == "infeasible":
                print("❌ Problem is infeasible.")
            elif status == "unbounded":
                print("❌ Problem is unbounded.")
            else:
                print("❌ Simplex stopped (iteration limit).")
            print("===========================================")

        elif choice == "2":
            n = int(input("\nNumber of variables (integer): "))
            m = int(input("Number of constraints: "))

            c = read_float_list("Objective coefficients (Max Z): ", count=n)
            constraints = read_constraints(m, n)

            print("\n⚙ Solving Integer LP using Branch & Bound...\n")
            status, x_int, Z_int = branch_and_bound(c, constraints)

            print("\n============== INTEGER RESULT =============")
            if status == "optimal":
                for i, v in enumerate(x_int):
                    print(f"x{i+1} = {v}")
                print(f"Z* = {Z_int}")
            else:
                print("❌ No feasible integer solution found.")
            print("===========================================")

        elif choice == "3":
            print("Exiting. Bye!")
            break
        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    menu()
