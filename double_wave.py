import sys

from fearquantlib.wavelib import *

config = QuantConfig()


def __compute_score_table(codes, time_delta):
    prepare_csv_data(codes, n_days=30, start_date="2019-07-01", end_date="2019-08-07",
                     timeUnitDelta=time_delta * timeConvTable['KL_60'])  # 如果让他返回落盘文件位置的从大周期到小周期的一个path list
    compute_df_bar(codes)  # 会打标波峰，波谷，连续红绿，ma5-10，

    all_info = []
    for code in codes:
        info = {"名称":code}
        for k in config.periods:
            fname = df_file_name(code, K_LINE_TYPE[k])
            df = pd.read_csv(fname, index_col=0)
            if k==KL_Period.KL_60:
                is_g_bar_reduce =  is_macd_bar_reduce(df, "macd_bar")
                info['时间'] = df.tail(1).iat[0, 1]
                info['60分缩短'] = "是" if is_g_bar_reduce  else "否"
            macd_wv_cnt = bar_green_wave_cnt(df, "macd_bar")
            ma_cnt = bar_green_wave_cnt(df, "em_bar")
            divergence_cnt = bottom_divergence_cnt(df, "macd_bar", "close")
            info[k] = { "macd波浪数":macd_wv_cnt, "均线波浪数":ma_cnt, "macd底背次数":divergence_cnt}

        all_info.append(info)

    print(json.dumps(all_info, indent=4, sort_keys=True, ensure_ascii=False))



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
