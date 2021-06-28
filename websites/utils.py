import codecs
import logging
import json
import re
import requests
from pathlib import Path

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from .storage_backends import private_storage

_logger = logging.getLogger("utils")


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


def download_media_file(url, filename):
    """
    download a media file from `url`.
    """
    try:
        response = requests.get(url)
        if response.status_code != 200:
            _logger.warning("Unable to download the media file at '%s'", url)
            return None
    except Exception as e:
        _logger.error("Unable to download the media file (error: %s)", str(e))
        return None

    media_file = NamedTemporaryFile(delete=True)
    media_file.write(response.content)
    media_file.flush()

    return media_file


def save_debug_data(filename, data):
    """ save debug data in a `filename` in the private media storage """
    _logger.info("save debug data {'filename': %s}", filename)
    file = NamedTemporaryFile(mode="wb+", delete=True)
    encodedData = json.dumps(data, indent=2).encode('utf-8')
    try:
        file.write(encodedData)
        file.flush()
        private_storage.save(f"private/debug/{filename}", File(file))
        _logger.info("debug data written")
    except Exception as e:
        _logger.exception("exception: %s, type: %s", str(e), type(e).__name__)
