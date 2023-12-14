import csv

file_path = 'feeds.csv'

# Assuming your data is stored in a file named 'data.csv'
def read_data(file_path):
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            print(row)


if __name__ == "__main__":

    read_data(file_path)