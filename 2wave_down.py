from __future__ import print_function, absolute_import
from gm.api import *
from datetime import datetime
from fearquantlib.wavelib import compute_df_bar, is_macd_bar_reduce
import pandas as pd
import numpy as np
from fearquantlib import *

# 策略中必须有init方法

symbols="SHSE.600000"


frequency = [f"{5*60}s", f"{15*60}s", f"{60*60}s", f"1d"]

FREQ = frequency[3]

def init(context):
    subscribe(symbols='SHSE.600000', frequency=FREQ, count=30, wait_group=False)


def on_bar(context, bars):
    df = history_n(symbols, FREQ, count=40, end_time=bars[0]['eob'], fields="open,close,high,low,eob", skip_suspended=True,
              fill_missing=None, adjust=ADJUST_PREV,  df=True)
    df = compute_df_bar(df, **{"moutain_min_width":5})

    is_bar_reduce, tm = is_macd_bar_reduce(df, field='macd_bar', max_reduce_bar_distance=2, **{"moutain_min_width":5})
    if is_bar_reduce:
        print(f"{symbols} {tm}")

    #print(df.index)



if __name__ == '__main__':
    run(strategy_id='674c5423-39cb-11ea-b634-000c2910bf06',
        filename='2wave_down.py',
        mode=MODE_BACKTEST,
        token='5e18d749d600b7caa519c7caa4f09853aaa9deb2',
        backtest_start_time='2018-06-17 09:30:00',
        backtest_end_time='2020-01-22 15:00:00',
        serv_addr="gw.mkmerich.com:10088")
