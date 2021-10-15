"""
----------------
REPORT GENERATOR
----------------

* Handles the generation of the report (html file).
* Contains a class 'HtmlReportContent' which contains methods for easy manipulation of the html file.
* ...

"""


import datetime
#from ... import ...


class HtmlReportContent(object):
    """Contains methods for easy manipulation of html file (report)"""

    def __init__(self):
        self.cnt = ""
        self.ind = 0

    def get_content(self):
        return self.cnt

    def write(self, data):
        """Inserts the given data (str) into the index point of the content (str).
        if Error: Returns 1
        Else: Returns 0"""
        if type(data) != str: return 1
        else:
            self.cnt = self.cnt[:self.ind] + data + self.cnt[self.ind:]
            self.ind += len(data)
            return 0

    def open_tag(self, tg_name, tg_class = "", tg_id = ""):
        """Inserts the given data (str) into the index point of the content (str).
        Index goes inbetween the tag's opening and closing tags.
        if Error: Returns 1 or 2 or 3
        Else: Returns 0"""
        if type(tg_name) != str: return 1
        elif type(tg_class) != str: return 2
        elif type(tg_id) != str: return 3
        else:
            if tg_class:
                if tg_id: self.write(f"<{tg_name} class = \"{tg_class}\" id = \"{tg_id}\">")
                else: self.write(f"<{tg_name} class = \"{tg_class}\">")
            else:
                if tg_id: self.write(f"<{tg_name} id = \"{tg_id}\">")
                else: self.write(f"<{tg_name}>")
            temp_ind = self.ind
            self.write(f"</{tg_name}>")
            self.ind = temp_ind
            return 0

    def go_front(self):
        """Moves the index after to the next closing tag.
        if Error: Returns 1
        Else: Returns 0"""

        temp_ind = self.ind
        check_1 = False
        check_2 = False
        while not(check_1 and check_2):
            try:
                if (self.cnt[temp_ind] == '<') and (self.cnt[temp_ind + 1] == '/'): check_1 = True
                elif check_1 and (self.cnt[temp_ind] == '>'): check_2 = True
            except IndexError: return 1
            temp_ind += 1
        self.ind = temp_ind
        return 0

    def go_back(self):
        """Moves the index before to the last opening tag.
        if Error: Returns 1
        Else: Returns 0"""

        temp_ind = self.ind
        check_1 = False
        check_2 = False
        while not(check_1 and check_2):
            try:
                if (self.cnt[temp_ind] == '>'): check_1 = True
                elif check_1 and (self.cnt[temp_ind - 1] == '<') and (self.cnt[temp_ind] != '/'):
                    check_2 = True
            except IndexError: return 1
            temp_ind -= 1
        self.ind = temp_ind
        return 0

    def go_into(self):
        """Moves the index after to the next opening tag.
        if Error: Returns 1
        Else: Returns 0"""

        temp_ind = self.ind
        check_1 = False
        check_2 = False
        while not(check_1 and check_2):
            try:
                if (self.cnt[temp_ind] == '<') and (self.cnt[temp_ind + 1] != '/'): check_1 = True
                elif check_1 and (self.cnt[temp_ind] == '>'): check_2 = True
            except IndexError: return 1
            temp_ind += 1
        self.ind = temp_ind
        return 0

    def generate(self):
        """Generates a report by writing the current content into an html file.
        The file name will be 'Report_<time-stamp>.html'."""

        # Generating time-stamp
        temp_ts = str(datetime.datetime.now())
        ts = ""
        for ele in temp_ts:
            if ele.isdigit(): ts += ele
            else: ts += '_'

        # Modifying time-stamp
        ts = ts[2:-3]           # removing first two digits of the year and last three digits of split seconds
        ts = ts.replace("_", "")# removing all the underscores

        # Generating report
        f_name = "Report_" + ts + ".html"
        with open(f_name, 'w') as f_h: f_h.write(self.cnt)


def generate_report(info):
    """Generates the HTML report for code metrics software based on the information given."""

    report_content = HtmlReportContent()
    insert_html_default_content(report_content)
    insert_consolidated_table(info, report_content)
    report_content.write("\n\n        <br><br>\n\n        ")
    insert_complete_table(info, report_content)
    report_content.generate()


def insert_consolidated_table(info, html_content):
    """Gets an HtmlReportContent and inserts a consolidated table.
    Leaves the cursor outside the closing tag of the table."""

    html_content.open_tag("table", "Consolidated")
    html_content.write("\n            ")
    html_content.open_tag("thead")
    html_content.write("\n                ")
    html_content.open_tag("tr")
    html_content.write("\n                    ")
    html_content.open_tag("th")
    html_content.write("Type of File")
    html_content.go_front()
    html_content.write("\n                    ")
    html_content.open_tag("th")
    html_content.write("Number of Files")
    html_content.go_front()
    html_content.write("\n                    ")
    html_content.open_tag("th")
    html_content.write("Number of Lines")
    html_content.go_front()
    html_content.write("\n                ")
    html_content.go_front()
    html_content.write("\n            ")
    html_content.go_front()
    html_content.write("\n            ")

    html_content.open_tag("tbody")
    for ext in info:
        html_content.write("\n                ")
        html_content.open_tag("tr")

        sum_lines = 0
        for file_name in info[ext]: sum_lines += info[ext][file_name]

        temp_info_lst = []
        temp_info_lst.append(ext[1:])
        temp_info_lst.append(str(len(info[ext])))
        temp_info_lst.append(str(sum_lines))
        for temp_info in temp_info_lst:
            html_content.write("\n                    ")
            html_content.open_tag("td")
            html_content.write(temp_info)
            html_content.go_front()

        html_content.write("\n                ")
        html_content.go_front()

    html_content.write("\n            ")
    html_content.go_front()
    html_content.write("\n        ")
    html_content.go_front()


