# Mobile Verification Toolkit (MVT)
# Copyright (c) 2021-2022 Claudio Guarnieri.
# Use of this software is governed by the MVT License 1.1 that can be found at
#   https://license.mvt.re/1.1/

import logging

from mvt.android.parsers import parse_dumpsys_accessibility

from .base import BugReportModule


class Accessibility(BugReportModule):
    """This module extracts stats on accessibility."""

    def __init__(self, file_path: str = None, target_path: str = None,
                 results_path: str = None, fast_mode: bool = False,
                 log: logging.Logger = logging.getLogger(__name__),
                 results: list = []) -> None:
        super().__init__(file_path=file_path, target_path=target_path,
                         results_path=results_path, fast_mode=fast_mode,
                         log=log, results=results)

    def check_indicators(self) -> None:
        if not self.indicators:
            return

        for result in self.results:
            ioc = self.indicators.check_app_id(result["package_name"])
            if ioc:
                result["matched_indicator"] = ioc
                self.detected.append(result)
                continue

    def run(self) -> None:
        content = self._get_dumpstate_file()
        if not content:
            self.log.error("Unable to find dumpstate file. Did you provide a valid bug report archive?")
            return

        lines = []
        in_accessibility = False
        for line in content.decode(errors="ignore").splitlines():
            if line.strip() == "DUMP OF SERVICE accessibility:":
                in_accessibility = True
                continue

            if not in_accessibility:
                continue

            if line.strip().startswith("------------------------------------------------------------------------------"):
                break

            lines.append(line)

        self.results = parse_dumpsys_accessibility("\n".join(lines))
        for result in self.results:
            self.log.info("Found installed accessibility service \"%s\"", result.get("service"))

        self.log.info("Identified a total of %d accessibility services", len(self.results))
