"""
@File:          csv_handler.py
@Descrption:    a module to handle csv writing
@Author:        Prossinger Jakob
@Date:          25 January 2022
@Todo:          * change prints to loggs
"""
import csv
import os
import logging


class CSV_HANDLER:
    """
    class to handle csv writing
    """

    def __init__(self, path: str) -> None:
        """
        init function of the CSV_HANDLER class

        Args:
            path (str): path to the csv-file write
        """
        self.path = path
        if os.path.exists(path) is False:
            with open(path, 'w') as f:
                f.write('')

    def csv_write_list(self, data_list: list) -> None:
        """
        write a list of data to the csv-file with no newline

        Args:
            data_list (list): list of data to write to the csv-file
        """
        try:
            with open(self.path, 'a', newline='') as csvfile:
                for data_point in data_list:
                    csvfile.write(str(data_point) + ';')
        except OSError:
            print(OSError)
        except Exception as e:
            print(e)

    def csv_write_data_row(self, data_list: list) -> None:
        """
        write a list of data to the csv-file with newline

        Args:
            data_list (list): list of data to write to the csv-file
        """
        try:
            with open(self.path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(data_list)
        except OSError:
            print(OSError)
        except Exception as e:
            print(e)

    def csv_write_data_cell(self, data_cell: str) -> None:
        """
        write single element to the csv-file

        Args:
            data_cell (str): data to write
        """
        try:
            with open(self.path, 'a', newline='') as csvfile:
                csvfile.write(str(data_cell) + ';')
        except OSError:
            print(OSError)
        except Exception as e:
            print(e)

    def csv_write_newline(self) -> None:
        """
        write a newline symbol to the csv-file
        """
        try:
            with open(self.path, 'a', newline='') as csvfile:
                csvfile.write('\r')
        except OSError:
            print(OSError)
        except Exception as e:
            print(e)
