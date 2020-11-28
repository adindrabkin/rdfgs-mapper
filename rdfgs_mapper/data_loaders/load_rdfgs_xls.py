"""
loader for the RDFGS survey
"""

import xlrd
from rdfgs_mapper import cfg


class Rdfgs_Xl:
    dfs = None
    book = None
    # Shouldn't be hard coded
    headers = {0: "City", 1: "County", 2: "LSR", 3: "POP", 4: "QT", 5: "I/O", 6: "X", 7: "K", 8: "KA", 9: "TSR",
               10: "Notes"}

    def __init__(self):
        self.book = xlrd.open_workbook(cfg.DATA.RDFGS, formatting_info=True)
        # normalizing state names by joining them in lower case
        # {northdakota: <xlrd.sheet.Sheet>}
        self.dfs = {cfg.STATE_ABBREV[sheetname]: self.book.sheet_by_name(sheetname) for sheetname in
                    self.book.sheet_names()}

    def get_state(self, state_abbr):
        """
        get city/county data for a state -- NO ERROR CHECKING
        :param state_abbr: state abbreviation (i.e CA)
        :return: sheet for that state
        """
        return self.dfs[state_abbr]


    def get_state_police(self, state_abbr):
        """
        get the police info of :state:
        :param state_abbr: state abbreviation
        :return: {LSR: Bool, POP: Bool, ... , Notes: ""}
        """
        st = self.get_state(state_abbr)
        rowidx = self.find_row(st, "State Police")
        row_info = self.get_row_info(st, rowidx)
        return row_info

    def get_state_counties(self, state_abbr, county_names):
        """
        get all matching counties for each state
        :param state_abbr: the abbr of the state (i.e CA)
        :param county_names: the county name(s), list/str. Do not include " County" at the end
        :return: {county_name: {LSR: Bool, POP: Bool, ... , Notes: ""}}
        """
        county_row_info = {}
        st = self.get_state(state_abbr)
        for county in list(county_names):
            county += " County"  # adding " County" to the end
            rowidx = self.find_row(st, county)
            row_info = self.get_row_info(st, rowidx)
            county_row_info[county] = row_info
        return county_row_info


    def cell_is_marked(self, bgx_color):
        """
        return true if bgx_color (background color) is not 22
        """
        # 22 is the gray background
        if bgx_color != 22:
            return True

    def get_row_info(self, sheet, rowidx):
        """
        Get :rowidx: from :sheet:. sheet[rowidx] should follow self.headers
        :param sheet: xlrd sheet
        :param rowidx: row index
        :return:
        """
        row_info = {}
        if rowidx is None:  # handling where nothing is found
            row_info = {self.headers[i]: "unk" for i in range(2, 10)}
            row_info["notes"] = ""
            return row_info
        for i in range(2, 10):  # boxs of LSR to TSR
            xfx = sheet.cell_xf_index(rowidx, i)

            # getting the background color
            xf = self.book.xf_list[xfx]
            bgx = xf.background.pattern_colour_index
            if self.cell_is_marked(bgx):
                row_info[self.headers[i]] = True
            else:
                row_info[self.headers[i]] = False
        row_info["notes"] = sheet.cell(rowidx, 10).value
        return row_info

    def find_row(self, sheet, row_str, colid=0):
        """
        find the first row of a sheet matching row_str
        :param sheet: sheet to search
        :param row_str: desired value in the row
        :param colidx: desired column to check, default is 0
        :return: columnid (0), rowid of the match value
        """
        for rowidx in range(sheet.nrows):
            if sheet.cell_value(rowidx, colid) == row_str:
                return rowidx
