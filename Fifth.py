#Final With colors


import tkinter as tk
from tkinter import messagebox
import random

def is_valid(board, row, col, num, N):
    sqrt_N = int(N ** 0.5)
    if sqrt_N ** 2 != N:
        return False
    for x in range(N):
        if board[row][x] == num or board[x][col] == num:
            return False
    start_row = row - row % sqrt_N
    start_col = col - col % sqrt_N
    for i in range(sqrt_N):
        for j in range(sqrt_N):
            if board[i + start_row][j + start_col] == num:
                return False
    return True

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

def find_empty_location(board, N):
    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:
                return i, j
    return None

def solve_puzzle():
    N = int(dim_entry.get())
    if not is_valid_size(N):
        messagebox.showinfo("Sudoku Solver", "Invalid size! Please enter 4, 9, or 16.")
        return
    board = []
    for i in range(N):
        row = []
        for j in range(N):
            if entries[i][j] is not None:
                try:
                    value = int(entries[i][j].get())
                except ValueError:
                    value = 0
                row.append(value)
            else:
                row.append(0)
        board.append(row)
    if solve_sudoku(board, N):
        display_solution(board, N, from_solver=True)
    else:
        messagebox.showinfo("Sudoku Solver", "No solution exists.")

def display_solution(board, N, from_solver=False):
    for i in range(N):
        for j in range(N):
            if entries[i][j] is not None:
                current_value = entries[i][j].get()
                if current_value == '' or current_value == '0':
                    entries[i][j].delete(0, tk.END)
                    entries[i][j].insert(0, board[i][j])
                    if from_solver:
                        entries[i][j].config(fg="blue")
                    else:
                        entries[i][j].config(fg="black")
                else:
                    entries[i][j].config(fg="black")

def clear_grid():
    N = int(dim_entry.get())
    for i in range(16):
        for j in range(16):
            if entries[i][j] is not None:
                entries[i][j].delete(0, tk.END)
                entries[i][j].grid_remove()
                entries[i][j].config(fg="black")

def generate_puzzle():
    N = int(dim_entry.get())
    if not is_valid_size(N):
        messagebox.showinfo("Sudoku Generator", "Invalid size! Please enter 4, 9, or 16.")
        return
    board = [[0] * N for _ in range(N)]
    solve_sudoku(board, N)
    remove_numbers(board, N)
    display_solution(board, N)

def remove_numbers(board, N):
    num_remove = N*N // 3
    removed_positions = set()
    while len(removed_positions) < num_remove:
        row = random.randint(0, N-1)
        col = random.randint(0, N-1)
        if (row, col) not in removed_positions:
            board[row][col] = 0
            removed_positions.add((row, col))

def is_valid_size(N):
    sqrt_N = int(N ** 0.5)
    return sqrt_N ** 2 == N

def create_grid():
    clear_grid()
    N = int(dim_entry.get())
    if not is_valid_size(N):
        messagebox.showinfo("Sudoku Grid", "Invalid size! Please enter 4, 9, or 16.")
        return
    for i in range(N):
        for j in range(N):
            entry = tk.Entry(root, width=3, font=('Arial', 18), justify='center')
            entry.grid(row=i+2, column=j, padx=5, pady=5)
            entries[i][j] = entry
            entries[i][j].grid()

root = tk.Tk()
root.title("Sudoku Solver & Generator")

entries = [[None for _ in range(16)] for _ in range(16)]

dim_label = tk.Label(root, text="Enter the dimension (4, 9, 16):")
dim_label.grid(row=0, column=0, columnspan=4)
dim_entry = tk.Entry(root)
dim_entry.grid(row=0, column=4, columnspan=2)

generate_button = tk.Button(root, text="Generate Sudoku", command=generate_puzzle)
generate_button.grid(row=1, column=0, columnspan=3)

solve_button = tk.Button(root, text="Solve Puzzle", command=solve_puzzle)
solve_button.grid(row=1, column=3, columnspan=3)

clear_button = tk.Button(root, text="Clear Grid", command=clear_grid)
clear_button.grid(row=1, column=6, columnspan=3)

create_grid_button = tk.Button(root, text="Create Grid", command=create_grid)
create_grid_button.grid(row=1, column=9, columnspan=3)

root.mainloop()