def simplex(c, A, b):
    """
    Solve max c^T x subject to A x <= b, x >= 0
    Returns (optimum, x), or raises ValueError if unbounded.
    """
    m, n = len(A), len(c)
    # Build initial tableau: (m+1) rows, (n+m+1) columns
    # Columns: [x0..x_{n-1}, s0..s_{m-1}, RHS]
    tableau = [row[:] + [0]*m + [b_i] for row, b_i in zip(A, b)]
    # identity for slacks
    for i in range(m):
        tableau[i][n + i] = 1
    # objective row
    tableau.append([-ci for ci in c] + [0]*m + [0])

    def pivot(row, col):
        # Divide pivot row
        pivot_val = tableau[row][col]
        tableau[row] = [v / pivot_val for v in tableau[row]]
        # Zero out other rows
        for r in range(len(tableau)):
            if r != row:
                factor = tableau[r][col]
                tableau[r] = [
                    tableau[r][j] - factor * tableau[row][j]
                    for j in range(len(tableau[0]))
                ]

    while True:
        # 1) Find entering col (first negative in bottom row)
        bottom = tableau[-1]
        try:
            entering = next(j for j, v in enumerate(bottom[:-1]) if v < 0)
        except StopIteration:
            break  # optimal

        # 2) Find leaving row (min ratio test)
        ratios = []
        for i in range(m):
            a_ij = tableau[i][entering]
            if a_ij > 0:
                ratios.append((tableau[i][-1] / a_ij, i))
        if not ratios:
            raise ValueError("Unbounded solution")

        _, leaving = min(ratios)
        # 3) Pivot
        pivot(leaving, entering)

    # Extract solution
    x = [0]*n
    for j in range(n):
        # find if column j is basic (one 1 and the rest 0s)
        col = [tableau[i][j] for i in range(m)]
        if col.count(1) == 1 and col.count(0) == m-1:
            i = col.index(1)
            x[j] = tableau[i][-1]
    optimum = tableau[-1][-1]
    return optimum, x

c = [3, 2]
A = [[2, 1],
     [1, 2],
     [1, 0]]
b = [18, 18, 8]
opt, x = simplex(c, A, b)
print("Optimal value:", opt)   # 36
print("x:", x)    
