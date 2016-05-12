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

def get_filename_index(filename):
    """Returns either 0 or the number at the end of a filename."""
    dirname, basename = path.split(filename)
    basename, extension = path.splitext(basename)

    # Index backwards from end of basename.
    filename_index = 0
    for idx in range(-1, -len(basename), -1):
        substring = basename[idx:]
        if substring.isdigit():
            filename_index = int(substring)
        else:
            break

    return filename_index

def replace_filename_index(filename, new_index=None):
    """inserts filename index into filename, replacing the existing one, if any.
    If new_index is not set, will increment the existing index."""
    filename_index = get_filename_index(filename)

    # Auto-increment index, if not defined.
    if not new_index:
        new_index = filename_index + 1

    basename, extension = path.splitext(filename)
    new_basename = basename[:-len(str(filename_index))] if (basename[-1]).isdigit() else basename
    return ''.join([new_basename, str(new_index), extension])






