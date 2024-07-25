"""
File: wildfires_api.py
Description: API for accessing data from the wildfires db
"""

import pandas as pd
import sqlite3


class WildfireAPI:
    con = None

    @staticmethod
    def connect(dbfile):
        """ make a connection """
        WildfireAPI.con = sqlite3.connect(dbfile, check_same_thread=False)

    @staticmethod
    def execute(query):
        return pd.read_sql_query(query, WildfireAPI.con)

    @staticmethod
    def get_state_list():
        query = "SELECT distinct STATE FROM Fires"
        df = WildfireAPI.execute(query)
        return list(df.STATE)

    @staticmethod
    def get_cause_list():
        query = "SELECT distinct STAT_CAUSE_DESCR FROM Fires"
        df = WildfireAPI.execute(query)
        return list(df.STAT_CAUSE_DESCR)

    @staticmethod
    def get_cause_count(state):
        """
      query to number of fires caused by a certain cause, should change based on the state selected in the dropdown
      """
        query = f"SELECT STAT_CAUSE_DESCR, COUNT(*) as count FROM Fires WHERE STATE = '{state}' GROUP BY STAT_CAUSE_DESCR"
        df = WildfireAPI.execute(query)
        return df['count'].tolist()

    @staticmethod
    def get_fire_data_by_state(state, year_range):
        """
        Query fire data based on state and year range.
        """
        year_min, year_max = year_range
        query = f"""SELECT FIRE_YEAR FROM Fires WHERE STATE = '{state}' AND FIRE_YEAR BETWEEN {year_min} AND {year_max}"""
        return WildfireAPI.execute(query)