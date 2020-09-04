import pandas as pd
import argparse, os

if __name__ == '__main__':

    parser=argparse.ArgumentParser()

    parser.add_argument('-f', '--files', nargs='+', help='List of space separated file paths.', required=True)
    parser.add_argument('-o', '--output', help='Name of the output file, w/o extension.', default='combined')

    args = parser.parse_args()

    df_list = []
    for f in args.files:
        df_list.append(pd.read_csv(f))

    df_comb = pd.concat(df_list)

    df_comb.to_csv(args.output+'.csv', index=False)
