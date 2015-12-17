import requests
import os

HANDWRITINGIO_KEY = os.environ['HANDWRITINGIO_KEY']
HANDWRITINGIO_SECRET = os.environ['HANDWRITINGIO_SECRET']

class Handwriting:
    API_URL = 'https://api.handwriting.io/'
    TOKEN_PAIR = (HANDWRITINGIO_KEY, HANDWRITINGIO_SECRET)

    render_types = ['png', 'pdf',]
    render_config = {
        'all': {
            'height': 'auto',
        },
        'png': {
            'width': '500px',
        },
        'pdf': {
            'width': '8in',
        },
    }

    def __init__(self, handwriting_id, text):
        self.handwriting_id = handwriting_id
        self.text = text

    def render(self, type='png'):
        url = '{0}render/{1}/'.format(self.API_URL, type)
        query_params = {
            'handwriting_id': self.handwriting_id,
            'text': self.text,
        }
        query_params.update(self.render_config['all'])
        query_params.update(self.render_config[type])
        response = requests.get(url, auth=self.TOKEN_PAIR, params=query_params)
        return response

    @classmethod
    def list(cls):
        url = '{0}handwritings/'.format(cls.API_URL)
        params = {
            'limit': '10',
        }
        response = requests.get(url, auth=cls.TOKEN_PAIR, params=params)
        return response
