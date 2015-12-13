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
            self.assertEqual(item.get('word'), self.words[i].word)

    def test_gets_word_list_filtered_by_pk(self):
        # Test GET - list words filtered by pk
        response = self.client.get(self.url, {'pk__in': [1, 3]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get('id'), self.words[0].id)
        self.assertEqual(response.data[0].get('word'), self.words[0].word)
        self.assertEqual(response.data[1].get('id'), self.words[2].id)
        self.assertEqual(response.data[1].get('word'), self.words[2].word)

    def test_saves_posted_word(self):
        # Test POST - saves new word
        response = self.client.post(self.url, {'word': 'word-four'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Word.objects.count(), 4)
        self.assertEqual(Word.objects.last().word, 'word-four')
        self.assertEqual(response.data.get('id'), 4)
        self.assertEqual(response.data.get('word'), 'word-four')

class WordRandomViewTest(BaseViewTest):
    url = reverse('word-random')

    def assert_random_get(self, response, limit):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), limit)
        for item in response.data:
            self.assertIn(item.get('id'), map((lambda x: x.id), self.words))
            self.assertIn(item.get('word'), map((lambda x: x.word), self.words))

    def test_gets_one_random_word_by_default(self):
        # Test GET - list one random words
        response = self.client.get(self.url, format='json')
        self.assert_random_get(response, 1)

    def test_gets_specified_number_of_random_words(self):
        # Test GET - list specified number of random words
        response = self.client.get(self.url, {'limit': 2}, format='json')
        self.assert_random_get(response, 2)

class PoemCreateViewTest(BaseViewTest):
    url = reverse('poem-create')

    def test_saves_posted_poem_and_word_relations(self):
        # Test POST - saves new poem and relations to words
        response = self.client.post(self.url, {'text': 'poem-four', 'words': [1]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Poem.objects.count(), 4)
        self.assertEqual(Poem.objects.last().text, 'poem-four')
        self.assertEqual(response.data.get('id'), 4)
        self.assertEqual(response.data.get('text'), 'poem-four')

class PoemRetrieveViewTest(BaseViewTest):
    url = reverse('poem-retrieve', kwargs={'pk': 1})

    def test_gets_poem(self):
        # Test GET - gets a single poem identified by given pk
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PoemRandomViewTest(BaseViewTest):
    url = reverse('poem-random')

    def assert_random_get(self, response, limit):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), limit)
        for item in response.data:
            self.assertIn(item.get('id'), map((lambda x: x.id), self.poems))
            self.assertIn(item.get('text'), map((lambda x: x.text), self.poems))

    def test_gets_one_random_poem_by_default(self):
        # Test GET - list one random poem
        response = self.client.get(self.url, format='json')
        self.assert_random_get(response, 1)

    def test_gets_specified_number_of_random_poems(self):
        # Test GET - list specified number of random poems
        response = self.client.get(self.url, {'limit': 2}, format='json')
        self.assert_random_get(response, 2)
