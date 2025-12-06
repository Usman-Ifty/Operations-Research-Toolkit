📊 OR Toolkit – Big-M Simplex + Branch & Bound Solver (Python)

A terminal-based Operations Research toolkit implemented in pure Python, designed for academic usage and step-by-step LP solving.
Supports:

Linear Programming (LP) Maximization

Branch & Bound for Integer Programming

Big-M Simplex with slack, surplus, and artificial variables

≤, ≥, and = constraints

No external dependencies

Simplex tableau printed at every iteration for learning or exam practice

✔ Works offline
✔ Pure Python
✔ Transparent simplex iterations
✔ Perfect for Operations Research assignments, exams, and viva

🧠 Why This Solver Is Special

Typical simple simplex implementations only support ≤ constraints and cannot correctly solve ≥ or = constraints.

This toolkit uses the Big-M method, allowing it to:

Add slack variables for ≤ constraints

Add surplus + artificial variables for ≥ constraints

Add artificial variables for = constraints

Automatically build a valid initial BFS

Solve LPs with general inequality structure

Use the same LP solver inside Branch & Bound

This makes it a fully correct academic implementation.

✨ Features
Linear Programming (Simplex)

Maximization problems

Fully supports constraints: ≤, ≥, =

Full tableau printing at every iteration

Artificial variable detection (infeasibility check)

Safe iteration protection

Integer Programming

Uses Branch & Bound

LP relaxation solved using the same Big-M simplex

Integer feasibility check

Branching:

xk ≤ floor(xk)

xk ≥ ceil(xk)

No External Libraries

Pure Python

Can be run in an exam lab without installing dependencies

🏷️ Input Format
Objective Function

Example:

Max Z = 100 x1 + 150 x2


You enter:

100 150

Constraint Format

Each constraint consists of:

Coefficient row

b and sense (LE, GE, or EQ)

Example:

A Row 1: 15 30
b[1] and sense: 200 LE

A Row 2: 8 4
b[2] and sense: 40 LE

A Row 3: 1 0
b[3] and sense: 2 GE


Valid sense types:

LE or <=

GE or >=

EQ or =

🖥️ How to Run
python or_toolkit.py


Menu appears:

=======================================
   OR TOOLKIT (BIG-M SIMPLEX + B&B)
=======================================
1) Solve LP (Max) with Simplex
2) Solve Integer LP (Max) with Branch & Bound
3) Exit
=======================================

🔍 Example LP Use
Number of variables: 2
Number of constraints: 3
Objective: 100 150
A Row 1: 15 30
b[1] and sense: 200 LE
A Row 2: 8 4
b[2] and sense: 40 LE
A Row 3: 1 0
b[3] and sense: 2 GE


The solver will:

Build slack/surplus/artificial variables

Run Big-M Simplex

Print every tableau

Show optimal Z and x values

🕌 Example Integer Problem (Branch & Bound)

Choose menu option 2:

Number of variables: 2
Number of constraints: 2
Objective: 100 150
A Row 1: 15 30
b[1] and sense: 200 LE
A Row 2: 8 4
b[2] and sense: 40 LE


The solver prints:

Optimal integer solution found:
x1 = ...
x2 = ...
Z* = ...

🧬 How It Works Internally

Constraint preprocessing ensures RHS ≥ 0

≥ constraints are transformed using:

Surplus (-1)

Artificial (+1)

Objective row is adjusted using:

+M artificial coefficients

−M artificial basic row projection

Pivot steps use:

Most negative entering variable

Minimum ratio test

Artificial feasibility check ensures:

If any artificial variable > 0 ⇒ infeasible

Branch & Bound:

Solves LP relaxation first

Checks integer feasibility

Adds two branching constraints:

xk ≤ floor(xk)

xk ≥ ceil(xk)

🛡️ Numerical Safety

Implemented safeguards:

Max iteration limit

EPS tolerance

Infeasibility detection

Unbounded detection

Integer rounding only after feasibility

🚫 Limitations

Only maximization supported in this version

No column merging/variable removal

No sensitivity analysis yet

No graphical UI (terminal based)

🎓 Academic Use Cases

OR Assignments

LP Viva Exams

Integer Programming Tutorials

Classroom Demonstrations

Hand-based tableau verification

This is not a black-box solver — it shows the entire simplex iteration process clearly.

✨ Future Enhancements (Planned)

Minimization support

Sensitivity analysis

Two-Phase simplex mode

Dual simplex

Save tableaux to file

Automatic Z row labeling

Fraction visualization

🧑‍💻 Author

This solver was written collaboratively with the assistance of ChatGPT to serve as a transparent, educational alternative to large OR libraries.

⭐ Star the Repo

If this project helps you in your academic work, give it a ⭐ on GitHub 🙌
Sharing helps more students learn OR properly without external solvers.

🙌 Contributions

PRs welcome for:

Minimization models

Two-Phase version

Graphical UI

Tableau saving / CSV / export

🏁 License

MIT License — free to use, study, and improve.