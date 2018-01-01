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

from stocksim import *
# from os import path

def main():
    ss = StockSim()

    # Open history
    with open("history.txt") as file:
        # Load history
        data = file.read()
        ss.stocks[0].history.load(data)
    # for i in sorted(ss.stocks[0].history.items()):
    #     print(i)

    # Open transactions
    with open("transactions2.csv") as file:
        # Load transactions
        data = file.read()
        ss.stocks[0].transactions.load(data)
    # for i in sorted(ss.stocks[0].transactions.items()):
    #     print(i)

    # Calculate shares
    print()
    print("---- Shares ----")
    ss.stocks[0].calc_shares()
    for i in sorted(ss.stocks[0].shares.items()):
        print(i)

    # Calculate value
    print()
    print("---- Value ----")
    ss.stocks[0].calc_value()
    for i in sorted(ss.stocks[0].value.items()):
        print(i)

    # Calculate cost
    print()
    print("---- Cost ----")
    ss.stocks[0].calc_cost()
    for i in sorted(ss.stocks[0].cost.items()):
        print(i)

    # Calculate gain
    print()
    print("---- Gain ----")
    ss.stocks[0].calc_gain()
    for i in sorted(ss.stocks[0].gain.items()):
        print(i)

    # Calculate gain ratio
    print()
    print("---- Gain (%) ----")
    ss.stocks[0].calc_gainp()
    for i in sorted(ss.stocks[0].gainp.items()):
        print(i)

    # Test StockSimGui
    # TODO


if __name__ == "__main__":
    # execute only if run as a script
    main()
