from wand.image import Image
from os import path
import re

def convert_pdf_to_jpg(pdf_filename, jpg_filename, resolution=300):

    # Auto-add .jpg to end of jpg_filename
    if not path.splitext(jpg_filename)[1]:
        jpg_filename += '.jpg'

    # Convert pdf to sequence of jpg files (will be one per page)
    with Image(filename=pdf_filename, resolution=resolution) as pdf:
        pdf.save(filename=jpg_filename)


def get_jpg_page_number(filename):
    return int(re.findall('([0-9]+)', filename)[0])

def sort_jpg_pages(filenames):
    filenames.sort(key=get_jpg_page_number)