import sys
import numpy as np
import copy

def get_candidates(board):
    """
    Returns a 9x9x9 boolean array where candidates[i, j, k] is True if k+1 is a candidate for cell (i, j).
    """
    candidates = np.ones((9, 9, 9), dtype=bool)
    
    # If a cell is filled, it has no candidates (or only itself, but we treat filled separately)
    # Actually, let's make it so filled cells have NO candidates in this array to simplify counting
    
    for r in range(9):
        for c in range(9):
            val = board[r, c]
            if val != 0:
                candidates[r, c, :] = False
                # Remove val from peers
                candidates[r, :, val-1] = False
                candidates[:, c, val-1] = False
                
                # Block
                br, bc = (r // 3) * 3, (c // 3) * 3
                candidates[br:br+3, bc:bc+3, val-1] = False
                
    return candidates

def is_valid(board):
    """
    Checks if the current board state is valid (no duplicates in rows, cols, blocks).
    """
    for i in range(9):
        # Row
        row = board[i, :]
        row = row[row != 0]
        if len(row) != len(np.unique(row)):
            return False
        # Col
        col = board[:, i]
        col = col[col != 0]
        if len(col) != len(np.unique(col)):
            return False
        
    for r in range(0, 9, 3):
        for c in range(0, 9, 3):
            block = board[r:r+3, c:c+3].flatten()
            block = block[block != 0]
            if len(block) != len(np.unique(block)):
                return False
    return True

def junior_step(board):
    """
    Performs one step of logical elimination.
    Returns (new_board, changed).
    """
    changed = False
    new_board = board.copy()
    
    # 1. Update candidates based on current board
    candidates = get_candidates(new_board)
    
    # 2. Check for Single Candidates (Naked Singles)
    # If a cell has only 1 possible candidate, fill it.
    for r in range(9):
        for c in range(9):
            if new_board[r, c] == 0:
                opts = np.where(candidates[r, c, :])[0]
                if len(opts) == 0:
                    # No candidates for empty cell -> Invalid path, but we just return unchanged here
                    # The validity check will catch it later or it will be stuck
                    return new_board, False 
                if len(opts) == 1:
                    val = opts[0] + 1
                    new_board[r, c] = val
                    changed = True
                    # Update candidates immediately for next iterations in this loop? 
                    # For simplicity, we restart the loop (return changed=True)
                    return new_board, True

    # 3. Check for Hidden Singles (Unique position for a candidate in a unit)
    # For each number 1-9, check rows, cols, blocks
    for val in range(1, 10):
        val_idx = val - 1
        
        # Rows
        for r in range(9):
            if val not in new_board[r, :]:
                # Where can 'val' go in this row?
                possible_cols = []
                for c in range(9):
                    if new_board[r, c] == 0 and candidates[r, c, val_idx]:
                        possible_cols.append(c)
                if len(possible_cols) == 1:
                    new_board[r, possible_cols[0]] = val
                    changed = True
                    return new_board, True
        
        # Cols
        for c in range(9):
            if val not in new_board[:, c]:
                possible_rows = []
                for r in range(9):
                    if new_board[r, c] == 0 and candidates[r, c, val_idx]:
                        possible_rows.append(r)
                if len(possible_rows) == 1:
                    new_board[possible_rows[0], c] = val
                    changed = True
                    return new_board, True

        # Blocks
        for br in range(0, 9, 3):
            for bc in range(0, 9, 3):
                block = new_board[br:br+3, bc:bc+3]
                if val not in block:
                    possible_pos = []
                    for r in range(br, br+3):
                        for c in range(bc, bc+3):
                            if new_board[r, c] == 0 and candidates[r, c, val_idx]:
                                possible_pos.append((r, c))
                    if len(possible_pos) == 1:
                        r, c = possible_pos[0]
                        new_board[r, c] = val
                        changed = True
                        return new_board, True

    return new_board, changed

def junior(board):
    """
    Repeatedly applies logical elimination until stuck.
    """
    curr_board = board.copy()
    while True:
        if not is_valid(curr_board):
            return None # Invalid state
        
        curr_board, changed = junior_step(curr_board)
        if not changed:
            break
            
    if not is_valid(curr_board):
        return None
        
    return curr_board

def solve_recursive(board):
    # 1. Apply logic (Junior)
    board = junior(board)
    if board is None:
        return None # Dead end
    
    # 2. Check if done
    if np.all(board != 0):
        return board
    
    # 3. Senior: Find cell with fewest candidates to branch
    candidates = get_candidates(board)
    min_len = 10
    best_cell = None
    
    for r in range(9):
        for c in range(9):
            if board[r, c] == 0:
                opts = np.where(candidates[r, c, :])[0]
                if len(opts) == 0:
                    return None # Empty cell with no candidates -> Dead end
                if len(opts) < min_len:
                    min_len = len(opts)
                    best_cell = (r, c)
    
    if best_cell is None:
        return None # Should not happen if board is not full
        
    r, c = best_cell
    opts = np.where(candidates[r, c, :])[0] + 1
    
    # Try each candidate
    for val in opts:
        new_state = board.copy()
        new_state[r, c] = val
        result = solve_recursive(new_state)
        if result is not None:
            return result
            
    return None

def parse_input(filepath):
    """
    Reads a 9x9 matrix from a file.
    Supports space/comma separated, or continuous strings.
    """
    with open(filepath, 'r') as f:
        content = f.read().strip().splitlines()
    
    matrix = []
    for line in content:
        # Remove brackets if present (MATLAB style)
        line = line.replace('[', '').replace(']', '').replace(';', '')
        if not line.strip(): continue
        
        # Try splitting by comma or space
        parts = line.replace(',', ' ').split()
        row = [int(p) for p in parts]
        if len(row) > 0:
            matrix.append(row)
            
    # If it's a flat list of 81 numbers
    if len(matrix) == 1 and len(matrix[0]) == 81:
        return np.array(matrix[0]).reshape(9, 9)
        
    return np.array(matrix)

def print_board(board):
    for r in range(9):
        if r % 3 == 0 and r != 0:
            print("-" * 21)
        for c in range(9):
            if c % 3 == 0 and c != 0:
                print("|", end=" ")
            print(board[r, c], end=" ")
        print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sudoku_solve.exe <input_file>")
        print("Input file should contain the Sudoku puzzle (0 for empty cells).")
        input("Press Enter to exit...")
        sys.exit(1)
        
    input_file = sys.argv[1]
    try:
        board = parse_input(input_file)
        print("Input Puzzle:")
        print_board(board)
        print("\nSolving...\n")
        
        solution = solve_recursive(board)
        
        if solution is not None:
            print("Solution Found:")
            print_board(solution)
            
            # Save to file
            np.savetxt("sudoku_solution.txt", solution, fmt='%d')
            print("\nSolution saved to sudoku_solution.txt")
        else:
            print("No solution found.")
            
    except Exception as e:
        print(f"Error: {e}")
     
        import traceback
        traceback.print_exc()
    
    # Keep window open if run from double-click
    # input("Press Enter to exit...")
