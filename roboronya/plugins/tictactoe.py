description = "Play Tic Tac Toe with Roboronya, beware of her skills. Check */tictactoe help* for more info."

from roboronya.plugins.plugin import *

class TicTacToe(object):
    
    board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
    player = 'o'
    cpu = 'x'
    
    cpuWins = 0
    peasantsWins = 0
    draws = 0

    def put(x, y):
        if TicTacToe.board[(y*3) + x] == ' ':
            TicTacToe.board[(y*3) + x] = TicTacToe.player
            a, pos = TicTacToe.nextMove(TicTacToe.board, TicTacToe.player)
            if a != 0:
                TicTacToe.board[pos] = TicTacToe.cpu
            return True
        else:
            return False

    def start():
        if all(x == ' ' for x in TicTacToe.board):
            pos = random.randint(0,8)
            TicTacToe.board[pos] = TicTacToe.cpu
            return True
        else:
            return False
        
    def get(x, y):
        char = TicTacToe.board[(y*3) + x]
        return char
    
    def isDraw():
        win, player = TicTacToe.isWin(TicTacToe.board)
        if all((x == TicTacToe.cpu or x == TicTacToe.player) for x in TicTacToe.board) and not win:
            return True
        else:
            return False

    def isWin(board):
        ### check if any of the rows has winning combination
        for i in range(3):
            if len(set(TicTacToe.board[i*3:i*3+3])) is  1 and TicTacToe.board[i*3] is not ' ':
                winner = TicTacToe.board[i*3]
                return True, winner
        
        ### check if any of the Columns has winning combination
        for i in range(3):
            if (TicTacToe.board[i] is TicTacToe.board[i+3]) and (TicTacToe.board[i] is  TicTacToe.board[i+6]) and TicTacToe.board[i] is not ' ':
                winner = TicTacToe.board[i]
                return True, winner

        ### 2,4,6 and 0,4,8 cases
        if TicTacToe.board[0] is TicTacToe.board[4] and TicTacToe.board[4] is TicTacToe.board[8] and TicTacToe.board[4] is not ' ':
            winner = TicTacToe.board[4]
            return  True, winner
            
        if TicTacToe.board[2] is TicTacToe.board[4] and TicTacToe.board[4] is TicTacToe.board[6] and TicTacToe.board[4] is not ' ':
            winner = TicTacToe.board[4]
            return  True, winner
            
        return False, None
        
        
    def nextMove(board, player):
        
        if len(set(board)) == 1:
            return 0,4
        
        nextplayer = TicTacToe.cpu if player == TicTacToe.player else TicTacToe.player
        if TicTacToe.isWin(board)[0] :
            if player is TicTacToe.cpu:
                return -1,-1
            else:
                return 1,-1
        res_list=[] # list for appending the result
        c= board.count(' ')
        if  c is 0:
            return 0,-1
        _list=[] # list for storing the indexes where ' ' appears
        for i in range(len(board)):
            if board[i] == ' ':
                _list.append(i)
        #tempboardlist=list(board)
        for i in _list:
            board[i]=player
            ret,move=TicTacToe.nextMove(board,nextplayer)
            res_list.append(ret)
            board[i]=' '
        if player is TicTacToe.cpu:
            maxele=max(res_list)
            return maxele,_list[res_list.index(maxele)]
        else :
            minele=min(res_list)
            return minele,_list[res_list.index(minele)]

    def reset():
        TicTacToe.board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
        
    def printBoard():
        return '\n ————\n'.join(['|'.join([' {} '.format(TicTacToe.get(i,j)) for i in range(3)])for j in range(3)])

class Command(Plugin):

    @Plugin.requires_args
    def run(roboronya, conv, cmd_args, **kwargs):
        Plugin.run(roboronya, conv, cmd_args, **kwargs)
        # Let's play some tic tac toe with Roboronya.

        if len(cmd_args) == 1:
            if cmd_args[0] == 'help':# Help for the command
                roboronya.send_message(
                    conv,
                    "**Let roboronya start the game:**\n/tictactoe start\n"+
                    "**Start or continue on position (x,y):**\n/tictactoe x_pos y_pos\n"+
                    "**Game stats:**\n/tictactoe stats",
                    **kwargs)
            elif cmd_args[0] == 'stats':# Game stats
                roboronya.send_message(
                    conv,
                    "**Roboronya:** {}\n".format(TicTacToe.cpuWins)+
                    "**Peasants:** {}\n".format(TicTacToe.peasantsWins)+
                    "**Draws:** {}".format(TicTacToe.draws),
                    **kwargs)
            elif cmd_args[0] == 'start': # Let roboronya start the game
                if TicTacToe.start():# Roboronya starts the game
                    roboronya.send_message(
                        conv,
                        TicTacToe.printBoard(),
                        **kwargs)
                else: # Game already started
                    roboronya.send_message(
                        conv,
                        TicTacToe.printBoard()+'\nGame already started',
                        **kwargs)
        elif len(cmd_args) == 2:
            x = int(cmd_args[0])
            y = int(cmd_args[1])
            if (x <= 2 and x >= 0) and (y <= 2 and y >= 0): # Valid positions
                if TicTacToe.put(x, y):# If position not taken
                    win, player = TicTacToe.isWin(TicTacToe.board)
                    if win:# If someone wins
                        if player == TicTacToe.cpu: # If roboronya wins
                            TicTacToe.cpuWins += 1
                            roboronya.send_message(
                                conv,
                                TicTacToe.printBoard()+'\n**Roboronya WINS!**',
                                **kwargs)
                            TicTacToe.reset()
                        else: # If the peasants win
                            TicTacToe.peasantsWins += 1
                            roboronya.send_message(
                                conv,
                                TicTacToe.printBoard()+'\n**You WIN!!**',
                                **kwargs)
                            TicTacToe.reset()
                    elif TicTacToe.isDraw(): # If it was a draw
                        TicTacToe.draws += 1
                        roboronya.send_message(
                            conv,
                            TicTacToe.printBoard()+'\n**Draw!!**',
                            **kwargs)
                        TicTacToe.reset()
                    else: # If no one has won yet
                        roboronya.send_message(
                            conv,
                            TicTacToe.printBoard(),
                            **kwargs)
                else: # If position is taken
                    roboronya.send_message(
                        conv,
                        TicTacToe.printBoard()+'\nChoose another position',
                        **kwargs)
            else: # If position is invalid
                roboronya.send_message(
                    conv,
                    TicTacToe.printBoard()+'\nInvalid position',
                    **kwargs)

