import sys
import random
import signal
import time
import copy

class MyPlayer():


    def __init__(self):
        self.deepcopy = copy.deepcopy
        pass

    def get_revflag(self, flag):
        if flag=='o':
            return 'x'
        else:
            return 'o'

    def print_board(self):
		# for printing the state of the board
		print '==============Board State=============='
		for i in range(16):
			if i%4 == 0:
				print
			for j in range(16):
				if j%4 == 0:
					print "",
				print self.board_status[i][j],
			print
		print

		print '==============Block State=============='
		for i in range(4):
			for j in range(4):
				print self.block_status[i][j],
			print
		print '======================================='
		print
		print

    """
    def check(self, board_status, block_status, X, Y):
        small_result = big_result = '-'
        for i in xrange(4):
			if (board_status[4*X+i][4*Y] == board_status[4*X+i][4*Y+1] == board_status[4*X+i][4*Y+2] == board_status[4*X+i][4*Y+3]):
                small_result = block_status[X][Y] = board_status[4*X+i][4*Y]
                break
			if (board_status[4*X][4*Y+i] == board_status[4*X+1][4*Y+i] == board_status[4*X+2][4*Y+i] == board_status[4*X+3][4*Y+i]):
				small_result = block_status[X][Y] = board_status[4*X][4*Y+i]
                break

		if small_result=='-' and (board_status[4*X][4*Y] == board_status[4*X+1][4*Y+1] == board_status[4*X+2][4*Y+2] == board_status[4*X+3][4*Y+3]):
            small_result = block_status[X][Y] = board_status[4*X][4*Y]

		if small_result=='-' and (board_status[4*X+3][4*Y] == board_status[4*X+2][4*Y+1] == board_status[4*X+1][4*Y+2] == board_status[4*X][4*Y+3]):
			small_result = block_status[X][Y] = board_status[4*X+3][4*Y]

        for i in xrange(4):
			for j in xrange(4):
				if board_status[4*X+i][4*Y+j] =='-':
                    return small_result, '-'
        block_status[X][Y] = 'd'
        return small_result, 'd'
    """

    def find_valid_move_cells(self, old_move):
        allowed_cells = []
        allowed_block = [old_move[0]%4, old_move[1]%4]

        if old_move != (-1,-1) and self.block_status[allowed_block[0]][allowed_block[1]] == '-':
            for i in range(4*allowed_block[0], 4*allowed_block[0]+4):
                for j in range(4*allowed_block[1], 4*allowed_block[1]+4):
                    if self.board_status[i][j] == '-':
                        allowed_cells.append((i,j))
        else:
            for i in range(16):
                for j in range(16):
                    if self.board_status[i][j] == '-' and self.block_status[i/4][j/4] == '-':
                        allowed_cells.append((i,j))
        return allowed_cells

    def get_move(self, old_move):
        cells = self.find_valid_move_cells(old_move)
        return cells[random.randint(0, len(cells)-1)]

    def play_move(self, new_move, ply):
        self.board_status[new_move[0]][new_move[1]] = ply
        x = new_move[0]/4
        y = new_move[1]/4
        bs = self.board_status

        for i in xrange(4):
    	    if (bs[4*x+i][4*y] == bs[4*x+i][4*y+1] == bs[4*x+i][4*y+2] == bs[4*x+i][4*y+3]) and (bs[4*x+i][4*y] == ply):
		        self.block_status[x][y] = ply
		        return
            if (bs[4*x][4*y+i] == bs[4*x+1][4*y+i] == bs[4*x+2][4*y+i] == bs[4*x+3][4*y+i]) and (bs[4*x][4*y+i] == ply):
                self.block_status[x][y] = ply
                return

            if (bs[4*x][4*y] == bs[4*x+1][4*y+1] == bs[4*x+2][4*y+2] == bs[4*x+3][4*y+3]) and (bs[4*x][4*y] == ply):
                self.block_status[x][y] = ply
                return
            if (bs[4*x+3][4*y] == bs[4*x+2][4*y+1] == bs[4*x+1][4*y+2] == bs[4*x][4*y+3]) and (bs[4*x+3][4*y] == ply):
                self.block_status[x][y] = ply
                return

        for i in xrange(4):
            for j in xrange(4):
                if bs[4*x+i][4*y+j] =='-':
			    return
        self.block_status[x][y] = 'd'
        return

    def check_big(self):

        bs = self.block_status
    	for i in xrange(4):
            if (bs[i][0] == bs[i][1] == bs[i][2] == bs[i][3]):
                return bs[i][0]
            if (bs[0][i] == bs[1][i] == bs[2][i] == bs[3][i]):
                return bs[0][i]

        if (bs[0][0] == bs[1][1] == bs[2][2] == bs[3][3]):
            return bs[0][0]
        if (bs[3][0] == bs[2][1] == bs[1][2] == bs[0][3]):
            return bs[3][0]

        for i in xrange(4):
            for j in xrange(4):
                if bs[i][j] == '-':
                    return '-'
        return 'd'


    def play_a_game(self, cell, flag):

        X = cell[0]/4
        Y = cell[1]/4
        x = cell[0]%4
        y = cell[1]%4
        revflag = self.get_revflag(flag)

        # play first move and check for termination
        #---------------------------------------
        self.play_move(cell, flag)
        cb = self.check_big()
        if self.block_status[X][Y] == flag:
            if cb != '-':
                return cb
        elif self.block_status[X][Y] == 'd':
            if cb == 'd':
                return cb
        #---------------------------------------


        """
        # decide loop's first move-block after first move
        #---------------------------------------
        if self.block_status[x][y] != '-':
            X = -1
            Y = -1
        else :
            X = x
            Y = y
        #---------------------------------------
        """


        # main game loop
        #---------------------------------------
        while True:
            """
            # randomly decide loop's first play
            #---------------------------------------
            if X == -1 and Y == -1:
                X = random.randint(0,3)
                Y = random.randint(0,3)
                while self.block_status[X][Y] != '-':
                    X = random.randint(0,3)
                    Y = random.randint(0,3)

            x = random.randint(0,3)
            y = random.randint(0,3)
            while self.board_status[4*X+x][4*Y+y] != '-':
                x = random.randint(0,3)
                y = random.randint(0,3)
            #---------------------------------------
            """
            now_move = self.get_move((x, y))
            X = now_move[0]/4
            Y = now_move[1]/4
            x = now_move[0]%4
            y = now_move[1]%4

            # play loop's first play
            #---------------------------------------
            self.play_move([4*X+x, 4*Y+y], revflag)
            cb = self.check_big()
            if self.block_status[X][Y] == revflag:
                if cb != '-':
                    return cb
            elif self.block_status[X][Y] == 'd':
                if cb == 'd':
                    return cb
            #---------------------------------------

            """
            # decide loop's second move-block
            #---------------------------------------
            if self.block_status[x][y] != '-':
                X = -1
                Y = -1
            else :
                X = x
                Y = y
            #---------------------------------------



            # randomly decide loop's second play
            #---------------------------------------
            if X == -1 and Y == -1:
                X = random.randint(0,3)
                Y = random.randint(0,3)
                while self.block_status[X][Y] != '-':
                    X = random.randint(0,3)
                    Y = random.randint(0,3)
            x = random.randint(0,3)
            y = random.randint(0,3)

            while self.board_status[4*X+x][4*Y+y] != '-':
                x = random.randint(0,3)
                y = random.randint(0,3)
            #---------------------------------------
            """
            now_move = self.get_move((x, y))
            X = now_move[0]/4
            Y = now_move[1]/4
            x = now_move[0]%4
            y = now_move[1]%4

            # play loop's second play
            #---------------------------------------
            self.play_move([4*X+x, 4*Y+y], flag)
            cb = self.check_big()
            if self.block_status[X][Y] == flag:
                if cb != '-':
                    return cb
            elif self.block_status[X][Y] == 'd':
                if cb == 'd':
                    return cb
            #---------------------------------------

            """
            # decide loop's first move-block after first move
            #---------------------------------------
            if self.block_status[x][y] != '-':
                X = -1
                Y = -1
            else :
                X = x
                Y = y
            #---------------------------------------
            """

    def move(self, board, old_move, flag):

        cells = board.find_valid_move_cells(old_move)
        time_per_cell = 1000000 * 13.5 / len(cells)
        wins = 0
        loses = 0
        ties = 0
        start_time = 0
        current_time = 0
        res = 0
        revflag = self.get_revflag(flag)

        self.deep_copied_board_status = copy.deepcopy(board.board_status)
        self.deep_copied_block_status = copy.deepcopy(board.block_status)

        best_prob = 0.0
        best_cell = None

        for cell in cells:
            wins = 0
            loses = 0
            ties = 0

            start_time = time.time()*1000000

            while time.time()*1000000 - start_time < time_per_cell:

                self.board_status = self.deepcopy(board.board_status)
                self.block_status = self.deepcopy(board.block_status)
                res = self.play_a_game(cell, flag)
                if res == flag:
                    wins += 1
                elif res == revflag:
                    loses += 1
                elif res == 'd':
                    ties += 1
                else:
                    raise "kaik problem chhe"

            prob = 1.0*wins / (wins+loses+ties)

            if prob > best_prob:
                best_prob = prob
                best_cell = cell
            #print cell, prob, best_cell, best_prob
            print wins, loses, ties
        print best_prob, best_cell
        return best_cell
