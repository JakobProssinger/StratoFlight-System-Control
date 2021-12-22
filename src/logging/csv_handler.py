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

csv_module_logger = logging.getLogger("strato_logger.sensor_process.ds18b20")


class CSVHandler:
    """
    A class used to Handle csv file writing and formatting 

    ...

    Attributes
    ----------
    csv_handler_directory : str
        the path of csv file which will be writen in 
    header_list : list
        a list of strings headers for the first column 

    Methods
    -------
    csv_write_header(self)
        write the header column to the csv file
    
    csv_write_data_row(self, data_list: list)
        appends a row to the csv file and goes to new line

    csv_write_data_cell(self, data_cell: float)
        appends a cell to the csv file. No new line included 

    csv_write_newline(self)
        appends a new line character to the csv file
    """
    def __init__(self, csv_handler_directory: str, header_list: list) -> None:
        """
        Parameters
        ----------
        csv_handler_directory : str
            the path of csv file which will be writen in 
        header_list : list
            a list of strings headers for the first row 
        """

        self.directory = csv_handler_directory
        self.header_list = header_list

    def csv_write_header(self) -> None:
        """
        Writes a the header_list in first row 

        Throws
        ------
        Exception
            if csv couldnt be opened or be writen
        """
        if os.stat(self.directory).st_size != 0:
            print("file empty")
            return

        try:
            with open(self.directory, 'w', newline='',
                      delimiter=';') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(self.header_list)
        except Exception as e:
            csv_module_logger.error(e)

    def csv_write_data_row(self, data_list: list) -> None:
        """
        appends a list, as a new row, to a csv file and adds a new line char
        
        Parameters
        ----------
        data_list: list
            of data elements which will be appended 

        Throws
        ------
        Exception
            if csv couldnt be opened or be writen
        """
        try:
            with open(self.directory, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(data_list)
        except Exception as e:
            csv_module_logger.error(e)

    def csv_write_data_cell(self, data_cell: float) -> None:
        """
        appends a float, as a new cell, to a csv file.
        
        Parameters
        ----------
        data_cell: float
            data element to append

        Throws
        ------
        Exception
            if csv couldnt be opened or be writen
        """
        try:
            with open(self.directory, 'a', newline='') as csvfile:
                csvfile.write(str(data_cell) + ';')
        except Exception as e:
            csv_module_logger.error(e)

    def csv_write_newline(self) -> None:
        """
        appends a newline char to the csv file.

        Throws
        ------
        Exception
            if csv couldnt be opened or be writen
        """
        try:
            with open(self.directory, 'a', newline='') as csvfile:
                csvfile.write('\r')
        except Exception as e:
            csv_module_logger.error(e)