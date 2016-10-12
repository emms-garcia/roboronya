description = "Wanna learn the meaning of something? Ask Roboronya, she knows. For a specific meaning use /whatis <words>, or use /whatis for a random meaning."

from roboronya.plugins.plugin import *

class Command(Plugin):

    def run(roboronya, conv, cmd_args, **kwargs):

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

        return roboronya.send_message(
            conv,
            text,
            **kwargs)
