from django.test import TestCase
from django.urls import reverse

from .models import Note


class NoteModelTest(TestCase):

    def test_str_returns_title_when_set(self):
        note = Note(title='Shopping list', content='Milk, eggs')
        self.assertEqual(str(note), 'Shopping list')

    def test_str_falls_back_to_note_pk_when_no_title(self):
        note = Note.objects.create(content='Untitled thought')
        self.assertEqual(str(note), f'Note {note.pk}')

    def test_display_title_returns_title_when_set(self):
        note = Note(title='My Title', content='Some content')
        self.assertEqual(note.display_title(), 'My Title')

    def test_display_title_truncates_content_when_no_title(self):
        long_content = 'x' * 80
        note = Note(title='', content=long_content)
        result = note.display_title()
        self.assertTrue(result.endswith('…'))
        self.assertEqual(len(result), 61)

    def test_display_title_full_content_when_short_and_no_title(self):
        note = Note(title='', content='Short note')
        self.assertEqual(note.display_title(), 'Short note')

    def test_notes_ordered_newest_first(self):
        first = Note.objects.create(content='First')
        second = Note.objects.create(content='Second')
        notes = list(Note.objects.all())
        self.assertEqual(notes[0], second)
        self.assertEqual(notes[1], first)

    def test_blank_title_is_allowed(self):
        note = Note(title='', content='Content only')
        note.full_clean()

    def test_empty_content_fails_validation(self):
        from django.core.exceptions import ValidationError
        note = Note(title='Title', content='')
        with self.assertRaises(ValidationError):
            note.full_clean()


class NoteListViewTest(TestCase):

    def test_list_view_returns_200(self):
        response = self.client.get(reverse('notes:list'))
        self.assertEqual(response.status_code, 200)

    def test_list_view_uses_correct_template(self):
        response = self.client.get(reverse('notes:list'))
        self.assertTemplateUsed(response, 'notes/note_list.html')

    def test_list_view_shows_notes(self):
        Note.objects.create(title='Hello', content='World')
        response = self.client.get(reverse('notes:list'))
        self.assertContains(response, 'Hello')

    def test_list_view_empty_state(self):
        response = self.client.get(reverse('notes:list'))
        self.assertContains(response, 'No notes yet')

    def test_list_view_newest_note_appears_first(self):
        Note.objects.create(content='Older note')
        Note.objects.create(title='Newer note', content='Details')
        response = self.client.get(reverse('notes:list'))
        content = response.content.decode()
        self.assertLess(content.index('Newer note'), content.index('Older note'))


class NoteCreateViewTest(TestCase):

    def test_create_view_returns_200_on_get(self):
        response = self.client.get(reverse('notes:create'))
        self.assertEqual(response.status_code, 200)

    def test_create_view_uses_correct_template(self):
        response = self.client.get(reverse('notes:create'))
        self.assertTemplateUsed(response, 'notes/note_form.html')

    def test_valid_post_creates_note_and_redirects(self):
        response = self.client.post(reverse('notes:create'), {
            'title': 'Test Note',
            'content': 'Some content here.',
        })
        self.assertRedirects(response, reverse('notes:list'))
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(Note.objects.first().title, 'Test Note')

    def test_valid_post_without_title_creates_note(self):
        self.client.post(reverse('notes:create'), {
            'title': '',
            'content': 'No title, just content.',
        })
        self.assertEqual(Note.objects.count(), 1)

    def test_empty_content_shows_validation_error(self):
        response = self.client.post(reverse('notes:create'), {
            'title': 'Something',
            'content': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Note content cannot be empty')
        self.assertEqual(Note.objects.count(), 0)

    def test_whitespace_only_content_fails_validation(self):
        response = self.client.post(reverse('notes:create'), {
            'title': '',
            'content': '   \n  ',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.count(), 0)
