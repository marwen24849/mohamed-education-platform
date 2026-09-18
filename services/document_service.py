import os
from pathlib import Path
from werkzeug.utils import secure_filename

from config import ALLOWED_EXTENSIONS


def _get_stream_size(file_storage):
    stream = getattr(file_storage, 'stream', None)
    if stream is None:
        return 0

    try:
        stream.seek(0, os.SEEK_END)
        size = stream.tell()
        stream.seek(0)
        return size
    except (AttributeError, OSError, ValueError):
        try:
            stream.seek(0)
        except Exception:
            pass
        return 0


def validate_upload(file_storage):
    if file_storage is None or file_storage.filename == '':
        return False, 'Aucun fichier sélectionné.'

    filename = secure_filename(file_storage.filename)
    if '.' not in filename:
        return False, 'Le fichier doit avoir une extension valide.'

    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, 'Type de fichier non autorisé.'

    stream = getattr(file_storage, 'stream', None)
    if stream is not None:
        try:
            stream.seek(0, os.SEEK_END)
            size = stream.tell()
            stream.seek(0)
        except (AttributeError, OSError, ValueError):
            size = 0
    else:
        try:
            size = file_storage.content_length
        except Exception:
            size = 0

    if size is None:
        size = 0

    if size <= 0:
        return False, 'Le fichier est vide.'

    max_size = int(os.getenv('MAX_CONTENT_LENGTH', 15 * 1024 * 1024))
    if size > max_size:
        return False, f'Le fichier dépasse la taille autorisée ({max_size // (1024 * 1024)} Mo).'

    return True, {'filename': filename, 'extension': ext, 'size': size}


def build_safe_filename(filename):
    safe = secure_filename(filename)
    if not safe:
        safe = 'document'
    stem = Path(safe).stem
    suffix = Path(safe).suffix.lower()
    return f'{stem}-{__import__("uuid").uuid4().hex}{suffix}'
