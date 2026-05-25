import numpy as np
from time import time

class Gomoku:

    def __init__(self, depth, overline = False):
        self.n_rows = 15
        self.n_cols = self.n_rows
        self.winning_length = 5     # hardcoded
        self.depth = depth
        self.all_games = []
        self.artificial_moves = []
        self.game = False
        self.overline = overline
        self.max_time = 0
        patterns = {
            # Player
            # 4 in a row
            '-pppp-': 100000,
            '-p-ppp-': 100000,
            '-pp-pp-': 100000,
            '-ppp-p-': 100000,

            'pppp-': 10000,
            '-pppp': 10000,
            'p-ppp': 10000,
            'pp-pp': 10000,
            'ppp-p': 10000,
            
            # 3 in a row
            '--ppp--': 5000,
            '--p-pp--': 5000,
            '--pp-p--': 5000,

            '-ppp-': 3000,
            '-p-pp-': 3000,
            '-pp-p-': 3000,
            '-p--pp-': 3000,

            '--ppp': 800,
            'pp--p': 800,
            'p--pp': 800,
            'p-p-p': 800,

            # 2 in a row
            '--pp--': 200,
            '--p-p--': 200,
            
            '-pp-': 100,
            '-p-p-': 100,
            '-p--p-': 100,

            # Player
            # 4 in a row
            '-oooo-': -500000,
            '-o-ooo-': -500000,
            '-oo-oo-': -500000,
            '-ooo-o-': -500000,

            'oooo-': -20000,
            '-oooo': -20000,
            'o-ooo': -20000,
            'oo-oo': -20000,
            'ooo-o': -20000,

            # 3 in a row
            '--ooo--': -6500,
            '--o-oo--': -6500,
            '--oo-o--': -6500,

            '-ooo-': -2000,
            '-o-oo-': -2000,
            '-oo-o-': -2000,
            '-o--oo-': -2000,

            '--ooo': -20,
            'oo--o': -20,
            'o--oo': -20,
            'o-o-o': -20
        }
        if overline:
            for i in range(6, max(self.n_rows, self.n_cols)+1):
                patterns['p'*i] = -50
        self.sorted_patterns = sorted(patterns.items(), key=lambda item: (len(item[0]), abs(item[1])), reverse=True)
        
        center_y = (self.n_rows-1)/2
        center_x = (self.n_cols-1)/2
        manhattan_distance = np.zeros((self.n_rows, self.n_cols))
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                manhattan_distance[i, j] = 1/(abs(i-center_y)+abs(j-center_x)+1)
        self.manhattan_distance = manhattan_distance

        self.positions = set()
        if self.n_rows % 2 == 0:
            y_shift = 0
        else:
            y_shift = 1
        if self.n_cols % 2 == 0:
            x_shift = 0
        else:
            x_shift = 1
        
        for i in range(-2-y_shift, 3):
            for j in range(-2-x_shift, 3):
                self.positions.add((i, j))
    
    def new_game(self):
        self.board = np.ones((self.n_rows, self.n_cols))*-9
        self.game_history = []
        self.game_version = 0
        while self.game_version != 1 and self.game_version != 2 and self.game_version != 3:
            self.game_version = int(input("Choose the type of game (1 - player vs player, 2 - AI vs AI, 3 - player vs AI): "))
        print("0's start the game")
        if self.game_version == 1:
            self.turns = ["P", "P"]
        elif self.game_version == 2:
            self.turns = ["AI", "AI"]
        else:
            who_starts = 0
            while who_starts != 1 and who_starts != 2:
                who_starts = int(input("Choose who starts the game (1 - the player, 2 - AI): "))
            if who_starts == 1: self.turns = ["P", "AI"]
            else: self.turns = ["AI", "P"]
        self.player = 0
        self.game = True
        self.play()

    def print_board(self):
        dashes = 6*self.n_rows+4
        board = self.board
        cols = "   |"
        for j in range(self.n_cols):
            if j+1>9:
                cols += f"  {j+1} |"
            else:
                cols += f"  {j+1}  |"
        print(cols)
        print("-"*(dashes))
        for i in range(self.n_rows):
            string = f"{i+1}  |"
            if i+1>9:
                string = f"{i+1} |"
            else:
                string = f"{i+1}  |"
            for j in range(self.n_cols):
                value = board[i, j]
                if value == 0: string += "  0  |"
                elif value == 1: string += "  1  |"
                else: string += "     |"
            print(string)
            print("-"*(dashes))

    def cell(self, row, col):
        if 0 <= row < self.n_rows and 0 <= col < self.n_cols:
            return self.board[int(row), int(col)]
        return -22

    def play(self):
        start = time()
        rows = self.n_rows
        cols = self.n_cols
        turn = 0
        while self.game:
            turn += 1
            if self.turns[self.player] == "P":
                print(f"Turn {turn}, player's ({self.player}) move")
                row = -1
                col = -1
                while self.cell(row, col) != -9:
                    row = int(input(f"Choose row number (1-{rows}): "))-1
                    col = int(input(f"Choose column number (1-{cols}): "))-1
            else:
                print(f"Turn {turn}, AI's ({self.player}) move")
                move = self.ai_move()
                row = move[0]
                col = move[1]

            self.board[row, col] = self.player
            self.game_history.append((row, col))
            self.print_board()
            
            if self.win(self.player, (row, col)):
                end = time()
                self.game = False
                self.game_history.append(self.player)
                self.all_games.append(self.game_history)
                if self.turns[self.player] == "P":
                    print(f"Player {self.player} won!")
                else:
                    print(f"AI {self.player} won!")
                if self.turns == ["AI", "AI"]:
                    print(f"Maximum time to make a move: {self.max_time:.3f} seconds")
                print(f"Time of the game: {end-start:.3f} seconds")

            if (self.board != -9).all():
                end = time()
                self.game = False
                self.game_history.append(self.player)
                self.all_games.append(self.game_history)
                print(f"It's a tie!")
                if self.turns == ["AI", "AI"]:
                    print(f"Maximum time to make a move: {self.max_time:.3f} seconds")
                print(f"Time of the game: {end-start:.3f} seconds")
            
            self.player = 1 - self.player

    def win(self, player, position):
        row, col = position
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            i = row + dr
            j = col + dc
            while 0 <= i < self.n_rows and 0 <= j < self.n_cols and self.board[i, j] == player:
                count += 1
                i += dr
                j += dc
            i = row - dr
            j = col - dc
            while 0 <= i < self.n_rows and 0 <= j < self.n_cols and self.board[i, j] == player:
                count += 1
                i -= dr
                j -= dc
            if self.overline:
                if count == 5:
                    return True
            else:
                if count >= 5:
                    return True
        return False

    def best_positions(self):
        if (self.board == -9).all():
            return [(self.n_rows//2, self.n_cols//2)]
        occupied = np.argwhere(self.board != -9)
        positions = {}
        for position in self.positions:
            row, col = position
            if self.board[row, col] == -9:
                positions[position] = self.manhattan_distance[row, col]
        for i, j in occupied:
            for r in range(i-2, i+3):
                for c in range(j-2, j+3):
                    if self.cell(r, c) == -9:
                        positions[(r, c)] = positions.get((r, c), self.manhattan_distance[r, c]) + 1
        positions = sorted(positions.items(), key=lambda item: item[1], reverse=True)
        return [move[0] for move in positions]

    @staticmethod
    def diagonal_as_string(board, rows, cols, r, c, dr, dc, char):
        line = ""
        while 0 <= r < rows and 0 <= c < cols:
            line += char[board[r, c]]
            r += dr
            c += dc
        return(line)
    
    def lines_as_string(self):
        lines = []
        rows = self.n_rows
        cols = self.n_cols
        player = self.player
        opponent = 1-player
        board = self.board
        char = {
            player: "p",
            opponent: "o",
            -9: "-"
        }

        # Rows
        for r in range(rows):
            line = "".join([char[board[r, c]] for c in range(cols)])
            lines.append(line)

        # Columns
        for c in range(cols):
            line = "".join([char[board[r, c]] for r in range(rows)])
            lines.append(line)

        # Diagonal (left-top to right-bottom)
        # Rows
        for r in range(rows):
            line = self.diagonal_as_string(board, rows, cols, r, 0, 1, 1, char)
            if len(line) >= 5:
                lines.append(line)
        # Columns
        for c in range(1, cols):
            line = self.diagonal_as_string(board, rows, cols, 0, c, 1, 1, char)
            if len(line) >= 5:
                lines.append(line)
        
        # Diagonal (right-top to left-bottom)
        board_flipped = np.flip(board, 1)
        # Rows
        # Rows
        for r in range(rows):
            line = self.diagonal_as_string(board_flipped, rows, cols, r, 0, 1, 1, char)
            if len(line) >= 5:
                lines.append(line)
        # Columns
        for c in range(1, cols):
            line = self.diagonal_as_string(board_flipped, rows, cols, 0, c, 1, 1, char)
            if len(line) >= 5:
                lines.append(line)

        return lines

    def evaluate_board(self):
        lines = self.lines_as_string()
        score = 0
        for line in lines:
            temp_line = line
            for pattern, value in self.sorted_patterns:
                while pattern in temp_line:
                    score += value
                    mask = pattern.replace("p", ".").replace("o", ".")
                    temp_line = temp_line.replace(pattern, mask, 1)
        return score

    def minimax(self, depth, position, alpha, beta, maximizingPlayer):
        if maximizingPlayer:
            last_player = 1-self.player
        else:
            last_player = self.player
        if self.win(last_player, position):
            if last_player == self.player:
                return 1e7 + depth
            else:
                return -1e7
        
        if depth == 0:
            return self.evaluate_board()
        
        best_positions = self.best_positions()

        if maximizingPlayer:
            maxEval = -np.inf
            for position in best_positions:
                self.board[position[0], position[1]] = self.player
                eval = self.minimax(depth - 1, position, alpha, beta, False)
                self.board[position[0], position[1]] = -9
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return(maxEval)

        else:
            minEval = np.inf
            for position in best_positions:
                self.board[position[0], position[1]] = 1-self.player
                eval = self.minimax(depth - 1, position, alpha, beta, True)
                self.board[position[0], position[1]] = -9
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return(minEval)

    def ai_move(self):
        best_positions = self.best_positions()
        best_score = -np.inf
        best_move = None
        alpha = -np.inf
        start = time()
        player = self.player
        for position in best_positions:
            row, col = position
            self.board[row, col] = player
            score = self.minimax(self.depth-1, position, alpha, np.inf, False)
            if best_score < score:
                best_move = position
                best_score = score
            alpha = max(alpha, best_score)
            self.board[row, col] = -9
        best_move1 = (best_move[0]+1, best_move[1]+1)
        end = time()
        current_time = end-start
        self.max_time = max(self.max_time, current_time)
        print(f"AI {player} chose coordinates {best_move1} with a score of {best_score}. Time: {current_time:.3f} seconds")
        return(best_move)

game = Gomoku(depth = 3)
game.new_game()