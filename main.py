# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime as dt
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os

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

# Get sheeets member info
def import_members():
    scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    try:
        spreadsheetid = os.environ["CAIC_PAYMENTLIST_SHEETID"]
        sheetrange = os.environ["CAIC_PAYMENTLIST_SHEETRANGE"]
        credpath = os.environ["CAIC_PAYMENTLIST_CREDPATH"]
    except KeyError:
        raise Exception("Environment variables not set")

    creds = None
    if os.path.exists(f'{credpath}/token.json'):
        creds = Credentials.from_authorized_user_file(f'{credpath}/token.json', scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                f'{credpath}/credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(f'{credpath}/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build("sheets", "v4", credentials=creds)
    sheets = service.spreadsheets()

    ret = sheets.values().get(spreadsheetId=spreadsheetid, range=sheetrange).execute()

    return ret.get("values",[])