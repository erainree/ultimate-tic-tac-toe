# Ultimate Tic Tac Toe - Clean Version with Countdown Timer, On-Screen Turn Loss Notice, and Instructions

import tkinter as tk
from tkinter import messagebox
import random

class UltimateTicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Tic Tac Toe")
        self.canvas = tk.Canvas(self.root, width=600, height=750, highlightthickness=0, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.timer_label = None
        self.timer_seconds = 15
        self.timer_id = None
        self.timer_started = False
        self.game_over = False
        self.allow_move = True

        self.current_player = "𖤓"
        self.next_board = None
        self.boards = [[None] * 9 for _ in range(9)]
        self.board_winners = [None] * 9
        self.turn_lost_msg = None

        self.show_instructions()

    def show_instructions(self):
        self.canvas.create_rectangle(50, 100, 550, 650, fill="#f0f0f0", outline="black", width=2, tags="instructions")
        instructions = (
            "Welcome to Ultimate Tic Tac Toe!\n\n"
            "Rules:\n"
            "- Each small board is a regular 3x3 Tic Tac Toe.\n"
            "- Win a small board to claim it.\n"
            "- Win 3 boards in a row to win the game.\n"
            "- You must play in the board matching your opponent’s last move.\n"
            "- If the board is won or tied, you can play anywhere.\n"
            "- You have 15 seconds per turn.\n"
            "- If you don’t move in time, you lose your turn!\n"
        )
        self.canvas.create_text(300, 250, text=instructions, font=("Arial", 12), fill="black", justify="center", tags="instructions")
        self.canvas.create_rectangle(250, 600, 350, 640, fill="#222222", outline="white", width=2, tags=("instructions", "start_button"))
        self.canvas.create_text(300, 620, text="Start Game", font=("Arial", 12), fill="white", tags=("instructions", "start_button"))
        self.canvas.tag_bind("start_button", "<Button-1>", lambda e: self.start_game())

    def start_game(self):
        self.canvas.delete("instructions")
        self.draw_static_ui()
        self.draw_board()

    def draw_static_ui(self):
        self.restart_btn_rect = self.canvas.create_rectangle(240, 670, 360, 700, fill="#222222", outline="white", width=2, tags="restart")
        self.restart_btn_text = self.canvas.create_text(300, 685, text="Restart Game", font=("Arial", 12), fill="white", tags="restart")
        self.canvas.tag_bind("restart", "<Button-1>", lambda e: self.restart_game())

        self.turn_text = self.canvas.create_text(300, 720, text=f"Player Turn: {self.current_player}", font=("Arial", 14), fill="black")
        self.timer_label = self.canvas.create_text(300, 705, text="15", font=("Arial", 14, "bold"), fill="red")

    def draw_board(self):
        self.cells = {}
        self.board_rects = {}
        for board in range(9):
            top_x = (board % 3) * 200
            top_y = (board // 3) * 200
            board_bg = self.canvas.create_rectangle(top_x, top_y, top_x + 200, top_y + 200, fill="white", outline="black")
            self.board_rects[board] = board_bg
            for cell in range(9):
                x = top_x + (cell % 3) * 60 + 10
                y = top_y + (cell // 3) * 60 + 10
                rect = self.canvas.create_rectangle(x, y, x + 50, y + 50, fill="#ffffff", outline="#333333", tags=f"cell_{board}_{cell}")
                text = self.canvas.create_text(x + 25, y + 25, text="", font=("Arial", 24), fill="black", tags=f"cell_{board}_{cell}")
                self.canvas.tag_raise(text)
                self.cells[(board, cell)] = (rect, text)
                self.canvas.tag_bind(f"cell_{board}_{cell}", '<Button-1>', lambda e, b=board, c=cell: self.make_move(b, c))
        self.highlight_active_board()

    def highlight_active_board(self):
        for board in range(9):
            if self.board_winners[board] is not None:
                self.canvas.itemconfig(self.board_rects[board], fill="white")
            elif self.next_board is None or self.next_board == board:
                self.canvas.itemconfig(self.board_rects[board], fill="#bbdefb")
            else:
                self.canvas.itemconfig(self.board_rects[board], fill="#ffcdd2")

    def make_move(self, board, cell):
        if self.game_over or not self.allow_move:
            return
        if self.next_board is not None and board != self.next_board:
            return
        if self.board_winners[board] is not None:
            return
        if self.boards[board][cell] is not None:
            return

        if not self.timer_started:
            self.start_timer()
            self.timer_started = True

        self.boards[board][cell] = self.current_player
        _, text = self.cells[(board, cell)]
        self.canvas.itemconfig(text, text=self.current_player)

        winner = self.check_win(self.boards[board])
        if winner:
            self.board_winners[board] = winner
            for cell_idx in range(9):
                self.canvas.delete(f"cell_{board}_{cell_idx}")
            self.canvas.create_text((board % 3) * 200 + 100, (board // 3) * 200 + 100, text=winner,
                                    font=("Arial", 48, "bold"), fill="orange")

        self.next_board = cell if self.board_winners[cell] is None else None
        self.highlight_active_board()
        overall_winner = self.check_win(self.board_winners)
        if overall_winner:
            self.game_over = True
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
            messagebox.showinfo("Game Over", f"{overall_winner} wins the game!")
            return

        self.current_player = "⏾" if self.current_player == "𖤓" else "𖤓"
        self.canvas.itemconfig(self.turn_text, text=f"Player Turn: {self.current_player}")

        self.start_timer()

    def get_board_status(self, board):
        counts = {"𖤓": 0, "⏾": 0}
        for mark in self.boards[board]:
            if mark in counts:
                counts[mark] += 1
        if counts["𖤓"] > counts["⏾"]:
            return "𖤓 likely"
        elif counts["⏾"] > counts["𖤓"]:
            return "⏾ likely"
        else:
            return "Even"

    def check_win(self, cells):
        wins = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for a, b, c in wins:
            if cells[a] == cells[b] == cells[c] and cells[a] is not None:
                return cells[a]
        return None

    def start_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.allow_move = True
        self.timer_seconds = 15
        self.update_timer()

    def update_timer(self):
        self.canvas.itemconfig(self.timer_label, text=str(self.timer_seconds))
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.canvas.itemconfig(self.timer_label, text="0")
            self.allow_move = False
            self.show_turn_loss_screen()

    def show_turn_loss_screen(self):
        emoji = self.current_player
        message = f"{emoji} lost their turn!"
        self.turn_lost_msg = self.canvas.create_text(300, 740, text=message, font=("Arial", 12, "bold"), fill="red")
        self.root.after(5000, self.clear_turn_loss_and_continue)

    def clear_turn_loss_and_continue(self):
        if self.turn_lost_msg:
            self.canvas.delete(self.turn_lost_msg)
        self.current_player = "⏾" if self.current_player == "𖤓" else "𖤓"
        self.canvas.itemconfig(self.turn_text, text=f"Player Turn: {self.current_player}")
        self.start_timer()

    def restart_game(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.canvas.delete("all")
        self.current_player = "𖤓"
        self.next_board = None
        self.boards = [[None] * 9 for _ in range(9)]
        self.board_winners = [None] * 9
        self.game_over = False
        self.allow_move = True
        self.timer_started = False
        self.turn_lost_msg = None
        self.draw_static_ui()
        self.draw_board()
        self.canvas.itemconfig(self.timer_label, text="15")

if __name__ == "__main__":
    root = tk.Tk()
    game = UltimateTicTacToe(root)
    root.mainloop()
