from csv_handler import csv_handler
import datetime
import time


def main() -> None:
    i = 0
    while 1:
        data = [datetime.datetime.now(), i]
        handler.write_data_cell(data[0])
        handler.write_data_cell(data[1])
        i = + 1
        handler.write_newline()
        time.sleep(5)
        if i > 5:
            return


if __name__ == "__main__":
    handler = csv_handler.CSV_HANDLER("data\sensor_data.csv")
    headers = ["time", "Number"]
    # handler.write_data_row(headers)
    handler.write_data_cell(headers[0])
    handler.write_data_cell(headers[1])
    handler.write_newline()
    main()
