# -*- coding: utf-8 -*-
import random

import giphypop
import requests

from config import (
    GIFYCAT_SEARCH_URL, MAX_GIF_SIZE_IN_MB,
    URBAN_DICT_URL, URBAN_DICT_RANDOM_URL
)

"""
    Helpers for the commands.
"""

COMMAND_HELP = [
    {
        'name': 'ping',
        'description': 'Check if bot is online. Should always work.'
    },
    {
        'name': 'love',
        'description': 'From Roboronya with love.'
    },
    {
        'name': 'cointoss',
        'description': 'Randomly toss a coin. 50-50 chances.'
    },
    {
        'name': 'magicball',
        'description': (
            'Ask Roboronya for advice. She knows more than she tells.'
        ),
    },
    {
        'name': 'caracola',
        'description': (
            'Alias for */magicball*.'
        )
    },
    {
        'name': 'fastgif',
        'description': 'For faster gifs, this only sends back the gif url.'
    },
    {
        'name': 'gif',
        'description': (
            'Searches for a gif (from Giphy) that matches the words '
            'following the command. *i. e. /gif cat*'
        )
    },
    {
        'name': 'gfycat',
        'description': (
            'Searches for a gif (from Gfycat) that matches the words '
            'following the command. *i. e. /gfycat dog*.'
        ),
    },
    {
        'name': 'cholify',
        'description': (
            'Roboronya will use her *Automated Cholification Algorithm* '
            '(Patent Pending) to translate your text to a more sophisticated'
            ' language.'
        )
    },
    {
        'name':'tictactoe',
        'description':'Play Tic Tac Toe with Roboronya, beware of her skills. Check */tictactoe help* for more info.'
    },
    {
        'name':'gato',
        'description':'Tic Tac Toe for those who prefer spanish. *Hola si, taco taco!*'
    },
    {
        'name':'whatis',
        'description':'Wanna learn the meaning of something? Ask Roboronya, she knows. For a specific meaning use /whatis <words>, or use /whatis for a random meaning.'
    }
]
def _failsafe(fn):
    """
    Sends a message in case of command failure.
    """
    error_message = (
        'Sorry {user_fullname} I failed to process '
        'your command: "{original_message}".'
    )

    def wrapper(roboronya, conv, cmd_args, **kwargs):
        try:
            return fn(roboronya, conv, cmd_args, **kwargs)
        except Exception as e:
            print(
                'Failed to execute command: {}. '
                'Error: {}.'.format(
                    kwargs['command_name'],
                    e
                )
            )
            roboronya.send_message(
                conv,
                error_message,
                **kwargs
            )
    return wrapper


def _get_gif_url(keywords):
    """
    Get an URL to a gif, given some keywords.
    """
    response_json = requests.get(
        GIFYCAT_SEARCH_URL,
        params={'search_text': ' '.join(keywords)}
    ).json()
    gfycats = response_json.get('gfycats', [])
    if gfycats:
        gfycat_json = random.choice(gfycats)
        return gfycat_json['max2mbGif']
    return None


def _log_command(fn):
    """
        Decorator to log running command data.
    """
    def wrapper(roboronya, conv, cmd_args, **kwargs):
        print(
            'Running /{} command with arguments: [{}].'.format(
                kwargs['command_name'],
                ', '.join(cmd_args)
            )
        )
        return fn(roboronya, conv, cmd_args, **kwargs)
    return wrapper


def _requires_args(fn):
    """
        Decorator to validate commands that require arguments.
    """
    def wrapper(roboronya, conv, cmd_args, **kwargs):
        if not cmd_args:
            print(
                'The command /{} requires arguments to work.'.format(
                    kwargs['command_name']
                )
            )
            roboronya.send_message(
                conv,
                (
                    'Sorry {user_fullname}, the /{command_name} '
                    'command requires arguments to work.'
                ),
                **kwargs
            )
            return
        return fn(roboronya, conv, cmd_args, **kwargs)
    return wrapper


"""
    Implemented commands. Any /command_name found in a message (and
    arguments) will be redirected here. Parameters are (in order):
    - conv: hangups.conversation.Conversation object.
    - cmd_args (optional): arguments given for the command, or
    in other words any following words written after the command.
"""

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

