📊 OR Toolkit — Big-M Simplex + Branch & Bound (Python)

A terminal-based Operations Research toolkit implemented in pure Python, designed for academic usage and step-by-step LP solving.

🚀 Supports

Linear Programming (Maximization)

Branch & Bound for Integer Programming

Big-M Simplex with:

Slack variables

Surplus variables

Artificial variables

General constraints:

<= (less-than equal)

>= (greater-than equal)

= (equality)

No external libraries required

Full simplex tableau printed at every iteration

✅ Why This Is Useful

Most student simplex implementations only work for <= constraints.
This solver is more academically correct, because:

<= constraints → slack

>= constraints → surplus + artificial

= constraints → artificial

Big-M method builds a valid initial BFS

Works fully for both LP and Integer LP

Branch & Bound uses the same LP solver internally

🧠 This is a fully transparent educational solver, ideal for exams or OR learning.

✨ Features
Linear Programming (Simplex — Max)

Fully handles: <=, >=, =

Builds valid Basic Feasible Solutions using Big-M

Tableau printed at every iteration

Detects infeasibility using artificial variables

Detects unboundedness

Safe pivoting with iteration limits

Integer Programming (Branch & Bound)

Relaxation solved using the same Big-M simplex

Integer feasibility check

Automatic branching rules:

xk ≤ floor(xk)

xk ≥ ceil(xk)

Pure Python — runs offline

🧩 Input Format
Objective Function

For:

Max Z = 100 x1 + 150 x2


Enter:

100 150

Constraint Format

Each constraint has two parts:

1️⃣ Coefficient row
2️⃣ RHS + sense (LE / GE / EQ)

Example:

A Row 1: 15 30
b[1] and sense: 200 LE


Multiple constraints example:

A Row 1: 15 30
b[1] and sense: 200 LE

A Row 2: 8 4
b[2] and sense: 40 LE

A Row 3: 1 0
b[3] and sense: 2 GE

Valid sense types
Input	Meaning
LE or <=	≤ constraint
GE or >=	≥ constraint
EQ or =	Equality
🖥️ How to Run
python or_toolkit.py


Main menu:

=======================================
   OR TOOLKIT (BIG-M SIMPLEX + B&B)
=======================================
1) Solve LP (Max) with Simplex
2) Solve Integer LP (Max) with Branch & Bound
3) Exit
=======================================

🔍 Example — LP Maximization

Example input

Number of variables: 2
Number of constraints: 3

Objective coefficients: 100 150

A Row 1: 15 30
b[1] and sense: 200 LE

A Row 2: 8 4
b[2] and sense: 40 LE

A Row 3: 1 0
b[3] and sense: 2 GE


The solver will:

Add slack/surplus/artificial variables automatically

Build a valid BFS using Big-M

Run simplex pivot iterations

Print every tableau

Display optimal solution

🕌 Example — Integer Programming

Choose option 2 in the menu.

Number of variables: 2
Number of constraints: 2

Objective coefficients: 100 150

A Row 1: 15 30
b[1] and sense: 200 LE

A Row 2: 8 4
b[2] and sense: 40 LE


Output:

Optimal integer solution found:
x1 = …
x2 = …
Z* = …

⚙️ Internal Mechanics (For Academic Study)
Constraint processing

Ensures RHS ≥ 0

If RHS < 0 → multiply:

coefficients

RHS

flip inequality direction

Constraint transformations
Constraint Type	Tableau Representation
<=	+ slack
>=	– surplus + artificial
=	+ artificial
Big-M objective row adjustment

Artificial variables added with –M penalty

Basic artificial rows projected into objective row

Pivot rules

Entering: most negative objective coefficient

Leaving: minimum ratio test

Artificial feasibility check:

any artificial > 0 ⇒ infeasible

Branch & Bound Logic

Solve LP relaxation using Big-M simplex

If integer → save solution

If fractional:

split on variable xk:

xk ≤ floor(xk)

xk ≥ ceil(xk)

Continue recursively until best integer optimum is found

🛡️ Numerical Safety

EPS tolerance

Max iteration safeguard

Detects:

infeasible

unbounded

numerical degeneracy

🚫 Known Limitations

Only maximization (minimization coming soon)

No dual outputs

No sensitivity analysis yet

Terminal UI only

Fraction formatting is decimal, not symbolic

🎓 Academic Use Cases

This toolkit is perfect for:

OR Assignments

Exam labs

Tableau demonstrations

Viva preparation

Integer programming tutorials

Classroom teaching

🧾 Students can verify hand calculations step-by-step using the printed tableaux.

🔮 Future Enhancements

Planned:

Minimization support

Sensitivity analysis

Two-Phase simplex mode

Dual simplex

CSV / file export for tableaus

Fraction visualization

GUI version

🧑‍💻 Author

Developed collaboratively with ChatGPT to provide a transparent & exam-ready OR solver for students and instructors.

⭐ Support

If this project helps with your coursework, please star the repo ⭐ — it helps more students learn Operations Research without black-box solvers.

📝 License

MIT License — open source and free to use for learning, research, or assignment work.

❤️ Contributions Welcome

PRs invited for:

Minimization models

GUI implementations

Two-phase method

Export utilities
