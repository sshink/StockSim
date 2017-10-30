#!/usr/bin/env python
import argparse
from collections import namedtuple
from enum import Enum
from datetime import date, datetime
import csv


class History(dict):
    Mode = Enum("Mode", "CSV JSON")
    HistoryData = namedtuple("HistoryData", "open, high, low, close, volume")

    def load(self, data, mode=Mode.CSV):
        # print("Mode: " + mode.name)
        if mode == History.Mode.CSV:
            lines = data.splitlines()
            lines[0] = lines[0].lower()
            r = csv.DictReader(lines)
            # date,open,high,low,close,volume
            self = dict()
            for row in r:
                d = datetime.strptime(list(row.values())[0], "%Y-%M-%d").date()
                self[d] = History.HistoryData(row["open"], row["high"], row["low"], row["close"], row["volume"])
                print(d, self[d])
        elif mode == History.Mode.JSON:
            # Not implemented
            pass
        else:
            # Unsupported mode
            pass


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="TODO")
    parser.add_argument("history", nargs='?', default="history.txt",
                        help="File containing history data")
    parser.add_argument('-j', '--json', action="store_true",
                        help="History data is stored in JSON.")

    args = parser.parse_args()

    if args.json:
        mode = History.Mode.JSON
    else:
        mode = History.Mode.CSV

    h = History()
    with open(args.history) as f:
        h.load(f.read(), mode)


if __name__ == "__main__":
    # execute only if run as a script
    print("Welcome to StockSim!")
    main()
