# -*- coding: utf-8 -*-
import random

from bs4 import BeautifulSoup
import giphypop
import requests

from roboronya import config
from roboronya.exceptions import CommandValidationException

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
        'name': 'tictactoe',
        'description': (
            'Play Tic Tac Toe with Roboronya, beware of her skills. '
            'Check */tictactoe help* for more info.'
        )
    },
    {
        'name': 'gato',
        'description': (
            'Tic Tac Toe for those who prefer spanish. *Hola si, taco taco!*'
        )
    },
    {
        'name': 'whatis',
        'description': (
            'Wanna learn the meaning of something? Ask Roboronya, '
            'she knows. For a specific meaning use /whatis <words>, '
            'or use /whatis for a random meaning.'
        )
    },
    {
        'name': 'chucknorris',
        'description': (
            'Look for a ~~random joke~~ undeniable truth about our '
            'lord and savior.'
        )
    },
    {
        'name': 'yesorno',
        'description': (
            'Randomly decide "yes" or "no", with a cool image.'
        )
    },
    {
        'name': 'piratify',
        'description': (
            'Translate some text to the good old pirate language.'
        )
    },
    {
        'name': 'catfacts',
        'description': (
            'Get a random fact about your furry friends.'
        )
    },
    {
        'name': 'xkcd',
        'description': (
            'Get a random XKCD comic, or specify a comic #.'
        )
    },
    {
        'name': 'randomcat',
        'description': (
            'Get a random feline picture. You can also specify '
            'the size of the image [small, med, full] or the '
            'format of the image [jpg, png, gif]. *i. e. '
            '/randomcat size type*'
        )
    }
]


def get_gif_url(keywords):
    """
    Get an URL to a gif, given some keywords.
    """
    response_json = requests.get(
        config.GIFYCAT_SEARCH_URL,
        params={'search_text': ' '.join(keywords)}
    ).json()
    gfycats = response_json.get('gfycats', [])
    if gfycats:
        gfycat_json = random.choice(gfycats)
        return gfycat_json['max2mbGif']
    return None


