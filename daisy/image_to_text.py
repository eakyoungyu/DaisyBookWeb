# -*- coding:utf-8 -*-
import io
import os
import pathlib
import asyncio

from google.cloud import vision
from pykospacing import spacing
from .models import Book
from webapp.settings import MEDIA_ROOT, BOOK_ROOT
from .bash import set_key


async def make_txt_file(img_path, page_num, txt_path):
    response = await detect_document(img_path)
    print('start', img_path)
    data = ''
    page_str = '@@p' + str(page_num) + '\n'
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                par_word = ''
                prev_word = ''
                is_line_wrapping_break = False
                for word in paragraph.words:
                    cur_word = ''
                    for symbol in word.symbols:
                        par_word += symbol.text
                        cur_word += symbol.text
                        break_type = symbol.property.detected_break.type
                        if break_type == 3:
                            is_line_wrapping_break = True
                            prev_word = cur_word
                        elif break_type == 1:
                            if is_line_wrapping_break:
                                prev_idx = par_word.rfind(prev_word)
                                un_spaced = par_word[prev_idx:]
                                par_word = par_word[:prev_idx]
                                cur_word = spacing(un_spaced)
                                is_line_wrapping_break = False
                                par_word += cur_word
                            par_word += ' '
                # remove page number
                if par_word != str(page_num):
                    data += par_word
                    data += '\n'

    if data == '':
        data = '빈 면\n'
    data = page_str + data
    with io.open(txt_path, 'w', encoding='UTF-8') as book_file:
        book_file.write(data)
    print('end', img_path)


async def detect_document(img_path):
    client = vision.ImageAnnotatorClient()
    print('request', img_path)
    with io.open(img_path, 'rb') as image_file:
        content = image_file.read()
        image = vision.types.Image(content=content)
        # response: json
        response = client.document_text_detection(image=image)
        # print(response.full_text_annotation.text)
    print('response', img_path)
    return response


async def make_files(start_file, end_file, IMG_DIR, TXT_DIR):
    tasks = []
    for page_num in range(start_file, end_file + 1):
        print(page_num)
        img_path = os.path.join(IMG_DIR, str(page_num) + ".jpg")
        txt_path = os.path.join(TXT_DIR, str(page_num) + ".txt")
        # call GOOGLE VISION API
        tasks.append(asyncio.ensure_future(
            make_txt_file(img_path, page_num, txt_path)))

    await asyncio.gather(*tasks)


def make_book(book_name, start_file, end_file):
    set_key()
    IMG_DIR = os.path.join(MEDIA_ROOT, book_name)
    TXT_DIR = os.path.join(MEDIA_ROOT, 'text', book_name)
    book_path = os.path.join(BOOK_ROOT, book_name + ".txt")

    pathlib.Path(BOOK_ROOT).mkdir(exist_ok=True, parents=True)
    pathlib.Path(TXT_DIR).mkdir(exist_ok=True, parents=True)

    if os.path.isfile(book_path):
        os.remove(book_path)

    start_file = int(start_file)
    end_file = int(end_file)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # loop = asyncio.get_event_loop()
    loop.run_until_complete(
        make_files(start_file, end_file, IMG_DIR, TXT_DIR))
    loop.close()

    # merge files
    with io.open(book_path, 'w', encoding='UTF-8') as book_file:
        for page_num in range(start_file, end_file + 1):
            txt_path = os.path.join(TXT_DIR, str(page_num) + ".txt")
            with io.open(txt_path, 'r', encoding='UTF-8') as page_file:
                data = page_file.read()
                book_file.write(data)

