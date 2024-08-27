import tkinter as tk
from tkinter import messagebox

# Initialize scores and settings
score_x = 0
score_o = 0
game_started = False
series_length = 3
wins_needed = 2
current_wins_x = 0
current_wins_o = 0

def update_score():
    """Update the score labels."""
    label_score_x.config(text=f"{player_x_name.get()}: {score_x} (Wins: {current_wins_x})")
    label_score_o.config(text=f"{player_o_name.get()}: {score_o} (Wins: {current_wins_o})")

def check_winner():
    """Check if there's a winner based on diagonal winning rule."""
    winning_combinations = [
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]]
    ]
    
    for combo in winning_combinations:
        if combo[0] == combo[1] == combo[2] != "":
            return combo[0]
    return None

def button_click(row, col):
    global current_player, winner, score_x, score_o, current_wins_x, current_wins_o
    if not game_started:
        return
    if board[row][col] == "" and winner is None:
        board[row][col] = current_player
        symbol = player_x_symbol.get() if current_player == "X" else player_o_symbol.get()
        buttons[row][col].config(text=symbol, fg="red")
        winner = check_winner()
        if winner:
            winner_name = player_x_name.get() if winner == "X" else player_o_name.get()
            messagebox.showinfo("Tic-Tac-Toe", f"🎉 Congratulations, {winner_name}! You won this round! 🎉")
            if winner == "X":
                score_x += 1
                current_wins_x += 1
            else:
                score_o += 1
                current_wins_o += 1
            update_score()  # Update the score display
            
            if current_wins_x == wins_needed:
                messagebox.showinfo("Tic-Tac-Toe", f"{player_x_name.get()} wins the series!")
                reset_game(full_reset=True)
            elif current_wins_o == wins_needed:
                messagebox.showinfo("Tic-Tac-Toe", f"{player_o_name.get()} wins the series!")
                reset_game(full_reset=True)
            else:
                continue_game()  # Start the next round
        elif all(board[row][col] != "" for row in range(3) for col in range(3)):
            messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
            continue_game()  # Start the next round
        else:
            current_player = "O" if current_player == "X" else "X"