def requires_args(fn):
    """
        Decorator to validate commands that require arguments.
    """
    def wrapper(roboronya, conv, cmd_args, **kwargs):
        if not cmd_args:
            raise CommandValidationException(
                'Sorry {user_fullname}, the /{command_name} '
                'command requires arguments to work.'
            )
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
    def help(roboronya, conv, cmd_args, **kwargs):
        """
        /help command. Shows the available commands.
        """
        if not cmd_args:
            return roboronya.send_message(
                conv,
                (
                    'Here are the available commands, to learn '
                    'more about a single command type /help '
                    '*command_name*\n'
                    '{}'.format('\n'.join([
                        '**/{}**'.format(command['name'])
                        for command in COMMAND_HELP
                    ]))
                ),
                **kwargs
            )
        try:
            cmd_help = next(
                filter(
                    lambda x: x['name'] == cmd_args[0],
                    COMMAND_HELP
                )
            )
            return roboronya.send_message(
                conv,
                '**/{}**: {}'.format(
                    cmd_help['name'],
                    cmd_help['description'],
                ),
                **kwargs
            )
        except StopIteration:
            return roboronya.send_message(
                conv,
                (
                    'No help found for command: **/{}**.'.format(
                        cmd_args[0]
                    )
                ),
                **kwargs
            )

    @staticmethod
    @requires_args
    def gif(roboronya, conv, cmd_args, **kwargs):
        """
        /gif command. Translates commands argument words as
        gifs using giphy.
        """
        giphy_image = giphypop.translate(phrase=' '.join(cmd_args))
        if giphy_image:
            size_in_mb = giphy_image.filesize * 1e-6
            if size_in_mb > config.MAX_GIF_SIZE_IN_MB:
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
    @requires_args
    def fastgif(roboronya, conv, cmd_args, **kwargs):
        """
        /fastgif command. Searches for a gif and sends the url.
        """
        kwargs['gif_url'] = get_gif_url(cmd_args)
        roboronya.send_message(
            conv,
            (
                'Here is your URL to the gif {user_fullname}: '
                '{gif_url} ... love you btw'
            ),
            **kwargs
        )

    @staticmethod
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
    def magicball(roboronya, conv, cmd_args, **kwargs):
        """
        /magicball command: Randomly answer like a magic ball.
        """

        roboronya.send_message(
            conv,
            random.choice(config.MAGICBALL_ANSWERS),
            **kwargs
        )

    def caracola(*args, **kwargs):
        """
        /caracola command: Alias for magicball.
        """
        Commands.magicball(*args, **kwargs)

    @staticmethod
    @requires_args
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
    @requires_args
    def gfycat(roboronya, conv, cmd_args, **kwargs):
        """
        /gfycat command: Like the /gif command but instead
        of using giphy it uses gfycat.
        """
        gif_url = get_gif_url(cmd_args)
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
    @requires_args
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
    def whatis(roboronya, conv, cmd_args, **kwargs):
        if len(cmd_args) != 0:
            response_json = requests.get(
                config.URBAN_DICT_URL,
                params={'term': ' '.join(cmd_args)}
                ).json()
        else:
            response_json = requests.get(
                config.URBAN_DICT_RANDOM_URL
                ).json()
        termList = response_json.get('list', [])
        bestTerm = termList[0]
        word = bestTerm['word']
        definition = bestTerm['definition']
        author = bestTerm['author']
        example = bestTerm['example']
        text = '**{}**: "{}"\n-{}'.format(word, definition, author)

        if example != '':
            text += '\n\nExample:\n*{}*'.format(example)

        roboronya.send_message(
            conv,
            text,
            **kwargs)

    @staticmethod
    def chucknorris(roboronya, conv, cmd_args, **kwargs):
        random_joke = requests.get(
            config.CHUCK_API_URL
        ).json()
        if random_joke['type'] == 'success':
            return roboronya.send_message(
                conv,
                random_joke['value']['joke'],
                **kwargs
            )
        print(
            'Failed to retrieve joke from {}. '
            'Got response: {}'.format(
                config.CHUCK_API_URL,
                random_joke,
            )
        )
        return roboronya.send_message(
            conv,
            (
                'Sorry I could not find a joke '
                'Please try again later.'
            ),
            **kwargs
        )

    @staticmethod
    def yesorno(roboronya, conv, cmd_args, **kwargs):
        response_json = requests.get(
            config.YES_OR_NO_API
        ).json()
        kwargs['file_extension'] = 'gif'
        return roboronya.send_file(
            conv,
            response_json['answer'],
            response_json['image'],
            **kwargs
        )

    @staticmethod
    @requires_args
    def piratify(roboronya, conv, cmd_args, **kwargs):
        response_json = requests.get(
            config.PIRATE_API_URL,
            params={
                'format': 'json',
                'text': ' '.join(cmd_args)
            }
        ).json()
        if response_json.get('translation'):
            return roboronya.send_message(
                conv,
                '**{}**'.format(response_json['translation']['pirate']),
                **kwargs
            )
        return roboronya.send_message(
            conv,
            'Sorry I could not piratify your message.',
            **kwargs
        )

    @staticmethod
    def catfacts(roboronya, conv, cmd_args, **kwargs):
        response_json = requests.get(
            config.CATFACTS_API_URL
        ).json()
        if (
            response_json.get('success') == 'true' and
            response_json.get('facts')
        ):
            return roboronya.send_message(
                conv,
                (
                    '**Did you know?** {}'.format(
                        '\n'.join(response_json['facts'])
                    )
                ),
                **kwargs
            )
        return roboronya.send_message(
            conv,
            'Sorry I could not find any cat facts.',
            **kwargs
        )

    @staticmethod
    def xkcd(roboronya, conv, cmd_args, **kwargs):
        response_json = requests.get(
            config.XKCD_LATEST_URL
        ).json()
        current_num = response_json['num']
        if cmd_args:
            try:
                comic_num = int(cmd_args[0])
            except ValueError:
                raise CommandValidationException(
                    'Sorry {user_fullname}, argument must '
                    'be a number between 1 and '+str(current_num)
                )
            if comic_num > current_num or comic_num < 0:
                raise CommandValidationException(
                    'Sorry {user_fullname}, current comic '
                    'numbers are between 1 and '+str(current_num)
                )
        else:
            comic_num = random.randint(1, current_num)

        response_json = requests.get(
            config.XKCD_DETAIL_URL.format(comic_num=comic_num)
        ).json()
        kwargs['file_extension'] = 'png'
        return roboronya.send_file(
            conv,
            'Title: {}'.format(response_json['title']),
            response_json['img'],
            **kwargs
        )

    @staticmethod
    def randomcat(roboronya, conv, cmd_args, **kwargs):
        valid_sizes = ['small', 'med', 'full']
        valid_types = ['jpg', 'png', 'gif']

        cat_img_size = 'small'
        if cmd_args and cmd_args[0] in valid_sizes:
            cat_img_size = cmd_args[0]

        cat_img_type = 'png'
        if len(cmd_args) > 1 and cmd_args[1] in valid_types:
            cat_img_type = cmd_args[1]

        response = requests.get(
            config.CAT_API_URL,
            params={
                'api_key': config.CAT_API_KEY,
                'format': 'xml',
                'results_per_page': '1',
                'size': cat_img_size,
                'type': cat_img_type,
            }
        )
        xml = BeautifulSoup(response.content, 'html.parser')
        kwargs['file_extension'] = 'png'
        return roboronya.send_file(
            conv,
            'Here\'s your cat {user_fullname}:',
            xml.images.image.url.text,
            **kwargs
        )
