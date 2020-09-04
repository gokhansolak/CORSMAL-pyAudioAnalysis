import pandas as pd

if __name__ == '__main__':

    parser=argparse.ArgumentParser()

    parser.add_argument('-t', '--ftype', nargs='+', help='Filling type csv file.', required=True)
    parser.add_argument('-l', '--flevel', nargs='+', help='Filling level csv file.', required=True)
    parser.add_argument('-c', '--capacity', nargs='+', help='Filling capacity csv file.', required=True)
    parser.add_argument('-o', '--output', help='Name of the output file, w/o extension.', default='Submission_Form')

    args = parser.parse_args()

    df_sub = pd.read_csv('Submission_form.csv')

    df_comb = pd.concat(df_list)

    df_comb.to_csv(args.output+'.csv', index=False)
