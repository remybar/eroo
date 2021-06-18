import logging
import multiprocessing
from functools import partial
import re
import requests


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
        partitions.append(lst[pos : pos + part_size])
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


def download_media_file(file_info, root_dir):
    """
    download a media file into the folder `root_dir`
    """
    url, filename = file_info
    filepath = root_dir / filename

    try:
        response = requests.get(url)
        if response.status_code != 200:
            logger.warning("Unable to download the media file at '%s'", url)
            return

        if not filepath.parent.exists():
            filepath.parent.mkdir(parents=True)

        with open(filepath, "wb") as f:
            f.write(response.content)
    except Exception as e:
        logger.error("Unable to download the media file (error: %s)", str(e))


def download_media_files(root_dir, files_info):
    """
    download all media files from `files_info` into the folder `root_dir`
    """
    pool = multiprocessing.Pool()
    download_func = partial(download_media_file, root_dir=root_dir)
    pool.map(download_func, files_info)
    pool.close()
    pool.join()
