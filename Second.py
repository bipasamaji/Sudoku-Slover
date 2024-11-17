#Second Input sudoku and added GUI



import tkinter as tk
from tkinter import messagebox

# Function to check if a number can be placed in the current row, column, and 3x3 subgrid
def is_valid(board, row, col, num):
    for x in range(9):
        if board[row][x] == num or board[x][col] == num:
            return False

    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False

    return True

# Backtracking algorithm to solve the Sudoku puzzle
def solve_sudoku(board):
    empty_cell = find_empty_location(board)
    if not empty_cell:
        return True
    row, col = empty_cell

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0

    return False

def find_empty_location(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

# Function to read the board from the GUI and solve it
def solve_puzzle():
    board = []
    for i in range(9):
        row = []
        for j in range(9):
            try:
                value = int(entries[i][j].get())
            except ValueError:
                value = 0
            row.append(value)
        board.append(row)

    if solve_sudoku(board):
        display_solution(board)
    else:
        messagebox.showinfo("Sudoku Solver", "No solution exists.")

# Function to display the solution on the GUI
def display_solution(board):
    for i in range(9):
        for j in range(9):
            entries[i][j].delete(0, tk.END)
            entries[i][j].insert(0, board[i][j])

# Function to clear the grid
def clear_grid():
    for i in range(9):
        for j in range(9):
            entries[i][j].delete(0, tk.END)

# Main GUI setup
root = tk.Tk()
root.title("Sudoku Solver")

entries = [[None for _ in range(9)] for _ in range(9)]

# Create a grid of entries (9x9)
for i in range(9):
    for j in range(9):
        entry = tk.Entry(root, width=3, font=('Arial', 18), justify='center')
        entry.grid(row=i, column=j, padx=5, pady=5)
        entries[i][j] = entry

# Solve button
solve_button = tk.Button(root, text="Solve", command=solve_puzzle)
solve_button.grid(row=10, column=0, columnspan=4)

# Clear button
clear_button = tk.Button(root, text="Clear", command=clear_grid)
clear_button.grid(row=10, column=5, columnspan=4)

# Run the Tkinter main loop
root.mainloop()