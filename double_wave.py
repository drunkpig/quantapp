from fearquantlib.wavelib import *

config = QuantConfig()


def __compute_score_table(codes, time_delta):
    is_ok = prepare_csv_data_tdx(codes, n_days=30, start_date="2019-07-01", end_date="2019-08-07",
                             timeUnitDelta=time_delta * timeConvTable['KL_60'])  # 如果让他返回落盘文件位置的从大周期到小周期的一个path list
    if is_ok is None:
        print("获取数据错误")
        exit(1)
    compute_df_bar(codes)  # 会打标波峰，波谷，连续红绿，ma5-10，

    all_info = []
    for code in codes:
        info = {"stock_code": code}
        green_start_time_key = None
        for k in config.periods:
            fname = df_file_name(code, k)
            df = pd.read_csv(fname, index_col=0)
            if k == KL_Period.KL_60:
                is_g_bar_reduce, green_start_time_key = is_macd_bar_reduce(df, "macd_bar", max_reduce_bar_distance=3)
                info['time'] = df.tail(1).iat[0, 1]
                info['is_macd_bar_60_reduce'] = "Y" if is_g_bar_reduce else "N"
            #green_start_time_key = None
            macd_wv_cnt = bar_green_wave_cnt(df, "macd_bar", start_time_key=green_start_time_key)
            # ma_cnt1 = bar_green_wave_cnt(df, "em_bar", start_time_key=None)
            ma_cnt = bar_green_wave_cnt(df, "em_bar", start_time_key=green_start_time_key)
            # divergence_cnt1 = bottom_divergence_cnt(df, "macd_bar", "close", start_time_key=None)
            divergence_cnt = bottom_divergence_cnt(df, "macd_bar", "close", start_time_key=green_start_time_key)
            ma_distance = get_current_ma_distance(df)

            info.update({f"{k}_macd_wave_cnt": macd_wv_cnt, f"{k}_ema_wave_cnt": ma_cnt,
                         f"{k}_macd_bottom_divergence_cnt": divergence_cnt, f"{k}_em_5_10_distance": ma_distance})

        df60 = pd.read_csv(df_file_name(code, KL_Period.KL_60), index_col=0)
        df30 = pd.read_csv(df_file_name(code, KL_Period.KL_30), index_col=0)
        df15 = pd.read_csv(df_file_name(code, KL_Period.KL_15), index_col=0)
        # 60~30, 60~15 macd共振
        # 30~15 macd共振
        macd_60_30 = resonance_cnt(df60, df30, "macd_bar", start_time_key=green_start_time_key)
        macd_60_15 = resonance_cnt(df60, df15, "macd_bar", start_time_key=green_start_time_key)
        macd_30_15 = resonance_cnt(df30, df15, "macd_bar", start_time_key=green_start_time_key)
        # 60~30， 60~15 均线共振
        # 30~15 均线共振
        em_60_30 = resonance_cnt(df60, df30, "em_bar", start_time_key=green_start_time_key)
        em_60_151 = resonance_cnt(df60, df15, "em_bar", start_time_key=None)
        em_60_15 = resonance_cnt(df60, df15, "em_bar", start_time_key=green_start_time_key)
        em_30_15 = resonance_cnt(df30, df15, "em_bar", start_time_key=green_start_time_key)
        resonance = "resonance"
        info.update({f"{resonance}_macd_60_30": macd_60_30, f"{resonance}_macd_60_15": macd_60_15,
                     f"{resonance}_macd_30_15": macd_30_15, \
                     f"{resonance}_em_60_30": em_60_30, f"{resonance}_em_60_15": em_60_15,
                     f"{resonance}_em_30_15": em_30_15, })

        all_info.append(info)
    df = pd.DataFrame(all_info)
    print(json.dumps(all_info, indent=4, sort_keys=True, ensure_ascii=False))
    return df


def __wave_cnt(df):
    """
    macd, ma的各周期波数目  # TODO 波数目的计算还存在一定问题，小周期的波数目应该从大周期绿波开始点算起
    :return:
    """


def __bottom_divergence_cnt(df):
    pass


def __ma_distance(df):
    pass


def __resonace_cnt(df):
    pass


if __name__ == "__main__":
    if len(sys.argv) > 2:
        file = sys.argv[2]
        if not file:
            print(f"代码文件没有找到")
            exit(0)
    else:
        print(f"Usage:\n$python3  /path/to/config.json  stock_list.txt\n\n")
        exit(0)

    with open(file, 'r', encoding='utf-8') as f:
        codes = f.readlines()

    for i in [-7, -6, -5, -4, -3, -2, -1, 0]:
        __compute_score_table(codes, i)

    # for date in range(2,2222):
    #     df = __compute_score_table(codes, 0)
    #     # TODO 保存并最后打印靠谱的点
