from django.test import TestCase
import requests
from slot_machine.handwriting import Handwriting
from mock import patch

class HandwritingTest(TestCase):

    @patch.object(requests, 'get')
    def test_render_gets_rendered_handwriting_with_GET_to_handwritingio_api(self, mock_requests_get):
        # Test GET - gets text rendered in handwriting
        handwriting = Handwriting(handwriting_id='1', text='text')
        handwriting.render('png')
        url = '{0}render/{1}/'.format(handwriting.API_URL, 'png')
        params = {
            'handwriting_id': handwriting.handwriting_id,
            'text': handwriting.text,
            'height': 'auto',
            'width': '500px'
        }
        mock_requests_get.assert_called_with(url, auth=handwriting.TOKEN_PAIR, params=params)
        handwriting.render('pdf')
        url = '{0}render/{1}/'.format(handwriting.API_URL, 'pdf')
        params = {
            'handwriting_id': handwriting.handwriting_id,
            'text': handwriting.text,
            'height': 'auto',
            'width': '8in'
        }
        mock_requests_get.assert_called_with(url, auth=handwriting.TOKEN_PAIR, params=params)

    @patch.object(requests, 'get')
    def test_list_gets_handwriting_list_with_GET_to_handwritingio_api(self, mock_requests_get):
        # Test GET - gets list of handwritings
        Handwriting.list()
        url = '{0}handwritings/'.format(Handwriting.API_URL)
        params = {'limit': '10'}
        mock_requests_get.asset_called_once_with(url, auth=Handwriting.TOKEN_PAIR, params=params)
