# Mobile Verification Toolkit (MVT)
# Copyright (c) 2021-2022 Claudio Guarnieri.
# Use of this software is governed by the MVT License 1.1 that can be found at
#   https://license.mvt.re/1.1/

import logging

from mvt.android.parsers import parse_dumpsys_activity_resolver_table

from .base import BugReportModule


class Activities(BugReportModule):
    """This module extracts details on receivers for risky activities."""

    def __init__(self, file_path: str = None, target_path: str = None,
                 results_path: str = None, fast_mode: bool = False,
                 log: logging.Logger = logging.getLogger(__name__),
                 results: list = []) -> None:
        super().__init__(file_path=file_path, target_path=target_path,
                         results_path=results_path, fast_mode=fast_mode,
                         log=log, results=results)

        self.results = results if results else {}

    def check_indicators(self) -> None:
        if not self.indicators:
            return

        for intent, activities in self.results.items():
            for activity in activities:
                ioc = self.indicators.check_app_id(activity["package_name"])
                if ioc:
                    activity["matched_indicator"] = ioc
                    self.detected.append({intent: activity})
                    continue

    def run(self) -> None:
        content = self._get_dumpstate_file()
        if not content:
            self.log.error("Unable to find dumpstate file. Did you provide a valid bug report archive?")
            return

        lines = []
        in_package = False
        for line in content.decode(errors="ignore").splitlines():
            if line.strip() == "DUMP OF SERVICE package:":
                in_package = True
                continue

            if not in_package:
                continue

            if line.strip().startswith("------------------------------------------------------------------------------"):
                break

            lines.append(line)

        self.results = parse_dumpsys_activity_resolver_table("\n".join(lines))

        self.log.info("Extracted activities for %d intents", len(self.results))
