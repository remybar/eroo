import logging
import json
import re
import requests
from pathlib import Path

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from .storage_backends import private_storage

_logger = logging.getLogger(__name__)

def partition_list(lst, n):
    """
    partition a list `lst` into `n` even chunks.
    When chunks are not equal, add pending items, one by one, from the first partition.

    Ex: _partition_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], 4)
    => [[1, 2, 3, 4], [5, 6, 7], [8, 9, 10], [11, 12, 13]]

       _partition_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 4)
    => [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15]]
    """
    pos = 0
    partitions = []
    for part_size in [
        len(lst) // n + min(max((len(lst) % n - i), 0), 1) for i in range(n)
    ]:
        partitions.append(lst[pos: pos + part_size])
        pos += part_size
    return partitions

def download_media_file(url, filename):
    """
    download a media file from `url`.
    """
    try:
        response = requests.get(url)
        if response.status_code != 200:
            _logger.warning("Unable to download the media file at '%s'", url)
            return None
    except Exception:
        return None

    media_file = NamedTemporaryFile(delete=True)
    media_file.write(response.content)
    media_file.flush()

    return media_file

def save_debug_data(filename, data):
    """
    save debug data in a `filename` in the private media storage
    """
    _logger.info("save debug data {'filename': %s}", filename)
    file = NamedTemporaryFile(mode="wb+", delete=True)
    try:
        file.write(json.dumps(data, indent=2).encode('utf-8'))
        file.flush()
        private_storage.save(f"debug/{filename}", File(file))
    except Exception as e:
        _logger.exception("exception: %s, type: %s", str(e), type(e).__name__)

def delete_debug_data(filename):
    """
    Delete debug data from the private media storage.
    """
    try:
        private_storage.delete(filename)
    except Exception as e:
        _logger.exception("exception: %s, type: %s", str(e), type(e).__name__)

def get_filename_from_url(url):
    """
    extract the filename from an url
    """
    return url.split("?")[0].split("/")[-1]

def get_extension_from_url(url):
    """
    extract the filename extension from an URL
    """
    filename = get_filename_from_url(url)
    return Path(filename).suffix
