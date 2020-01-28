from __future__ import print_function, absolute_import
from gm.api import *
from datetime import datetime
from fearquantlib.wavelib import compute_df_bar, is_macd_bar_reduce, bar_green_wave_cnt
import pandas as pd
import numpy as np
from fearquantlib import *

# 策略中必须有init方法

symbols="SHSE.601988"


frequency = [f"{5*60}s", f"{15*60}s", f"{30*60}s",  f"{60*60}s", f"1d"]

FREQ_5 = frequency[0]
FREQ_15 = frequency[1]
FREQ_30 = frequency[2]
FREQ_60 = frequency[3]
FREQ_D = frequency[4]
FETCH_BATCH_SIZE=50

def init(context):
    subscribe(symbols=symbols, frequency=FREQ_60, count=FETCH_BATCH_SIZE, wait_group=False)


def on_bar(context, bars):
    df60 = history_n(symbols, FREQ_60, count=FETCH_BATCH_SIZE, end_time=bars[0]['eob'], fields="open,close,high,low,eob", skip_suspended=True,
                   fill_missing=None, adjust=ADJUST_PREV, df=True)
    df60 = compute_df_bar(df60, **{"moutain_min_width":5})
    macd_wave_60_cnt = bar_green_wave_cnt(df60, bar_field='macd_bar', start_time_key=None)
    ma_wave_60_cnt = bar_green_wave_cnt(df60, bar_field='em_bar', start_time_key=None)

    is_bigT_reduce, tm = is_macd_bar_reduce(df60, field='macd_bar', max_reduce_bar_distance=2, **{"moutain_min_width":5})
    if is_bigT_reduce: # 大变短
        # 小波数
        df30 = history_n(symbols, FREQ_30, count=FETCH_BATCH_SIZE, end_time=bars[0]['eob'], fields="open,close,high,low,eob",
                         skip_suspended=True,
                         fill_missing=None, adjust=ADJUST_PREV, df=True)
        df30 = compute_df_bar(df30, **{"moutain_min_width":5})
        macd_wave_cnt = bar_green_wave_cnt(df30, bar_field='macd_bar', start_time_key=None)
        ma_wave_cnt = bar_green_wave_cnt(df30, bar_field='em_bar', start_time_key=None)
        if macd_wave_cnt >1 or ma_wave_cnt > 1 or macd_wave_cnt >1 or ma_wave_60_cnt > 1:
            print(f"{symbols} {tm}  macd_wave_cnt_30={macd_wave_cnt}  ma_wave_cnt_30={ma_wave_cnt}  macd_wave_cnt_60={macd_wave_60_cnt}  ma_wave_cnt_60={ma_wave_60_cnt}")


if __name__ == '__main__':
    run(strategy_id='674c5423-39cb-11ea-b634-000c2910bf06',
        filename='2wave_down.py',
        mode=MODE_BACKTEST,
        token='5e18d749d600b7caa519c7caa4f09853aaa9deb2',
        backtest_start_time='2019-06-01 09:30:00',
        backtest_end_time='2020-01-22 15:00:00',
        serv_addr="localhost:7001")
