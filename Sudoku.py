import tkinter as tk
from tkinter import messagebox
import random

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
        display_solution(board, N)
    else:
        messagebox.showinfo("Sudoku Solver", "No solution exists.")

def display_solution(board, N):
    for i in range(N):
        for j in range(N):
            if entries[i][j] is not None:
                entries[i][j].delete(0, tk.END)  
                entries[i][j].insert(0, board[i][j])  

def clear_grid():
    N = int(dim_entry.get())
    for i in range(N):
        for j in range(N):
            if entries[i][j] is not None:
                entries[i][j].delete(0, tk.END)  

def generate_puzzle():
    N = int(dim_entry.get())
    board = [[0] * N for _ in range(N)]
    fill_diagonal_blocks(board, N)
    solve_sudoku(board, N)
    remove_numbers(board, N)
    display_solution(board, N)

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

def remove_numbers(board, N):
    num_remove = N*N // 3
    for _ in range(num_remove):
        row = random.randint(0, N-1)
        col = random.randint(0, N-1)
        board[row][col] = 0

def create_grid():
    N = int(dim_entry.get())
    clear_grid()  
    for i in range(N):
        for j in range(N):
            entry = tk.Entry(root, width=3, font=('Arial', 18), justify='center')
            entry.grid(row=i+2, column=j, padx=5, pady=5)
            entries[i][j] = entry  

root = tk.Tk()
root.title("Sudoku Solver & Generator")

entries = [[None for _ in range(16)] for _ in range(16)]  
dim_label = tk.Label(root, text="Enter the dimension (e.g., 9 for 9x9):")
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
