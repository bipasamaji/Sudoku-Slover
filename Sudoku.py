#Third added the Sudoku Generator and added a menu for dimensions 

import tkinter as tk
from tkinter import messagebox
import random

# Function to check if a number can be placed in the current row, column, and subgrid
def is_valid(board, row, col, num, N):
    for x in range(N):
        if board[row][x] == num or board[x][col] == num:
            return False

    sqrt_N = int(N ** 0.5)
    start_row = row - row % sqrt_N
    start_col = col - col % sqrt_N
    for i in range(sqrt_N):
        for j in range(sqrt_N):
            if board[i + start_row][j + start_col] == num:
                return False

    return True

# Backtracking algorithm to solve the Sudoku puzzle
def solve_sudoku(board, N):
    empty_cell = find_empty_location(board, N)
    if not empty_cell:
        return True
    row, col = empty_cell

    for num in range(1, N+1):
        if is_valid(board, row, col, num, N):
            board[row][col] = num
            if solve_sudoku(board, N):
                return True
            board[row][col] = 0

    return False

# Find the next empty location
def find_empty_location(board, N):
    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:
                return i, j
    return None

# Function to solve the user-entered puzzle
def solve_puzzle():
    N = int(dim_entry.get())
    board = []
    for i in range(N):
        row = []
        for j in range(N):
            if entries[i][j] is not None:
                try:
                    value = int(entries[i][j].get())  # Fetch the current value from Entry
                except ValueError:
                    value = 0
                row.append(value)
            else:
                row.append(0)
        board.append(row)

    if solve_sudoku(board, N):
        display_solution(board, N)
    else:
        messagebox.showinfo("Sudoku Solver", "No solution exists.")

# Function to display the solution
def display_solution(board, N):
    for i in range(N):
        for j in range(N):
            if entries[i][j] is not None:
                entries[i][j].delete(0, tk.END)  # Clear the entry first
                entries[i][j].insert(0, board[i][j])  # Insert the solved value

# Function to clear the grid
def clear_grid():
    N = int(dim_entry.get())
    for i in range(N):
        for j in range(N):
            if entries[i][j] is not None:
                entries[i][j].delete(0, tk.END)  # Clear the entry widget

# Function to generate a random puzzle
def generate_puzzle():
    N = int(dim_entry.get())
    board = [[0] * N for _ in range(N)]
    fill_diagonal_blocks(board, N)
    solve_sudoku(board, N)
    remove_numbers(board, N)
    display_solution(board, N)

# Fill diagonal blocks to ensure solvability
def fill_diagonal_blocks(board, N):
    sqrt_N = int(N ** 0.5)
    for i in range(0, N, sqrt_N):
        fill_block(board, i, i, N)

def fill_block(board, row, col, N):
    nums = random.sample(range(1, N+1), N)
    sqrt_N = int(N ** 0.5)
    for i in range(sqrt_N):
        for j in range(sqrt_N):
            board[row + i][col + j] = nums.pop()

# Remove random numbers to create a puzzle
def remove_numbers(board, N):
    num_remove = N*N // 3
    for _ in range(num_remove):
        row = random.randint(0, N-1)
        col = random.randint(0, N-1)
        board[row][col] = 0

# Function to dynamically generate the input grid based on the dimensions
def create_grid():
    N = int(dim_entry.get())
    clear_grid()  # Clear previous grid before creating a new one
    for i in range(N):
        for j in range(N):
            entry = tk.Entry(root, width=3, font=('Arial', 18), justify='center')
            entry.grid(row=i+2, column=j, padx=5, pady=5)
            entries[i][j] = entry  # Store the entry widget in the entries array

# Main GUI setup
root = tk.Tk()
root.title("Sudoku Solver & Generator")

entries = [[None for _ in range(16)] for _ in range(16)]  # Max size is 16x16

dim_label = tk.Label(root, text="Enter the dimension (e.g., 9 for 9x9):")
dim_label.grid(row=0, column=0, columnspan=4)
dim_entry = tk.Entry(root)
dim_entry.grid(row=0,column=4,columnspan=2)
generate_button = tk.Button(root, text="Generate Sudoku", command=generate_puzzle)
generate_button.grid(row=1, column=0, columnspan=3)

solve_button = tk.Button(root, text="Solve Puzzle", command=solve_puzzle)
solve_button.grid(row=1, column=3, columnspan=3)

clear_button = tk.Button(root, text="Clear Grid", command=clear_grid)
clear_button.grid(row=1, column=6, columnspan=3)

create_grid_button = tk.Button(root, text="Create Grid", command=create_grid)
create_grid_button.grid(row=1, column=9, columnspan=3)

root.mainloop()