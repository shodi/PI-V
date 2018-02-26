#!/usr/bin/python

class CSVObject:
    def __init__(self):
        headers = []
        data = []

    def set_headers(self, headers):
        self.headers = headers
    def process_line(self, line):
        self.data.push(line)
    def remove_null_columns(self, lines):
        null_qtty = {}
        line_qtty = 0
        for line in lines:
            for index, item in enumerate(line):
                if item is None:
                    if str(index) in null_qtty:
                        null_qtty[str(index)] += 1
                    else:
                         null_qtty[str(index)] = 0
            line_qtty += 1
        