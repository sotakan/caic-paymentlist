# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime as dt

# Filters by date and tx type
def import_syncable(syncablecsv, year):
    raw = pd.read_csv(syncablecsv, parse_dates = ["寄付日"])

    # Select rows with matching start date and payment is a subscription
    start_matching = raw.loc[(raw["寄付日"] >= dt(year,1,1)) & (raw["種別"] == "年会費")]

    # Return rows with end date
    return start_matching.loc[(start_matching["寄付日"] < dt(year+1,1,1)) & (start_matching["種別"] == "年会費")]

# Filters by tx deposit
def import_sbi(sbicsv):
    raw = pd.read_csv(sbicsv, parse_dates = ["日付"], encoding = "shift-jis")

    deposits =raw.dropna(subset = "入金金額(円)")

    return deposits.fillna(0)