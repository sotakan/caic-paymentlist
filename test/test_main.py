# -*- coding: utf-8 -*-

import unittest
import pandas as pd
from datetime import datetime as dt
import main

class testMain(unittest.TestCase):
    def testImport_Syncable(self):
        exp = {
            "id": [2,4,5],
            "寄付日": [dt(2021,1,27,14,30), dt(2021,1,1,14,30), dt(2021,12,31,14,30)],
            "金額": [12000, 12000, 12000],
            "手数料": [660, 660, 660],
            "種別": ["年会費", "年会費", "年会費"],
            "寄付者ユニークID": [2, 4, 5],
            "氏名": ["テスト　太郎", "テスト　太郎", "テスト　太郎"]}

        expdf = pd.DataFrame(exp)

        raw = main.import_syncable("test/testsyncable.csv", 2021)
        ret = raw.to_dict("list")

        assert ret == exp