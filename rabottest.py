from unittest import TestCase
from core import CsvReader


test_list = [{'id': '',
              'name': 'Артем',
              'surname': 'Ивлев',
              'patronymic': 'Владимирович',
              'username': 'vinsmazuka',
              'chat_id': '',
              'salary': '24500',
              'deployment_date': '01.12.2018',
              'birthday': '01.01.1998',
              'status': ''},
             {'id': '',
              'name': 'Ксения',
              'surname': 'Закирова',
              'patronymic': 'Раисовна',
              'username': 'firmamento_89',
              'chat_id': '', 'salary': '50000',
              'deployment_date': '12.03.2016',
              'birthday': '01.01.2001',
              'status': ''}]


class TestCoreMethods(TestCase):
    def test_read_file(self):
        """
        Проверка корректного чтения из csv файла
        """
        self.assertEqual(CsvReader.read_file('test.csv'), test_list)


