#!/usr/bin/env python
import argparse
from collections import namedtuple
from enum import Enum
from datetime import date, datetime
import csv

DataMode = Enum("Mode", "CSV JSON")


class History(dict):
    HistoryData = namedtuple("HistoryData", "open, high, low, close, volume")

    def load(self, data, mode=DataMode.CSV):
        # print("Mode: " + mode.name)
        if mode == DataMode.CSV:
            lines = data.splitlines()
            lines[0] = lines[0].lower()
            r = csv.DictReader(lines)
            # date,open,high,low,close,volume
            self = dict()
            for row in r:
                d = datetime.strptime(list(row.values())[0], "%Y-%M-%d").date()
                self[d] = History.HistoryData(row["open"], row["high"], row["low"], row["close"], row["volume"])
                # print(d, self[d])
        elif mode == DataMode.JSON:
            # Not implemented
            pass
        else:
            # Unsupported mode
            pass


class Dividend(dict):
    pass


class TransactionHistory(dict):
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
        mode = DataMode.JSON
    else:
        mode = DataMode.CSV

    h = History()
    with open(args.history) as f:
        h.load(f.read(), mode)


if __name__ == "__main__":
    # execute only if run as a script
    print("Welcome to StockSim!")
    main()
