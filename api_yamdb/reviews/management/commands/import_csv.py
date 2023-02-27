from django.core.management import BaseCommand
import csv
from .serializers_for_import import (
    CategoryCmdSerializer, GenresCmdSerializer,
    GenreTitleCmdSerializer, TitleCmdSerializer,
    UserCmdSerializer, ReviewCmdSerializer,
    CommentCmdSerializer
)


CSV_SERIALIZER_LIST = (
    ('static/data/category.csv', CategoryCmdSerializer),
    ('static/data/genre.csv', GenresCmdSerializer),
    ('static/data/titles.csv', TitleCmdSerializer),
    ('static/data/genre_title.csv', GenreTitleCmdSerializer),
    ('static/data/users.csv', UserCmdSerializer),
    ('static/data/review.csv', ReviewCmdSerializer),
    ('static/data/comments.csv', CommentCmdSerializer),
)


class Command(BaseCommand):

    help = 'Adds CSV files into your database'

    def handle(self, *args, **options):
        try:
            for filepath, serializer_type in CSV_SERIALIZER_LIST:
                with open(filepath, encoding="utf8") as csv_file:
                    reader = csv.DictReader(csv_file)
                    for row_dict in reader:
                        serializer = serializer_type(data=row_dict)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            self.stdout.write(self.style.SUCCESS(
                                f'Ошибка в файле {filepath} \n'
                                f'{serializer.errors}'
                            ))

                    self.stdout.write(self.style.SUCCESS(
                        f'Файл {filepath} успешно загружен в базу'
                    ))
            self.stdout.write(self.style.SUCCESS('Все файлы загружены.'))
        except Exception as e:
            raise Exception(f'Ошибка {e}')
