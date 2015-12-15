from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from slot_machine.models import Word, Poem

class BaseViewTest(APITestCase):
    fixtures = ['test_words.json', 'test_poems.json']

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

    def test_saves_posted_poem_and_word_relations(self):
        # Test POST - saves new poem and relations to words
        response = self.client.post(self.url, {'text': 'poem-four', 'words': [1]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Poem.objects.count(), 4)
        self.assertEqual(Poem.objects.last().text, 'poem-four')

    def test_fetches_one_random_poem(self):
        # Test POST - after saving poem, fetches one poems and returns them as response
        # Test GET - list one random poem
        response = self.client.post(self.url, {'text': 'poem-four', 'words': [1]}, format='json')
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
