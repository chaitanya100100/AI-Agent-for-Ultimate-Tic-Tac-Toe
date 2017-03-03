import sys
import random
import signal
import time
import copy
from operator import itemgetter

class MyPlayer():


    def __init__(self):
        self.deepcopy = copy.deepcopy
        self.hor = [ 5, 6, 7, 8]
        self.ver = [ 9, 10, 11, 12]
        self.dia = [ 13, 14]
        self.my_constants = [ 0, 2, 15, 70, 300 ]
        self.his_constants = [ 0, 2, 15, 70, 300 ]

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

    def print_utility(self, flag, revflag):
        mup = self.my_utility_params
        hup = self.his_utility_params
        mu = self.my_utility
        hu = self.his_utility

        for bi in range(4):
            for bj in range(4):
                print "----------------------"
                print bi, bj
                print "----------------------"
                print "my", flag
                for k in range(15):
                    if k % 4 == 1 and k != 1:
                        print
                    print mup[bi][bj][k],
                print
                print "-------", mu[bi][bj],"----------"
                print "his", revflag
                for k in range(15):
                    if k % 4 == 1 and k != 1:
                        print
                    print hup[bi][bj][k],
                print
                print "-------", hu[bi][bj],"----------"
                print


    def get_available_moves(self):
        self.available_moves = [[[] for j in range(4)] for i in range(4)]
        for i in range(16):
            for j in range(16):
                if self.board_status[i][j] == '-' and self.block_status[i/4][j/4] == '-':
                    self.available_moves[i/4][j/4].append((i,j))
        return

    def init_utility(self, flag, revflag):
        self.my_utility_params_dc = [ [ [ 0 for k in range(15) ] for j in range(4)] for i in range(4)]
        self.his_utility_params_dc = [ [ [ 0 for k in range(15) ] for j in range(4)] for i in range(4)]
        self.my_utility_dc = [ [ 0 for j in range(4) ] for i in range(4)]
        self.his_utility_dc = [ [ 0 for j in range(4) ] for i in range(4)]
        bs = self.deep_copied_board_status
        mup = self.my_utility_params_dc
        hup = self.his_utility_params_dc
        mu = self.my_utility_dc
        hu = self.his_utility_dc

        hor = self.hor
        ver = self.ver
        dia = self.dia
        my_constants = self.my_constants
        his_constants = self.his_constants


        for i in range(4):
            for j in range(4):
                x = 4*i
                y = 4*j
                for a in range(4):
                    for b in range(4):

                        if bs[x+a][y+b] == flag:
                            mup[i][j][hor[a]] += 1
                            mup[i][j][ver[b]] += 1

                            if a == b:
                                mup[i][j][dia[0]] += 1
                            elif a+b == 3:
                                mup[i][j][dia[1]] += 1

                        elif bs[x+a][y+b] == revflag:
                            hup[i][j][hor[a]] += 1
                            hup[i][j][ver[b]] += 1

                            if a == b:
                                hup[i][j][dia[0]] += 1
                            elif a+b == 3:
                                hup[i][j][dia[1]] += 1

                for k in range(5, 15):
                    if not hup[i][j][k]:
                        mup[i][j][ mup[i][j][k] ] += 1
                    if not mup[i][j][k]:
                        hup[i][j][ hup[i][j][k] ] += 1


                mu[i][j] = my_constants[0] * mup[i][j][0] + my_constants[1] * mup[i][j][1] + my_constants[2] * mup[i][j][2] + my_constants[3] * mup[i][j][3] + my_constants[4] * mup[i][j][4]
                hu[i][j] = his_constants[0] * hup[i][j][0] + his_constants[1] * hup[i][j][1] + his_constants[2] * hup[i][j][2] + his_constants[3] * hup[i][j][3] + his_constants[4] * hup[i][j][4]


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


    def update_utility(self, move, flag):
        x = move[0]/4
        y = move[1]/4
        i = move[0]%4
        j = move[1]%4
        hor = self.hor
        ver = self.ver
        dia = self.dia
        if flag == self.my_main_flag:
            mup = self.my_utility_params
            hup = self.his_utility_params
            mu = self.my_utility
            hu = self.his_utility
            my_constants = self.my_constants
            his_constants = self.his_constants
        else:
            hup = self.my_utility_params
            mup = self.his_utility_params
            hu = self.my_utility
            mu = self.his_utility
            his_constants = self.my_constants
            my_constants = self.his_constants

        if not hup[x][y][hor[i]]:
            mu[x][y] += my_constants[mup[x][y][hor[i]] + 1] - my_constants[mup[x][y][hor[i]]]
        if not mup[x][y][hor[i]]:
            hu[x][y] -= his_constants[hup[x][y][hor[i]]]
        mup[x][y][hor[i]] += 1

        if not hup[x][y][ver[j]]:
            mu[x][y] += my_constants[mup[x][y][ver[j]] + 1] - my_constants[mup[x][y][ver[j]]]
        if not mup[x][y][ver[j]]:
            hu[x][y] -= his_constants[hup[x][y][ver[j]]]
        mup[x][y][ver[j]] += 1

        if i==j:
            if not hup[x][y][dia[0]]:
                mu[x][y] += my_constants[mup[x][y][dia[0]] + 1] - my_constants[mup[x][y][dia[0]]]
            if not mup[x][y][dia[0]]:
                hu[x][y] -= his_constants[hup[x][y][dia[0]]]
            mup[x][y][dia[0]] += 1
        elif i+j==3:
            if not hup[x][y][dia[1]]:
                mu[x][y] += my_constants[mup[x][y][dia[1]] + 1] - my_constants[mup[x][y][dia[1]]]
            if not mup[x][y][dia[1]]:
                hu[x][y] -= his_constants[hup[x][y][dia[1]]]
            mup[x][y][dia[1]] += 1


    def get_move(self, old_move, flag):
        allowed_cells = []
        allowed_block = [old_move[0]%4, old_move[1]%4]

        if old_move != (-1,-1) and self.block_status[allowed_block[0]][allowed_block[1]] == '-':
            allowed_cells.extend(self.available_moves[allowed_block[0]][allowed_block[1]])
        else:
            for i in range(4):
                for j in range(4):
                    allowed_cells.extend(self.available_moves[i][j])


        # choose according to utility
        #---------------------------------------

        utility_arr = [(0, 0) for i in xrange(len(allowed_cells))]
        hor = self.hor
        ver = self.ver
        dia = self.dia

        if flag == self.my_main_flag:
            mup = self.my_utility_params
            hup = self.his_utility_params
            mu = self.my_utility
            hu = self.his_utility
            my_constants = self.my_constants
            his_constants = self.his_constants
        else:
            hup = self.my_utility_params
            mup = self.his_utility_params
            hu = self.my_utility
            mu = self.his_utility
            his_constants = self.my_constants
            my_constants = self.his_constants

        count = 0
        total = 0
        mi = 1000000000
        for i, j in allowed_cells:
            x = i/4
            y = j/4
            i = i%4
            j = j%4
            my_ut = mu[x][y]
            his_ut = hu[x][y]

            if not hup[x][y][hor[i]]:
                my_ut += my_constants[mup[x][y][hor[i]] + 1] - my_constants[mup[x][y][hor[i]]]
            if not hup[x][y][ver[j]]:
                my_ut += my_constants[mup[x][y][ver[j]] + 1] - my_constants[mup[x][y][ver[j]]]

            if not mup[x][y][hor[i]]:
                his_ut -= his_constants[hup[x][y][hor[i]]]
            if not mup[x][y][ver[j]]:
                his_ut -= his_constants[hup[x][y][ver[j]]]

            if i==j:
                if not hup[x][y][dia[0]]:
                    my_ut += my_constants[mup[x][y][dia[0]] + 1] - my_constants[mup[x][y][dia[0]]]
                if not mup[x][y][dia[0]]:
                    his_ut -= his_constants[hup[x][y][dia[0]]]
            if i+j==3:
                if not hup[x][y][dia[1]]:
                    my_ut += my_constants[mup[x][y][dia[1]] + 1] - my_constants[mup[x][y][dia[1]]]
                if not mup[x][y][dia[1]]:
                    his_ut -= his_constants[hup[x][y][dia[1]]]

            if self.block_status[i][j] != '-':
                his_max = -1000000
                for p in range(4):
                    for q in range(4):
                        if hu[p][q]> his_max:
                            his_max = hu[p][q]
                final_ut = 30*(my_ut - mu[x][y]) + 30*(hu[x][y] - his_ut) - 2*his_max
            else:
                final_ut = 30*(my_ut - mu[x][y]) + 30*(hu[x][y] - his_ut) - 2*hu[i][j]

            if final_ut < mi:
                mi = final_ut
            utility_arr[count] = (final_ut, count)
            total += final_ut
            count += 1

        le = len(allowed_cells)
        rand_number = random.randint(0, total - mi*le)
        total = 0
        count = 0
	utility_arr = sorted(utility_arr, reverse=True)	
	maxi7 = 0.5*utility_arr[0][0]
        for u in utility_arr:
	    if u[0] < maxi7:
		break
	    count+=1
        #---------------------------------------
        if count >= le:
            count = le - 1
        return allowed_cells[utility_arr[random.randint(0,count)][1]]


    def play_move(self, new_move, ply):
        self.board_status[new_move[0]][new_move[1]] = ply
        self.update_utility(new_move, ply)
        x = new_move[0]/4
        y = new_move[1]/4
        x4 = 4*x
        y4 = 4*y
        self.available_moves[x][y].remove((new_move[0], new_move[1]))
        bs = self.board_status

        for i in xrange(4):
    	    if (bs[x4+i][y4] == bs[x4+i][y4+1] == bs[x4+i][y4+2] == bs[x4+i][y4+3] == ply):
                self.block_status[x][y] = ply
                del self.available_moves[x][y][:]
                return
            if (bs[x4][y4+i] == bs[x4+1][y4+i] == bs[x4+2][y4+i] == bs[x4+3][y4+i] == ply):
                self.block_status[x][y] = ply
                del self.available_moves[x][y][:]
                return

        if (bs[x4][y4] == bs[x4+1][y4+1] == bs[x4+2][y4+2] == bs[x4+3][y4+3] == ply):
            self.block_status[x][y] = ply
            del self.available_moves[x][y][:]
            return
        if (bs[x4+3][y4] == bs[x4+2][y4+1] == bs[x4+1][y4+2] == bs[x4][y4+3] == ply):
            self.block_status[x][y] = ply
            del self.available_moves[x][y][:]
            return

        for i in xrange(4):
            for j in xrange(4):
                if bs[x4+i][y4+j] =='-':
			        return
        self.block_status[x][y] = 'd'
        del self.available_moves[x][y][:]
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
        if flag == 'o':
            revflag = 'x'
        else :
            revflag = 'o'

        # play first move and check for termination
        #---------------------------------------
        self.play_move(cell, flag)
        if self.block_status[X][Y] == flag:
            cb = self.check_big()
            if cb != '-':
                return cb
        elif self.block_status[X][Y] == 'd':
            cb = self.check_big()
            if cb == 'd':
                return cb
        #---------------------------------------


        # main game loop
        #---------------------------------------
        while 1:
            # decide loop's first play
            #---------------------------------------
            now_move = self.get_move((x, y), revflag)
            X = now_move[0]/4
            Y = now_move[1]/4
            x = now_move[0]%4
            y = now_move[1]%4
            #---------------------------------------

            # play loop's first play
            #---------------------------------------
            self.play_move([4*X+x, 4*Y+y], revflag)
            if self.block_status[X][Y] == revflag:
                cb = self.check_big()
                if cb != '-':
                    return cb
            elif self.block_status[X][Y] == 'd':
                cb = self.check_big()
                if cb == 'd':
                    return cb
            #---------------------------------------

            # decide loop's second play
            #---------------------------------------
            now_move = self.get_move((x, y), flag)
            X = now_move[0]/4
            Y = now_move[1]/4
            x = now_move[0]%4
            y = now_move[1]%4
            #---------------------------------------

            # play loop's second play
            #---------------------------------------
            self.play_move([4*X+x, 4*Y+y], flag)
            if self.block_status[X][Y] == flag:
                cb = self.check_big()
                if cb != '-':
                    return cb
            elif self.block_status[X][Y] == 'd':
                cb = self.check_big()
                if cb == 'd':
                    return cb
            #---------------------------------------

    def move(self, board, old_move, flag):

        cells = board.find_valid_move_cells(old_move)
        self.my_main_flag = flag
        time_per_cell = 1000000 * 13.5 / len(cells)
        wins = 0
        loses = 0
        ties = 0
        start_time = 0
        current_time = 0
        res = 0
        if flag == 'o':
            revflag = 'x'
        else:
            revflag = 'o'

        self.deep_copied_board_status = self.deepcopy(board.board_status)
        self.deep_copied_block_status = self.deepcopy(board.block_status)

        self.init_utility(flag, revflag)
        # self.print_utility(flag, revflag)

        best_prob = -0.01
        best_cell = None

        for cell in cells:
            wins = 0
            loses = 0
            ties = 0

            start_time = time.time()*1000000

            while time.time()*1000000 - start_time < time_per_cell:

                self.board_status = self.deepcopy(self.deep_copied_board_status)
                self.block_status = self.deepcopy(self.deep_copied_block_status)
                self.my_utility = self.deepcopy(self.my_utility_dc)
                self.his_utility = self.deepcopy(self.his_utility_dc)
                self.my_utility_params = self.deepcopy(self.my_utility_params_dc)
                self.his_utility_params = self.deepcopy(self.his_utility_params_dc)

                self.get_available_moves()
                res = self.play_a_game(cell, flag)
                if res == flag:
                    wins += 1
                elif res == revflag:
                    loses += 1
                elif res == 'd':
                    ties += 1
                else:
                    raise "kaik problem chhe"
            tot = wins + ties + loses
            prob = (1.0*wins) / tot + (1.0*loses*ties) / (tot*tot)

            if prob > best_prob:
                best_prob = prob
                best_cell = cell
            #print cell, prob, best_cell, best_prob
            print wins, loses, ties, wins+loses+ties
        print best_prob, best_cell
        return best_cell
