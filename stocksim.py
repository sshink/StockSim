#!/usr/bin/env python

# Copyright (C) 2017 Simon Shink

# This file is part of StockSim.
# 
# StockSim is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# StockSim is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with StockSim.  If not, see <http://www.gnu.org/licenses/>.

import argparse
from collections import namedtuple
from enum import Enum
from datetime import date, datetime, timedelta
import csv

DataMode = Enum("Mode", "CSV JSON")
TransactionType = Enum("TransactionType", "Cash Shares")


class History(dict):
    HistoryData = namedtuple("HistoryData", "open, high, low, close, volume")

    def load(self, data, mode=DataMode.CSV):
        # print("Mode: " + mode.name)
        if mode == DataMode.CSV:
            lines = data.splitlines()
            lines[0] = lines[0].lower()
            r = csv.DictReader(lines)
            # date,open,high,low,close,volume
            # self = dict()
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

    def get_latest(self, date: date):
        if date in self:
            return self[date]
        elif date > min(self.keys()):
            return self[max([d for d in self.keys() if d < date])]
        else:
            return None

    def get_next(self, date: date):
        if date in self:
            return self[date]
        elif date < max(self.keys()):
            return self[min([d for d in self.keys() if d > date])]
        else:
            return None


class Dividend(dict):
    def __init__(self, t=TransactionType.Cash):
        super(Dividend, self).__init__()
        self.type = t

    def load(self, data, mode=DataMode.CSV):
        if mode == DataMode.CSV:
            lines = data.splitlines()
            lines[0] = lines[0].lower()
            reader = csv.DictReader(lines)
            for row in reader:
                r = list(row.values())
                d = datetime.strptime(r[0], "%Y-%M-%d").date()
                v = r[1]
                if v > 0:
                    self[d] = v
        elif mode == DataMode.JSON:
            # Not implemented
            pass
        else:
            # Unsupported mode
            pass


class TransactionHistory(dict):
    def __init__(self, t=TransactionType.Cash):
        super(TransactionHistory, self).__init__()
        self.type = t

    def load(self, data, mode=DataMode.CSV):
        if mode == DataMode.CSV:
            lines = data.splitlines()
            lines[0] = lines[0].lower()
            reader = csv.DictReader(lines)
            for row in reader:
                r = list(row.values())
                d = datetime.strptime(r[0], "%Y-%M-%d").date()
                v = r[1]
                if v != 0:
                    self[d] = v
        elif mode == DataMode.JSON:
            # Not implemented
            pass
        else:
            # Unsupported mode
            pass


class Stock:
    # Return
    # Reinvest

    def __init__(self):
        super(Stock, self).__init__()
        self.history = History()
        self.reinvest = False
        self.transactions = TransactionHistory()
        self.shares = {date.min: 0}
        self.cost = {date.min: 0}
        self.value = {date.min: 0}
        self.gain = {date.min: 0}
        self.gainp = {date.min: 0}

    def calc_shares(self):
        self.shares = self.calc_shares(self.transactions, self.history, self.reinvest)
        return self.shares

    @staticmethod
    def calc_shares(transactions: TransactionHistory, history: History = None, reinvest=False):
        shares = {min(transactions) - timedelta(1): 0}
        s = 0
        for k in sorted(transactions):
            if transactions.type == TransactionType.Shares:
                s += transactions[k]
            elif transactions.type == TransactionType.Cash:
                # TODO: Handle exceptions
                s += transactions[k] / history[k]["close"]
            else:
                # Unsupported transaction type
                pass
            shares[k] = s

        if reinvest:
            # TODO reinvest dividend
            pass

        return shares

    def calc_cost(self):
        self.cost = self.calc_cost(self.transactions, self.history)
        return self.cost

    @staticmethod
    def calc_cost(transactions: TransactionHistory, history: History = None):
        cost = {min(transactions) - timedelta(1): 0}
        s = 0
        for k in sorted(transactions):
            if transactions.type == TransactionType.Shares:
                # TODO: Handle exceptions
                s += transactions[k] * history[k]["close"]
            elif transactions.type == TransactionType.Cash:
                s += transactions[k]
            else:
                # Unsupported transaction type
                pass
            cost[k] = s
        return cost

    def calc_value(self):
        self.value = self.calc_value(self.shares, self.history)
        return self.value

    @staticmethod
    def calc_value(shares, history: History):
        value = {}
        d = min(shares)
        s = 0
        for k in sorted(shares):
            while d < k:
                value[d] = s * history[d]["close"]
                d += timedelta(1)
            s = shares[k]
        value[d] = s * history[d]["close"]
        return value

    def calc_gain(self):
        self.gain = self.calc_gain(self.value, self.cost)
        return self.gain

    @staticmethod
    def calc_gain(value, cost):
        gain = {}
        d = max([min(value), min(cost)])
        c = 0
        for k in sorted(cost):
            while d < k:
                gain[d] = value[d] - c
                d += timedelta(1)
            c = cost[k]
        gain[d] = value[d] - c
        return gain

    def calc_gainp(self):
        self.gainp = self.calc_gainp(self.gain, self.cost)
        return self.gainp

    @staticmethod
    def calc_gainp(gain, cost):
        gainp = {}
        d = max([min(gain), min(cost)])
        c = 0
        for k in sorted(cost):
            while d < k:
                if c != 0:
                    gainp[d] = gain[d] / c
                d += timedelta(1)
            c = cost[k]
        if c != 0:
            gainp[d] = gain[d] / c
        return gainp


class StockSim:
    def __init__(self):
        super(StockSim, self).__init__()
        self.stocks = [Stock()]

    # Save
    # Load
    # Add stock
    # Load stock
    # Export stock
    # Remove stock


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
