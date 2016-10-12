description = 'Get a random feline picture. You can also specify the size of the image [small, med, full] or the format of the image [jpg, png, gif]. i. e. */randomcat size type*'

from roboronya.plugins.plugin import *

class Command(Plugin):

    def run(roboronya, conv, cmd_args, **kwargs):
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
        message = 'Here\'s your cat {user_fullname}:'
        return roboronya.send_file(
            conv, message, xml.images.image.url.text, **kwargs
        )
