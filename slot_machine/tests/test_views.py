from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from slot_machine.models import Word, Poem, RenderedPoem
from slot_machine.handwriting import Handwriting
from mock import patch

class BaseViewTest(APITestCase):
    fixtures = ['test_words.json', 'test_poems.json', 'test_renderedpoems.json']

    def setUp(self):
        self.words = Word.objects.all()
        self.poems = Poem.objects.all()


class WordListViewTest(BaseViewTest):
    url = reverse('word-list')

    def test_gets_list_of_all_words(self):
        # Test GET - list all words
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        for i, item in enumerate(response.data):
            self.assertEqual(item.get('id'), self.words[i].id)
            self.assertEqual(item.get('text'), self.words[i].text)

    def test_gets_word_list_filtered_by_pk(self):
        # Test GET - list words filtered by pk
        response = self.client.get(self.url, {'pk__in': [1, 3]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get('id'), self.words[0].id)
        self.assertEqual(response.data[0].get('text'), self.words[0].text)
        self.assertEqual(response.data[1].get('id'), self.words[2].id)
        self.assertEqual(response.data[1].get('text'), self.words[2].text)


class WordSubmitViewTest(BaseViewTest):
    url = reverse('word-submit')

    def test_saves_posted_word(self):
        # Test POST - saves new word
        response = self.client.post(self.url, {'text': 'word-four'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Word.objects.count(), 4)
        self.assertEqual(Word.objects.last().text, 'word-four')

    def test_fetches_three_random_words(self):
        # Test POST - after saving word, fetches three random words and returns them as response
        response = self.client.post(self.url, {'text': 'word-four'}, format='json')
        self.assertEqual(len(response.data), 1)
        for item in response.data.get('results'):
            self.assertIn(item.get('id'), map((lambda x: x.id), self.words))
            self.assertIn(item.get('text'), map((lambda x: x.text), self.words))


class PoemSubmitViewTest(BaseViewTest):
    url = reverse('poem-submit')

    @patch.object(Poem, 'render')
    def test_saves_posted_poem_and_word_relations(self, mock_render):
        # Test POST - saves new poem and relations to words
        response = self.client.post(self.url, {
            'text': 'poem-four',
            'words': [1],
            'handwriting_id': '1',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Poem.objects.count(), 4)
        self.assertEqual(Poem.objects.last().text, 'poem-four')

    @patch.object(Poem, 'render')
    def test_fetches_one_random_poem(self, mock_render):
        # Test POST - after saving poem, fetches one poems and returns them as response
        # Test GET - list one random poem
        response = self.client.post(self.url, {
            'text': 'poem-four',
            'words': [1],
            'handwriting_id': '1',
        }, format='json')
        self.assertEqual(len(response.data), 1)
        for item in response.data.get('results'):
            self.assertIn(item.get('id'), map((lambda x: x.id), self.poems))
            self.assertIn(item.get('text'), map((lambda x: x.text), self.poems))


class PoemRetrieveViewTest(BaseViewTest):
    url = reverse('poem-retrieve', kwargs={'pk': 1})

    def test_gets_poem(self):
        # Test GET - gets a single poem identified by given pk
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PoemPreviewViewTest(BaseViewTest):
    url = reverse('poem-preview')

    @patch.object(Handwriting, 'render')
    def test_gets_rendered_poem_png_preview(self, mock_handwriting_render):
        # Test GET - gets rendered poem png for poem of given pk
        mock_handwriting_render.return_value.status_code = status.HTTP_200_OK
        response = self.client.get(self.url, format='json')
        mock_handwriting_render.expect_called_once_with('png')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(Handwriting, 'render')
    def test_gets_rendered_poem_pdf_preview(self, mock_handwriting_render):
        # Test GET - gets rendered poem png for poem of given pk
        mock_handwriting_render.return_value.status_code = status.HTTP_200_OK
        response = self.client.get(self.url, {'type': 'pdf'}, format='json')
        mock_handwriting_render.expect_called_once_with('pdf')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PoemRenderViewTest(BaseViewTest):
    url = reverse('poem-render', kwargs={'pk': 1})

    def test_gets_rendered_poem_png(self):
        # Test GET - gets rendered poem png for poem of given pk
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'image/png')

    def test_gets_rendered_poem_pdf(self):
        # Test GET - gets rendered poem pdf for poem of given pk
        response = self.client.get(self.url, {'type': 'pdf'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')

class HandwritingListViewTest(BaseViewTest):
    url = reverse('handwriting-list')

    @patch.object(Handwriting, 'list')
    def test_gets_handwriting_list(self, mock_handwriting_list):
        # Test GET - gets list of handwritings
        mock_handwriting_list.return_value.status_code = status.HTTP_200_OK
        mock_handwriting_list.return_value.text = '[]'
        response = self.client.get(self.url, format='json')
        mock_handwriting_list.assert_called_once_with()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
