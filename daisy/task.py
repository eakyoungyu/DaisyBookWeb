from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery_progress.backend import ProgressRecorder
from time import sleep

import os
import pathlib

from webapp.settings import MEDIA_ROOT
from .bash import set_key
from .image_to_text import detect_document


@shared_task
def sleepy(duration):
    sleep(duration)
    return None


@shared_task(bind=True)
def my_task(self):
    progress_recorder = ProgressRecorder(self)
    result = 0
    seconds = 2
    print('SECONDS', seconds)
    for i in range(seconds):
        sleep(1)
        result += i
        print(i)
        progress_recorder.set_progress(i + 1, seconds)
    return result


@shared_task(bind=True)
def make_book_async(self, book_name, start_file, end_file):
    set_key()
    progress_recorder = ProgressRecorder(self)

    IMG_DIR = os.path.join(MEDIA_ROOT, book_name)
    BOOK_DIR = os.path.join(MEDIA_ROOT, 'txt_book')
    book_path = os.path.join(BOOK_DIR, book_name + ".txt")

    pathlib.Path(IMG_DIR).mkdir(exist_ok=True, parents=True)
    pathlib.Path(BOOK_DIR).mkdir(exist_ok=True, parents=True)

    start_file = int(start_file)
    end_file = int(end_file)

    for page_num in range(start_file, end_file + 1):
        print(page_num)
        img_path = os.path.join(IMG_DIR, str(page_num) + ".jpg")
        # call GOOGLE VISION API
        detect_document(img_path, page_num, book_path)
        progress_recorder.set_progress(page_num+1, end_file)
    return 'DONE'
