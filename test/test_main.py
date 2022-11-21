# -*- coding: utf-8 -*-

import unittest
import pandas as pd
import main
import os

from google.oauth2.credentials import Credentials


class testMain(unittest.TestCase):
    def testImport_Syncable(self):
        exp = {
            "id": [2, 4, 5],
            "寄付日": [pd.Timestamp(2021, 1, 27, 14, 30), pd.Timestamp(2021, 1, 1, 14, 30), pd.Timestamp(2021, 12, 31, 14, 30)],
            "金額": [12000, 12000, 12000],
            "手数料": [660, 660, 660],
            "種別": ["年会費", "年会費", "年会費"],
            "寄付者ユニークID": [2, 4, 5],
            "氏名": ["テスト　太郎", "テスト　太郎", "テスト　太郎"]}

        raw = main.import_syncable("test/testsyncable.csv", 2021)
        ret = raw.to_dict("list")

        self.assertEqual(exp, ret)

    def testImport_sbi(self):
        exp = {
            "日付": [pd.Timestamp(2022, 10, 21), pd.Timestamp(2022, 10, 16), pd.Timestamp(2022, 10, 12)],
            "内容": ["振込＊テスト　タロウジュニア", "利息", "振込＊テスト　タロウシニア"],
            "出金金額(円)": [0, 0, 0],
            "入金金額(円)": ["17,000", "2", "17,000"],
            "残高(円)": ["3,018,066", "3,001,066", "3,001,064"],
            "メモ": ["-", "-", "-"]}

        raw = main.import_sbi("test/testsbi.csv")
        ret = raw.to_dict("list")

        self.assertEqual(ret, exp)

    def testImport_member(self):

        if os.environ.get("CI") == "true":
            creds = Credentials(token=os.environ.get("CI_TOKEN"), refresh_token=os.environ.get("CI_REFRESH_TOKEN"), token_uri=os.environ.get("CI_TOKEN_URI"), client_id=os.environ.get("CI_CLIENT_ID"), client_secret=os.environ.get("CI_CLIENT_SECRET"), scopes= [os.environ.get("CI_SCOPES")])
        else:
            os.environ["CAIC_PAYMENTLIST_CREDPATH"]="creds"
            creds = main.auth_google()

        os.environ["CAIC_PAYMENTLIST_SHEETID"]="1TkDu5TI5T7aPuhVVGAF4XhBtGEDEPVspmqkSJSv-bkI"
        os.environ["CAIC_PAYMENTLIST_SHEETRANGE"]="会費確認!A:C"
        
        exp=["会員種別", "氏名", "口座名義"]
        ret=main.import_members(creds)

        self.assertEqual(exp, ret[0])