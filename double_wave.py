from fearquantlib.wavelib import *
import sys

if __name__=="__main__":
    if len(sys.argv)>2:
        file = sys.argv[2]
        if not file:
            print(f"代码文件没有找到")
            exit(0)
    else:
        print(f"Usage:\n$python3  /path/to/config.json  stock_list.txt\n\n")
        exit(0)

    with open(file, 'r', encoding='utf-8') as f:
        codes = f.readlines()

    prepare_csv_data(codes, n_days=30, timeUnitDelta=-3*timeConvTable['KL_60'])   # 如果让他返回落盘文件位置的从大周期到小周期的一个path list
    compute_df_bar(codes) # 会打标波峰，波谷，连续红绿，ma5-10，
    fname = df_file_name(codes[0], K_LINE_TYPE[KL_Period.KL_60])
    df60 = pd.read_csv(fname, index_col=0)
    if is_macd_bar_reduce(df60, "macd_bar"):
        pass
    # 计算各项得分


