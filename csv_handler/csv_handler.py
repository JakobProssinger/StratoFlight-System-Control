"""
@File:          csv_handler.py
@Descrption:    a module to handle csv writing
@Author:        Prossinger Jakob
@Date:          14 December 2021
@Todo:          * change prints to loggs
                * throw OSErrors insteed of standard excpetions
                * csv_write_header only if file is empty
                * test if csv does not exist
"""
import csv
import os
import logging


class CSV_HANDLER:
    def __init__(self, path: str) -> None:
        self.path = csv_handler_path

    def csv_write_data_row(self, data_list: list) -> None:
        try:
            with open(self.path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(data_list)
        except Exception as e:
            csv_module_logger.error(e)

    def csv_write_data_cell(self, data_cell: str) -> None:
        try:
            with open(self.path, 'a', newline='') as csvfile:
                csvfile.write(str(data_cell) + ';')
        except Exception as e:
            csv_module_logger.error(e)

    def csv_write_newline(self) -> None:
        try:
            with open(self.path, 'a', newline='') as csvfile:
                csvfile.write('\r')
        except Exception as e:
            csv_module_logger.error(e)
