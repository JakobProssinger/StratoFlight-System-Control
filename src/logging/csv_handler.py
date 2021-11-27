import csv
from os import write

class CSV_HANDLER:

    def __init__(self, csv_handler_directory: str, header_list: list) -> None:
        self.directory = csv_handler_directory
        self.header_list = header_list

    def csv_write_header(self) -> None:
        try:
            with open(self.directory, 'w', newline = '') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(self.header_list)
        except Exception as e:
            print(e)

    def csv_write_data_row(self, data_list: list) -> None:
        try:
            with open(self.directory, 'a', newline = '') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(data_list)
        except Exception as e:
            print(e)
    
    def csv_write_data_cell(self, data_cell: float) -> None:
        try:
            with open(self.directory, 'a', newline='') as csvfile:
                csvfile.write(str(data_cell) + ',')
        except Exception as e:
            print(e)


    def csv_write_newline(self) -> None:
        try:
            with open(self.directory, 'a', newline = '') as csvfile:
                csvfile.write('\r')
        except Exception as e:
            print(e)
