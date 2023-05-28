import os


def _delete_document_file(path):
    if os.path.isfile(path):
        os.remove(path)


def _delete_image(path):
    print("///////")
    if os.path.exists(path):
        print("///////")
        os.remove(path)
