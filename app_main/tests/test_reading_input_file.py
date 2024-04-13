from django.test import TestCase
from app_main.models import Submission, Platform
from app_main.read_file import read_links_file
import os


class ReadingInputFileTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(ReadingInputFileTestCase, cls).setUpClass()
        cls.script_dir = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_reading_correct_input_file(self):
        file_path = os.path.join(self.script_dir, "test_input_file.xlsx")
        with open(file_path, "rb") as file:
            data = read_links_file(file)

            self.assertEqual(data,
                             [('Facebook',
                               'https://www.facebook.com/adam.kotowski.5201?comment_id=Y29tbWVudDo2MjEwNTQwNDMzOTA4NTNfMjQyMTQ0MzY1MDk3OTk1'),
                              ('Facebook',
                               'https://www.facebook.com/profile.php?id=100087905568334&comment_id=Y29tbWVudDo2MjI1MDI1NTk5MTI2NjhfNjUwMDgwMzE1OTk3MTYwNQ%3D%3D'),
                              ('Twitter', 'https://twitter.com/DonicaKrystian'),
                              ('Twitter', 'https://twitter.com/DonicaKrystian'),
                              ('Facebook', 'https://www.facebook.com/piotr.plasan')])

