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
import json
from collections import namedtuple, OrderedDict
from enum import Enum
from datetime import date, datetime, timedelta
import csv
import sys

DataMode = Enum("Mode", "CSV JSON")
TransactionType = Enum("TransactionType", "Cash Shares")


def floatornone(s):
    return None if s is None else float(s)


def intornone(s):
    return None if s is None else int(s)


class StockHistory(dict):
    HistoryData = namedtuple("HistoryData", "open, high, low, close, volume")

    def __init__(self):
        super(StockHistory, self).__init__()
        self.dividend = None

    def init_dividend(self):
        self.dividend = DividendHistory()

    def load(self, data, mode=DataMode.CSV):
        # print("Mode: " + mode.name)
        if mode == DataMode.CSV:
            lines = data.splitlines()
            lines[0] = lines[0].lower()
            r = csv.DictReader(lines)
            # date,open,high,low,close,volume
            # self = dict()
            for row in r:
                d = datetime.strptime(list(row.values())[0], "%Y-%m-%d").date()
                self[d] = StockHistory.HistoryData(floatornone(row.get("open")), floatornone(row.get("high")),
                                                   floatornone(row.get("low")),
                                                   floatornone(row.get("close")), intornone(row.get("volume")))
                # print(d, self[d])
        elif mode == DataMode.JSON:
            # QuoteMedia JSON
            jsondata = json.loads(data)
            for eoddata in jsondata.get("results").get("history")[0].get("eoddata"):
                d = datetime.strptime(eoddata.get("date"), "%Y-%m-%d").date()
                self[d] = StockHistory.HistoryData(floatornone(eoddata.get("unadjustedopen")),
                                                   floatornone(eoddata.get("unadjustedhigh")),
                                                   floatornone(eoddata.get("unadjustedlow")),
                                                   floatornone(eoddata.get("unadjustedclose")),
                                                   intornone(eoddata.get("sharevolume")))
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


class DividendHistory(dict):
    def __init__(self, t=TransactionType.Cash):
        super(DividendHistory, self).__init__()
        self.type = t

    def load(self, data, mode=DataMode.CSV):
        if mode == DataMode.CSV:
            lines = data.splitlines()
            lines[0] = lines[0].lower()
            reader = csv.DictReader(lines)
            for row in reader:
                r = list(row.values())
                d = datetime.strptime(r[0], "%Y-%m-%d").date()
                v = float(r[1])
                if v > 0:
                    self[d] = v
        elif mode == DataMode.JSON:
            # QuoteMedia JSON
            jsondata = json.loads(data)
            for dividend in jsondata.get("results").get("dividends")[0].get("dividend"):
                d = datetime.strptime(dividend.get("date"), "%Y-%m-%d").date()
                self[d] = floatornone(dividend.get("amount"))
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
                d = datetime.strptime(r[0], "%Y-%m-%d").date()
                v = float(r[1])
                if v != 0:
                    self[d] = v
        elif mode == DataMode.JSON:
            # Not implemented
            pass
        else:
            # Unsupported mode
            pass


