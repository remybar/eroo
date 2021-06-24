import logging
import multiprocessing
import json
import re
import requests
from pathlib import Path

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from .storage_backends import private_storage

logger = logging.getLogger(__name__)


def is_ajax(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


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


def explode_airbnb_url(url):
    """
    explode the airbnb url in a tuple (base url, airbnb id)
    """

    def _explode(_url):
        base_url = _url.split("?")[0]
        res = re.search(r"/([0-9]+)$", base_url)
        if res:
            return (base_url, res.group(1))
        return None, None

    try:
        res = _explode(url)
        if not res:
            # the provided url main be a shortcut of the real airbnb URL
            # in this case, just access to the URL to retrieve the real URL
            response = requests.get(url)
            if response.status_code != 200:
                return None, None
            res = _explode(response.url)
    except Exception:
        res = None, None

    return res


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


def download_media_file(data):
    """
    download a media file from `url` and store it in the `media_field` of
    the `parent`.
    """
    url, filename, media_field, parent = data
    try:
        response = requests.get(url)
        if response.status_code != 200:
            logger.warning("Unable to download the media file at '%s'", url)
            return
    except Exception as e:
        logger.error("Unable to download the media file (error: %s)", str(e))

    media_file = NamedTemporaryFile(delete=True)
    media_file.write(response.content)
    media_file.flush()

    media_field.save(filename, File(media_file))
    parent.save()


def download_media_files(files_info):
    """
    download all media files from `files_info`.
    """
    pool = multiprocessing.Pool()
    pool.map(download_media_file, files_info)
    pool.close()
    pool.join()


def save_debug_data(filename, data):
    """ save debug data in a `filename` in the private media storage """
    file = NamedTemporaryFile(mode="w+", delete=True)
    json.dump(data, file, indent=2)
    file.flush()
    private_storage.save(f"private/debug/{filename}", File(file))