def start_game():
    global game_started, series_length, wins_needed, current_wins_x, current_wins_o
    game_started = True
    start_button.grid_forget()
    player_x_name.config(state=tk.DISABLED)
    player_o_name.config(state=tk.DISABLED)
    player_x_symbol_menu.config(state=tk.DISABLED)
    player_o_symbol_menu.config(state=tk.DISABLED)
    series_menu.config(state=tk.DISABLED)
    
    # Set the number of wins needed based on the series length
    series_length = int(series_choice.get())
    wins_needed = (series_length // 2) + 1
    
    current_wins_x = 0
    current_wins_o = 0
    
    update_score()
    create_board()  # Initialize the game board

def reset_game(full_reset=False):
    global current_player, winner, score_x, score_o, game_started
    current_player = "X"
    winner = None
    for row in range(3):
        for col in range(3):
            board[row][col] = ""
            if buttons[row][col]:
                buttons[row][col].grid_forget()

    if full_reset:
        game_started = False
        score_x = 0
        score_o = 0
        player_x_name.config(state=tk.NORMAL)
        player_o_name.config(state=tk.NORMAL)
        player_x_symbol_menu.config(state=tk.NORMAL)
        player_o_symbol_menu.config(state=tk.NORMAL)
        series_menu.config(state=tk.NORMAL)
        start_button.grid(row=5, column=0, columnspan=4, pady=10)
        root.geometry("600x400")
        enable_all_symbols()  # Re-enable all symbols when resetting the game

    update_score()

def continue_game():
    global current_player, winner
    current_player = "X"
    winner = None
    for row in range(3):
        for col in range(3):
            board[row][col] = ""
            buttons[row][col].config(text="", fg="red")

def create_board():
    global buttons, board, current_player, winner
    buttons = [[None]*3 for _ in range(3)]
    board = [[""]*3 for _ in range(3)]
    current_player = "X"
    winner = None
    for row in range(3):
        for col in range(3):
            buttons[row][col] = tk.Button(root, text="", font=("Arial", 48), width=6, height=3,
                                          command=lambda r=row, c=col: button_click(r, c),
                                          bg="black", fg="red", bd=5)
            buttons[row][col].grid(row=row+4, column=col, sticky="nsew")

    for i in range(3):
        root.grid_rowconfigure(i+4, weight=1)  # Make the board rows expand
        root.grid_columnconfigure(i, weight=1)  # Make the board columns expand

    # Add reset and continue buttons below the board
    reset_button = tk.Button(root, text="Reset Game", command=lambda: reset_game(full_reset=True), bg="black", fg="red", font=("Arial", 16))
    reset_button.grid(row=7, column=0, columnspan=3, pady=10)

    continue_button = tk.Button(root, text="Continue Game", command=continue_game, bg="black", fg="red", font=("Arial", 16))
    continue_button.grid(row=8, column=0, columnspan=3, pady=10)

def on_symbol_change(*args):
    """Callback function to handle symbol selection changes."""
    selected_x_symbol = player_x_symbol.get()
    selected_o_symbol = player_o_symbol.get()

    # Re-enable all options first
    enable_all_symbols()

    # Disable the selected symbol in the other player's menu
    if selected_x_symbol in symbols:
        player_o_symbol_menu["menu"].entryconfig(symbols.index(selected_x_symbol), state="disabled")
    if selected_o_symbol in symbols:
        player_x_symbol_menu["menu"].entryconfig(symbols.index(selected_o_symbol), state="disabled")

def enable_all_symbols():
    """Enable all symbol options for both players."""
    for i in range(len(symbols)):
        player_x_symbol_menu["menu"].entryconfig(i, state="normal")
        player_o_symbol_menu["menu"].entryconfig(i, state="normal")

# Initialize the Tkinter window
root = tk.Tk()
root.title("Tic-Tac-Toe")

# Set the window background to black
root.configure(bg="black")

# Add entry fields for player names with red text and black background
tk.Label(root, text="Player X Name:", bg="black", fg="red", font=("Arial", 12)).grid(row=0, column=0)
player_x_name = tk.Entry(root, bg="black", fg="red", font=("Arial", 12))
player_x_name.grid(row=0, column=1)

tk.Label(root, text="Player O Name:", bg="black", fg="red", font=("Arial", 12)).grid(row=1, column=0)
player_o_name = tk.Entry(root, bg="black", fg="red", font=("Arial", 12))
player_o_name.grid(row=1, column=1)

# Add dropdown menus for symbol selection
symbols = [":)", ":(", "UwU", "OvO"]

tk.Label(root, text="Player X Symbol:", bg="black", fg="red", font=("Arial", 12)).grid(row=0, column=2)
player_x_symbol = tk.StringVar(root)
player_x_symbol.set(symbols[0])  # Default value
player_x_symbol.trace("w", on_symbol_change)  # Trace the variable to call the function on change
player_x_symbol_menu = tk.OptionMenu(root, player_x_symbol, *symbols)
player_x_symbol_menu.grid(row=0, column=3)

tk.Label(root, text="Player O Symbol:", bg="black", fg="red", font=("Arial", 12)).grid(row=1, column=2)
player_o_symbol = tk.StringVar(root)
player_o_symbol.set(symbols[1])  # Default value
player_o_symbol.trace("w", on_symbol_change)  # Trace the variable to call the function on change
player_o_symbol_menu = tk.OptionMenu(root, player_o_symbol, *symbols)
player_o_symbol_menu.grid(row=1, column=3)

# Add dropdown menu for series selection (Best of 3, 5, 7)
tk.Label(root, text="Series Length:", bg="black", fg="red", font=("Arial", 12)).grid(row=2, column=0)
series_choice = tk.StringVar(root)
series_choice.set("3")  # Default value
series_menu = tk.OptionMenu(root, series_choice, "3", "5", "7")
series_menu.grid(row=2, column=1)

# Add score labels
label_score_x = tk.Label(root, text="Player X: 0 (Wins: 0)", bg="black", fg="red", font=("Arial", 12))
label_score_x.grid(row=3, column=0, columnspan=2)

label_score_o = tk.Label(root, text="Player O: 0 (Wins: 0)", bg="black", fg="red", font=("Arial", 12))
label_score_o.grid(row=3, column=2, columnspan=2)

# Add instructions label
instruction_label = tk.Label(root, text="Diagonals only to win a round!!", bg="black", fg="red", font=("Arial", 12))
instruction_label.grid(row=4, column=0, columnspan=4)

# Add start game button, centered
start_button = tk.Button(root, text="Start Game", command=start_game, bg="black", fg="red", font=("Arial", 16))
start_button.grid(row=5, column=0, columnspan=4, pady=10)

# Adjust the window size to better fit the game board
root.geometry("600x450")

root.mainloop()
