import numpy as np
import math
from collections import deque

def simplex(c, A, b):
    """
    Solve max c^T x subject to A x <= b, x >= 0
    Returns (optimum, x), or raises ValueError if unbounded.
    (This is your original simplex code)
    """
    m, n = len(A), len(c)
    tableau = [row[:] + [0]*m + [b_i] for row, b_i in zip(A, b)]
    for i in range(m):
        tableau[i][n + i] = 1
    tableau.append([-ci for ci in c] + [0]*m + [0])

    def pivot(row, col):
        pivot_val = tableau[row][col]
        tableau[row] = [v / pivot_val for v in tableau[row]]
        for r in range(len(tableau)):
            if r != row:
                factor = tableau[r][col]
                tableau[r] = [tableau[r][j] - factor * tableau[row][j] for j in range(len(tableau[0]))]

    while True:
        bottom = tableau[-1]
        try:
            entering = next(j for j, v in enumerate(bottom[:-1]) if v < 0)
        except StopIteration:
            break
        ratios = [(tableau[i][-1] / tableau[i][entering], i) for i in range(m) if tableau[i][entering] > 0]
        if not ratios:
            raise ValueError("Unbounded solution")
        _, leaving = min(ratios)
        pivot(leaving, entering)

    x = [0]*n
    for j in range(n):
        col = [tableau[i][j] for i in range(m)]
        if col.count(1) == 1 and col.count(0) == m-1:
            i = col.index(1)
            x[j] = tableau[i][-1]
    return tableau[-1][-1], x

# =====================================================================================
# Branch and Bound function to solve Integer Linear Programs
# =====================================================================================
def branch_and_bound_ilp(c, A, b):
    """
    Solves an ILP using the Branch and Bound method.
    It uses the provided simplex function to solve LP relaxations.
    """
    # Initialize the queue with the root problem (original constraints)
    queue = deque([(np.array(A), np.array(b))])
    
    best_objective = -float('inf')
    best_solution = None

    while queue:
        # Get the next subproblem to evaluate
        current_A, current_b = queue.popleft()

        try:
            # Solve the LP relaxation of the subproblem
            lp_opt, lp_x = simplex(c, current_A.tolist(), current_b.tolist())
        except ValueError:
            # If the subproblem is unbounded or infeasible, prune this branch
            continue

        # --- Pruning by Bound ---
        # If this branch's best possible outcome is worse than our best integer
        # solution found so far, there's no need to explore it further.
        if lp_opt <= best_objective:
            continue

        # --- Check for Integer Solution ---
        # Find variables that are not close to an integer value
        fractional_vars = [(i, val) for i, val in enumerate(lp_x) if abs(val - round(val)) > 1e-9]

        if not fractional_vars:
            # This is a valid integer solution.
            if lp_opt > best_objective:
                # We found a new, better integer solution!
                best_objective = lp_opt
                best_solution = lp_x
            # Prune this branch, as we've found an integer solution here.
            continue
        
        # --- Branching ---
        # If we get here, the solution is fractional. We must branch.
        # Choose the first fractional variable to branch on.
        branch_var_index, branch_var_value = fractional_vars[0]

        # Branch 1: Add constraint x_i <= floor(value)
        new_row_A1 = np.zeros(len(c))
        new_row_A1[branch_var_index] = 1
        A1 = np.vstack([current_A, new_row_A1])
        b1 = np.append(current_b, math.floor(branch_var_value))
        queue.append((A1, b1))

        # Branch 2: Add constraint x_i >= ceil(value)  (i.e., -x_i <= -ceil(value))
        new_row_A2 = np.zeros(len(c))
        new_row_A2[branch_var_index] = -1
        A2 = np.vstack([current_A, new_row_A2])
        b2 = np.append(current_b, -math.ceil(branch_var_value))
        queue.append((A2, b2))

    return best_objective, best_solution

# --- Example Usage ---
# Original LP problem
c = [3, 2]        # maximize 3x + 2y
A = [[2, 1],
     [1, 2],
     [1, 0]]
b = [18, 18, 8]

# Solve as an LP
lp_opt, lp_x = simplex(c, A, b)
print("--- LP Solution (Relaxed) ---")
print(f"Optimal value: {lp_opt}")
print(f"x: {lp_x}\n")

# Solve as an ILP
ilp_opt, ilp_x = branch_and_bound_ilp(c, A, b)
print("--- ILP Solution (Branch and Bound) ---")
print(f"Optimal value: {ilp_opt}")
print(f"x: {ilp_x}")