class Commands(object):

    @staticmethod
    @_log_command
    @_failsafe
    def help(roboronya, conv, cmd_args, **kwargs):
        """
        /help command. Shows the available commands.
        """
        roboronya.send_message(
            conv, '\n'.join([
                '**/{}**: {}'.format(command['name'], command['description'])
                for command in COMMAND_HELP
            ]),
            **kwargs
        )

    @staticmethod
    @_requires_args
    @_log_command
    @_failsafe
    def gif(roboronya, conv, cmd_args, **kwargs):
        """
        /gif command. Translates commands argument words as
        gifs using giphy.
        """
        giphy_image = giphypop.translate(phrase=' '.join(cmd_args))
        if giphy_image:
            size_in_mb = giphy_image.filesize * 1e-6
            if size_in_mb > MAX_GIF_SIZE_IN_MB:
                kwargs['gif_url'] = giphy_image.bitly
                roboronya.send_message(
                    conv,
                    (
                        'Sorry {user_fullname} gif is too large. '
                        'Here\'s the link instead: {gif_url}'
                    ),
                    **kwargs
                )
            else:
                kwargs['file_extension'] = 'gif'
                roboronya.send_file(
                    conv,
                    'Here\'s your gif {user_fullname}.',
                    giphy_image.media_url,
                    **kwargs
                )
        else:
            print(
                'Could not not find a gif for keywords: '
                '{}'.format(cmd_args)
            )
            kwargs['cmd_args'] = cmd_args
            roboronya.send_message(
                conv,
                (
                    'Sorry {user_fullname} I could not find '
                    'a gif for your keywords: {cmd_args}.'
                ),
                **kwargs
            )

    @staticmethod
    @_requires_args
    @_log_command
    @_failsafe
    def fastgif(roboronya, conv, cmd_args, **kwargs):
        """
        /fastgif command. Searches for a gif and sends the url.
        """
        kwargs['gif_url'] = _get_gif_url(cmd_args)
        roboronya.send_message(
            conv,
            (
                'Here is your URL to the gif {user_fullname}: '
                '{gif_url} ... love you btw'
            ),
            **kwargs
        )

    @staticmethod
    @_log_command
    @_failsafe
    def love(roboronya, conv, cmd_args, **kwargs):
        """
        /love command. From Robornya with love.
        """
        roboronya.send_message(
            conv,
            'I love you {user_fullname} <3.',
            **kwargs
        )

    @staticmethod
    @_log_command
    @_failsafe
    def cointoss(roboronya, conv, cmd_args, **kwargs):
        """
        /cointoss command. Tosses a coin to make a decision as gods should,
        based on luck.
        """
        roboronya.send_message(
            conv,
            'heads' if random.getrandbits(1) == 0 else 'tails',
            **kwargs
        )

    @staticmethod
    @_log_command
    @_failsafe
    def ping(roboronya, conv, cmd_args, **kwargs):
        """
        /ping command. Check bot status.
        """
        roboronya.send_message(
            conv,
            '**Pong!**',
            **kwargs
        )

    @staticmethod
    @_log_command
    @_failsafe
    def magicball(roboronya, conv, cmd_args, **kwargs):
        """
        /magicball command: Randomly answer like a magic ball.
        """
        answers = [
            'It is certain {user_fullname}',
            'It is decidedly so {user_fullname}',
            'Without a doubt {user_fullname}',
            'Yes {user_fullname}, definitely',
            'You may rely on it {user_fullname}',
            'As I see it, yes {user_fullname}',
            'Most likely {user_fullname}',
            'Outlook good {user_fullname}',
            'Yes {user_fullname}',
            'Signs point to yes {user_fullname}',
            'Reply hazy, try again {user_fullname}',
            'Ask again later {user_fullname}',
            'Better not tell you now {user_fullname}',
            'Cannot predict now {user_fullname}',
            'Concentrate and ask again {user_fullname}',
            'Don\'t count on it {user_fullname}',
            'My reply is no {user_fullname}',
            'My sources say no {user_fullname}',
            'Outlook not so good {user_fullname}',
            'Very doubtful {user_fullname}'
        ]

        roboronya.send_message(
            conv,
            random.choice(answers),
            **kwargs
        )

    def caracola(*args, **kwargs):
        """
        /caracola command: Alias for magicball.
        """
        Commands.magicball(*args, **kwargs)

    @staticmethod
    @_log_command
    @_failsafe
    def cholify(roboronya, conv, cmd_args, **kwargs):

        def _cholify(words):
            choloWords = []
            for word in words:
                choloWord = ''
                oldChar = ''
                for char in word.lower():
                    if char == 'y':
                        choloWord += 'ii'
                    elif char == 't':
                        choloWord += 'th'
                    elif char == 'u' and (oldChar == 'q'):
                        choloWord += random.choice(['kh', 'k'])
                    elif (char == 'i' or char == 'e') and oldChar == 'c':
                        choloWord = choloWord[:-1]
                        choloWord += random.choice(['s', 'z']) + char
                    elif char == 'h' and oldChar == 'c':
                        choloWord = choloWord[:-1]
                        choloWord += random.choice(['zh', 'sh'])
                    elif char == 'c':
                        choloWord += 'k'
                    elif char == 's':
                        choloWord += 'z'
                    elif char == 'v':
                        choloWord += 'b'
                    elif char == 'b':
                        choloWord += 'v'
                    elif char == 'q':
                        pass
                    else:
                        choloWord += char
                    oldChar = char
                choloWords.append(choloWord)
            return choloWords

        roboronya.send_message(
            conv,
            ' '.join(_cholify(cmd_args)),
            **kwargs
        )

    @staticmethod
    @_requires_args
    @_log_command
    @_failsafe
    def gfycat(roboronya, conv, cmd_args, **kwargs):
        """
        /gfycat command: Like the /gif command but instead
        of using giphy it uses gfycat.
        """
        gif_url = _get_gif_url(cmd_args)
        if gif_url:
            kwargs['file_extension'] = 'gif'
            roboronya.send_file(
                conv,
                'Here\'s your gif {user_fullname}.',
                gif_url,
                **kwargs
            )
        else:
            roboronya.send_message(
                conv,
                'Sorry {user_fullname}, I couldn\'t find'
                ' a gif for you.',
                **kwargs
            )

    @staticmethod
    @_log_command
    @_failsafe
    def tictactoe(roboronya, conv, cmd_args, **kwargs):
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

    def gato(*args, **kwargs):
        Commands.tictactoe(*args, **kwargs)


    @staticmethod
    @_log_command
    @_failsafe
    def whatis(roboronya, conv, cmd_args, **kwargs):
        if len(cmd_args) != 0:
            response_json = requests.get(
                URBAN_DICT_URL,
                params={'term': ' '.join(cmd_args)}
                ).json()
        else:
            response_json = requests.get(
                URBAN_DICT_RANDOM_URL
                ).json()
        termList = response_json.get('list', [])
        bestTerm = termList[0]
        word = bestTerm['word']
        definition = bestTerm['definition']
        author = bestTerm['author']
        example = bestTerm['example']
        text = '**{}**: "{}"\n-{}'.format(word, definition, author)

        if example != '':
            text+='\n\nExample:\n*{}*'.format(example)

        roboronya.send_message(
            conv,
            text,
            **kwargs)
