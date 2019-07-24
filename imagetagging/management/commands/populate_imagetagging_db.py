# coding:utf-8

import os, csv

from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import User
# from django.core.files import File
# from django.utils.timezone import make_aware
from ...models import ImageTask, Tag


@transaction.atomic
class Command(BaseCommand):
    # args = '<poll_id poll_id ...>'
    help = 'Load tags from csv file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs='+', type=str)

    def handle(self, *args, **options):
        self.stdout.write("importing.. \n")

        Tag.objects.all().delete()
        ImageTask.objects.all().delete()

        # if User.objects.filter(is_superuser=True).exists():
        #     superuser = User.objects.filter(is_superuser=True)[0]
        # else:
        superuser = User.objects.create_superuser('groundtruth', email='', password='password')

        for filename in options['csv_file']:
            print('filename:', filename)
            reader = csv.reader(open(filename, 'rU', encoding='utf-8'))
            # skip header
            next(reader)
            for line in reader:
                print(line)
                image_number = int(line[0])
                tags = line[1:]

                filename = '%d.jpg' % image_number
                # create ImageTask
                image_task = ImageTask(next_task = None)
                image_task.image.name = os.path.join('imagetagging', 'images', filename)
                image_task.save()

                # create tags
                for t in tags:
                    Tag.objects.create(
                        user = superuser,
                        label = t,
                        image_task = image_task
                    )

            # link images
            all_tasks = ImageTask.objects.all()
            prev_image_task = all_tasks.last()
            for image_task in all_tasks:
                prev_image_task.next_task = image_task
                prev_image_task.save()
                prev_image_task = image_task

        self.stdout.write("\n..done\n")