class Stock:
    StockData = namedtuple("StockData", "shares, value, cost, gain, gainp")

    def __init__(self):
        super(Stock, self).__init__()
        self.history = StockHistory()
        self.reinvest = False
        self.transactions = TransactionHistory()
        self.shares = {date.min: 0}
        self.cost = {date.min: 0}
        self.value = {date.min: 0}
        self.gain = {date.min: 0}
        self.gainp = {date.min: 0}
        self.data = {date.min: 0}

    def load_files(self, history, transactions, dividend=None, mode=DataMode.CSV):
        with open(history) as file:
            self.history.load(file.read(), mode)
        with open(transactions) as file:
            self.transactions.load(file.read(), mode)
        with open(dividend) as file:
            self.history.init_dividend()
            self.history.dividend.load(file.read(), mode)

    def calc_shares(self):
        self.shares = self._calc_shares(self.transactions, self.history, self.reinvest)
        return self.shares

    @staticmethod
    def _calc_shares(transactions: TransactionHistory, history: StockHistory = None, reinvest=False):
        shares = {min(transactions) - timedelta(1): 0}
        s = 0
        if reinvest and history.dividend is not None:
            div_dates = sorted(history.dividend)
            # Find first applicable dividend date (shares > 0)
            i = 0
            while div_dates[i] < min(transactions):
                i += 1

            for k in sorted(transactions):
                # Calculate dividend up to k
                if i < len(div_dates):
                    while k >= div_dates[i]:
                        # Reinvest dividend
                        if history.dividend.type == TransactionType.Shares:
                            s += s * history.dividend[div_dates[i]]
                        elif history.dividend.type == TransactionType.Cash:
                            price = history.get_latest(div_dates[i]).close
                            s += s * history.dividend[div_dates[i]] / price
                        else:
                            # Unsupported transaction type
                            pass
                        shares[div_dates[i]] = s
                        i += 1
                        if i >= len(div_dates):
                            break
                # Process transaction
                if transactions.type == TransactionType.Shares:
                    s += transactions[k]
                elif transactions.type == TransactionType.Cash:
                    # TODO: Handle exceptions
                    price = history.get_latest(k).close
                    s += transactions[k] / price
                else:
                    # Unsupported transaction type
                    pass
                shares[k] = s

            # Calculate dividend after last transaction
            while i < len(div_dates):
                # Reinvest dividend
                if history.dividend.type == TransactionType.Shares:
                    s += s * history.dividend[div_dates[i]]
                elif history.dividend.type == TransactionType.Cash:
                    price = history.get_latest(div_dates[i]).close
                    s += s * history.dividend[div_dates[i]] / price
                else:
                    # Unsupported transaction type
                    pass
                shares[div_dates[i]] = s
                i += 1

        else:
            for k in sorted(transactions):
                if transactions.type == TransactionType.Shares:
                    s += transactions[k]
                elif transactions.type == TransactionType.Cash:
                    # TODO: Handle exceptions
                    price = history.get_latest(k).close
                    s += transactions[k] / price
                else:
                    # Unsupported transaction type
                    pass
                shares[k] = s
        return shares

    def calc_cost(self):
        self.cost = self._calc_cost(self.transactions, self.history)
        return self.cost

    @staticmethod
    def _calc_cost(transactions: TransactionHistory, history: StockHistory = None):
        cost = {min(transactions) - timedelta(1): 0}
        s = 0
        for k in sorted(transactions):
            if transactions.type == TransactionType.Shares:
                # TODO: Handle exceptions
                s += transactions[k] * history[k].close
            elif transactions.type == TransactionType.Cash:
                s += transactions[k]
            else:
                # Unsupported transaction type
                pass
            cost[k] = s
        return cost

    def calc_value(self):
        self.value = self._calc_value(self.shares, self.history)
        return self.value

    @staticmethod
    def _calc_value(shares, history: StockHistory, until: date = None):
        if until is None:
            until = max(history)
        value = {}
        date = min(shares)
        # s = 0
        for k in sorted(shares):
            while date < k:
                # TODO: Handle exceptions
                if s == 0:
                    value[date] = 0
                else:
                    if date in history:
                        value[date] = s * history[date].close
                date += timedelta(1)
            s = shares[k]
            value[k] = s * history.get_latest(k).close

        for d in [d for d in history if (d > date) and (d <= until)]:
            value[d] = s * history[d].close  # ordered()?
        return value

    def calc_gain(self):
        self.gain = self._calc_gain(self.value, self.cost)
        return self.gain

    @staticmethod
    def _calc_gain(value, cost):
        gain = {}
        date = max([min(value), min(cost)])
        # c = 0
        for k in sorted(cost):
            while date < k:
                if date in value:
                    gain[date] = value[date] - c
                date += timedelta(1)
            c = cost[k]
        if date in value:
            gain[date] = value[date] - c
        for d in [d for d in value if (d > date)]:
            gain[d] = value[d] - c
        return gain

    def calc_gainp(self):
        self.gainp = self._calc_gainp(self.gain, self.cost)
        return self.gainp

    @staticmethod
    def _calc_gainp(gain, cost):
        gainp = {}
        date = max([min(gain), min(cost)])
        c = 0
        for k in sorted(cost):
            if c != 0:
                while date < k:
                    if date in gain:
                        gainp[date] = gain[date] / c
                    date += timedelta(1)
            c = cost[k]
        if c != 0:
            if date in gain:
                gainp[date] = gain[date] / c
            for d in [d for d in gain if (d > date)]:
                gainp[d] = gain[d] / c
        return gainp

    def calc(self):
        self.calc_shares()
        self.calc_value()
        self.calc_cost()
        self.calc_gain()
        self.calc_gainp()
        self.calc_data()

    def output(self, output):
        csvwriter = csv.writer(output)

        print(file=output)
        print("---- Shares ----", file=output)
        csvwriter.writerow(["Date", "Shares"])
        csvwriter.writerows(sorted(self.shares.items()))

        print(file=output)
        print("---- Value ----", file=output)
        csvwriter.writerow(["Date", "Value"])
        csvwriter.writerows(sorted(self.value.items()))

        print(file=output)
        print("---- Cost ----", file=output)
        csvwriter.writerow(["Date", "Cost"])
        csvwriter.writerows(sorted(self.cost.items()))

        print(file=output)
        print("---- Gain ----", file=output)
        csvwriter.writerow(["Date", "Gain"])
        csvwriter.writerows(sorted(self.gain.items()))

        print(file=output)
        print("---- Gain (%) ----", file=output)
        csvwriter.writerow(["Date", "Gain (%)"])
        csvwriter.writerows(sorted(self.gainp.items()))

    def calc_data(self):
        self.data = OrderedDict(dict.fromkeys(sorted(self.value.keys())))
        for k in self.data.keys():
            self.data[k] = self._calc_data(k)

    def _calc_data(self, date):
        return Stock.StockData(self.get_shares(date), self.get_value(date), self.get_cost(date), self.get_gain(date),
                               self.get_gainp(date))

    def get_gainp(self, date):
        return Stock._get_latest(self.gainp, date)

    def get_gain(self, date):
        return Stock._get_latest(self.gain, date)

    def get_cost(self, date):
        return Stock._get_latest(self.cost, date)

    def get_value(self, date):
        return Stock._get_latest(self.value, date)

    def get_shares(self, date):
        return Stock._get_latest(self.shares, date)

    @staticmethod
    def _get_latest(d: dict, date: date):
        if date in d:
            return d[date]
        elif date > min(d.keys()):
            return d[max([d for d in d.keys() if d < date])]
        else:
            return None


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


class Portfolio:
    def __init__(self):
        super(Portfolio, self).__init__()
        self.cost = {date.min: 0}
        self.value = {date.min: 0}
        self.gain = {date.min: 0}
        self.gainp = {date.min: 0}


def parse_args():
    parser = argparse.ArgumentParser(description="TODO")
    parser.add_argument("transactions", help="File containing transaction data")
    parser.add_argument("history", nargs='?', default="history.txt",
                        help="File containing history data")
    parser.add_argument("dividend", nargs='?', help="File containing transaction data")
    parser.add_argument('-j', '--json', action="store_true",
                        help="History data is stored in JSON.")
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    return args


def main():
    # Parse arguments
    args = parse_args()

    if args.json:
        mode = DataMode.JSON
    else:
        mode = DataMode.CSV

    stock = Stock()
    stock.load_files(args.history, args.transactions, args.dividend, mode)
    stock.reinvest = True
    stock.calc()

    with open(args.output, 'w', newline='') if isinstance(args.output, str) else sys.stdout as out:
        stock.output(out)


if __name__ == "__main__":
    # execute only if run as a script
    print("Welcome to StockSim!")
    main()