def insert_complete_table(info, html_content):
    """Gets an HtmlReportContent and inserts a complete table.
    Leaves the cursor outside the closing tag of the table."""

    html_content.open_tag("table")
    html_content.write("\n            ")
    html_content.open_tag("thead")
    html_content.write("\n                ")
    html_content.open_tag("tr")
    html_content.write("\n                    ")
    html_content.open_tag("th")
    html_content.write("File Name")
    html_content.go_front()
    html_content.write("\n                    ")
    html_content.open_tag("th")
    html_content.write("Number of Lines")
    html_content.go_front()
    html_content.write("\n                ")
    html_content.go_front()
    html_content.write("\n            ")
    html_content.go_front()
    html_content.write("\n            ")

    html_content.open_tag("tbody")
    for ext in info:
        html_content.write("\n                ")
        html_content.open_tag("tr", "SubHeading")
        html_content.write("\n                    ")
        html_content.open_tag("td")
        html_content.write(ext[1:] + " Files")
        html_content.go_front()
        html_content.write("\n                    ")
        html_content.open_tag("td")
        html_content.go_front()
        html_content.write("\n                ")
        html_content.go_front()

        for file_info_pair in info[ext].items():
            html_content.write("\n                ")
            html_content.open_tag("tr")

            for file_info in file_info_pair:
                html_content.write("\n                    ")
                html_content.open_tag("td")
                html_content.write(str(file_info))
                html_content.go_front()

            html_content.write("\n                ")
            html_content.go_front()

    html_content.write("\n            ")
    html_content.go_front()
    html_content.write("\n        ")
    html_content.go_front()


def generate_error_report(error):
    """Generates an HTML error report for code metrics software based on the error string given."""

    report_content = HtmlReportContent()
    insert_html_default_content(report_content)
    report_content.open_tag("h4")
    report_content.write("Sorry, an error had occured:")
    report_content.go_front()
    report_content.write("\n        ")
    report_content.open_tag("h6")
    report_content.write(error)
    report_content.generate()


def insert_html_default_content(html_content):
    """Gets an HtmlReportContent and inserts default html tags and css styles.
    Leaves the cursor inside the 'body' block."""

    html_content.write("<!DOCTYPE html>\n\n")
    html_content.open_tag("html")
    html_content.write("\n\n    ")
    html_content.open_tag("head")
    html_content.write("\n\n        ")
    html_content.open_tag("title")
    html_content.write("Code Metrics Report")
    html_content.go_front()
    html_content.write("\n\n        ")
    html_content.open_tag("style")
    html_content.write(r'''
            h1 {
                font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
                text-align: center;
                color: blue;
            }
            h4 {
                font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
                color: red;
            }
            h6 {
                font-style: italic;
                color: red;
            }
            table {
                border: 2px solid black;
                border-collapse: collapse;
            }
            td, th {
                border: 2px solid black;
                padding: 3px;
                font-family: Arial, Helvetica, sans-serif;
                padding-left: 10px;
                padding-right: 10px;
            }
            .SubHeading > td {
                border: 0px solid black;
                background-color: rgb(216, 175, 255);
            }
            th {
                font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
                font-size: 20px;
                background-color: blueviolet;
                /*color: rgb(230, 230, 230);*/
                color: wheat;
                padding-left: 100px;
                padding-right: 100px;
            }
            .Consolidated th {
                background-color: orange;
                color: white;
                padding-left: 75px;
                padding-right: 75px;
            }
            .Consolidated td {
                background-color: rgb(255, 201, 100);
            }
        ''')
    html_content.go_front()
    html_content.write("\n\n    ")
    html_content.go_front()
    html_content.write("\n\n    ")
    html_content.open_tag("body")
    html_content.write("\n        <!-- NOTE: This is an auto-generated file -->\n\n        ")
    html_content.open_tag("h1")
    html_content.write("CODE METRICS REPORT")
    html_content.go_front()
    html_content.write("\n\n    ")
    html_content.go_front()
    html_content.write("\n\n")
    html_content.go_back()
    html_content.go_front()
    html_content.write("\n        <br>\n\n        ")


if __name__ == '__main__':
    print("\n\
NOT MEANT TO BE RUN\n\
\n\
This is just the module to generate the html report.\n\
Run 'code_metrics.py' to start the application.\n\
")


# END
