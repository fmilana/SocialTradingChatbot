# coding:utf-8

import os, csv

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count
from django.contrib.auth.models import User
# from django.core.files import File
# from django.utils.timezone import make_aware
from imagetagging.models import ImageTask, GroundTruthTag, Tag


@transaction.atomic
class Command(BaseCommand):
    # args = '<poll_id poll_id ...>'
    help = 'Export tagging data to csv file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs='+', type=str)

        # Named (optional) arguments
        # parser.add_argument(
        #     '--update',
        #     action='store_true',
        #     help='clear groundtruth tags before adding new',
        # )

    def handle(self, *args, **options):
        self.stdout.write("exporting.. \n")

        filename = options['csv_file'][0]
        writer = csv.writer(open(filename, 'w', encoding='utf-8'))
        writer.writerow(('user', 'condition', 'attempted', 'correct', 'images', 'timestamp'))

        for current_user in User.objects.all():
            tags = Tag.objects.filter(user=current_user)
            no_total_tags = tags.count()
            correct_tags = tags.filter(correct=True)
            no_correct_tags = correct_tags.count()

            # count how many images have 3 correct tags from this user?
            no_successful_images = ImageTask.objects.filter(
                        tag__user=current_user,tag__correct=True).annotate(
                        n_correct=Count('tag')).filter(
                            n_correct=3).count()

            try:
                row = (current_user.pk, 
                        current_user.participant.condition_active,
                        no_total_tags, 
                        no_correct_tags, 
                        no_successful_images, 
                        current_user.participant.created_at)
                print(row)
                writer.writerow(row)
                
            except User.participant.RelatedObjectDoesNotExist:
                print('skipping', current_user)


        self.stdout.write("\n..done\n")
