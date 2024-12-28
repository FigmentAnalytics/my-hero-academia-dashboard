import pandas as pd

def main():
    # Read the CSV with 'id' as string
    df = pd.read_csv('../data/characters.csv', dtype={'id': str})
    # Print the data types of each column
    print(df.dtypes)

if __name__ == "__main__":
    main()
