# Mobile Verification Toolkit (MVT)
# Copyright (c) 2021-2022 Claudio Guarnieri.
# Use of this software is governed by the MVT License 1.1 that can be found at
#   https://license.mvt.re/1.1/

import logging

from .webkit_base import WebkitBase

WEBKIT_LOCALSTORAGE_ROOT_PATHS = [
    "private/var/mobile/Containers/Data/Application/*/Library/WebKit/WebsiteData/LocalStorage/",
]


class WebkitLocalStorage(WebkitBase):
    """This module looks extracts records from WebKit LocalStorage folders,
    and checks them against any provided list of suspicious domains.


    """

    def __init__(self, file_path: str = None, target_path: str = None,
                 results_path: str = None, fast_mode: bool = False,
                 log: logging.Logger = logging.getLogger(__name__),
                 results: list = []) -> None:
        super().__init__(file_path=file_path, target_path=target_path,
                         results_path=results_path, fast_mode=fast_mode,
                         log=log, results=results)

    def serialize(self, record: dict) -> None:
        return {
            "timestamp": record["isodate"],
            "module": self.__class__.__name__,
            "event": "webkit_local_storage",
            "data": f"WebKit Local Storage folder {record['folder']} containing file for URL {record['url']}",
        }

    def run(self) -> None:
        self._process_webkit_folder(WEBKIT_LOCALSTORAGE_ROOT_PATHS)
        self.log.info("Extracted a total of %d records from WebKit Local Storages",
                      len(self.results))
