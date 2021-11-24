import csv
from os import write

class CSV_HANDLER:

    def __init__(self, csv_handler_directory, header_list):
        self.directory = csv_handler_directory
        self.header_list = header_list
        self.csv_file_row = 1                            #csv row to write in next

    def csv_write_header(self):
        try:
            with open(self.directory, 'w+', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(self.header_list)
                self.csv_file_row += 1
                csvfile.close()
        except Exception as e:
            print(e)

    def csv_write_data_row(self, data_list):
        try:
            with open(self.directory, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(data_list)
                csvfile.close()
        except Exception as e:
            print(e)
    
    def csv_write_data_cell(self, data_cell):
        try:
            with open(self.directory, 'a', newline='') as csvfile:
                csvfile.write(str(data_cell) + ',')
                csvfile.close()
        except Exception as e:
            print(e)
