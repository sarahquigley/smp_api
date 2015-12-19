from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.test import TestCase
from slot_machine.models import Word, Poem, RenderedPoem
from slot_machine.handwriting import Handwriting
from mock import patch

class WordModelTest(TestCase):
    def test_on_save_word_text_is_lowercased(self):
        # Test that Word model text is saved as lowercase
        word = Word(text='Hello')
        word.save()
        self.assertEqual(word.text, 'hello')

    def test_word_text_should_be_invalid(self):
        # Test that Word model text with spaces or non-letter characters
        # (other than hyphen) is invalid
        # This test could possibly be made more thorough
        invalid = ['a b', ' a', 'a ', '$', '%']
        for text in invalid:
            word = Word(text=text)
            with self.assertRaises(ValidationError):
                word.full_clean()


    def test_word_text_should_be_valid(self):
        # Test that Word model text without spaces or non-letter characters
        # (other than hyphen) is invalid
        # This test could possibly be made more thorough
        valid = ['a', 'a-b', ur'\u00C0']
        for text in valid:
            word = Word(text=text)
            try:
                word.full_clean()
            except ValidationError:
                self.fail("Word#save raised ValidationError unexpectedly.")

class PoemModelTest(TestCase):

    @patch.object(Handwriting, 'render')
    def test_render_calls_handwriting_render_method_and_returns_rendered_poem(self, mock_render):
        poem = Poem(text='poem', handwriting_id='1')
        rendered_poem = poem.render()
        mock_render.assert_called_with('png')

    @patch.object(Poem, 'render')
    def test_save_calls_poem_render(self, mock_render):
        poem = Poem(text='poem', handwriting_id='1')
        poem.save()
        mock_render.assert_any_call('png')
        mock_render.assert_any_call('pdf')

class RenderedPoemModelTest(TestCase):
    def test_content_type_returns_correct_value_depending_on_type(self):
        rendered_poem = RenderedPoem(type='png')
        self.assertEqual(rendered_poem.content_type(), 'image/png')
        rendered_poem = RenderedPoem(type='pdf')
        self.assertEqual(rendered_poem.content_type(), 'application/pdf')

