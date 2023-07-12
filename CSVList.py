import csv


# Blueprint for CSVList objects.
class CSVList:
    def __init__(self):
        self.list = []

    # Opens, reads, and adds list to self.list
    def add_list(self, csv_file_path):
        with open(csv_file_path) as csv_file:
            csv_data = csv.reader(csv_file)
            self.list = list(csv_data)

    # Retrieves cell value from csv list
    # O(1)time --- O(1)space
    def get_x_y(self, x, y):
        value = self.list[x][y]
        if value == '':
            value = self.list[y][x]
        return float(value)

    # Retrieves id from csv list
    # O(N)time --- O(1)space
    def get_csv_id(self, string):
        for record in self.list:
            if string in record[2]:
                return int(record[0])
