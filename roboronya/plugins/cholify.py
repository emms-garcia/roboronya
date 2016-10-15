import random
from roboronya.plugins.plugin import Plugin

class Cholificator(Plugin):

    description = 'Roboronya will use her *Automated Cholification Algorithm* (Patent Pending) to translate your text to a more sophisticated language.'
    name = 'cholify'

    @Plugin.requires_args
    def run(roboronya, conv, cmd_args, **kwargs):

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

        return roboronya.send_message(
            conv,
            ' '.join(_cholify(cmd_args)),
            **kwargs
        )
