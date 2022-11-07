# transform.py
import re
import os
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, date

class WifiLogTransformer:
    
    def __init__(self, file_path: str, date: datetime.date):
        self.file_path = Path(file_path)
        self.date = date
        self.file_name = file_path[-23:]
        self.log_df = None
        self.logs_array = None
        
        
    def read_and_filter_log(self, logs_of_interest: list = ['<501100> <1918>'] ):
        """ 
        Given a raw log file path, read file and filter for logs of interest
        based on the codes:
                association request - '<501095>' 
                association success - '<501100>' 
                auth success - '<501093>' 
                deauth1 - '<501080>' 
                deauth2 - '<501105>' 
                deauth3 - '<501106>' 
        Convert timestamp to Python datetime object. 


        Parameters:
            log_file_path (str): absolute file path of log file 
            logs_of_interest (list): List of strings that represent the different codes in the log file. 
                                     Will be used to check for matches in each line. 

        Returns:
            log_array (List): 2d list of logs with timestamp separated into its own column

                                [ [{datetime 1}, {log contents 1}],
                                  [{datetime 2}, {log contents 2}],
                                    . . .
                                  [{datetime n}, {log contents n}] ]

        """
    
        month_dict = {
            'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6,
            'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12
        }

        def format_timestamp( timestamp: str, year: int ):
            """
            Given a timestamp from a log record, parse the
            string and create datetime object

            Parameters:
                timestamp (str): Raw string representation of timestamp from the log record
                year (int): year value from log file name (year is not included in time stamp)

            Returns:
                datetime (datetime.datetime): Python datetime object 
            """

            dt = timestamp.split(' ')
            time = dt[2].split(':')

            return datetime(
                year = year,
                month = month_dict[ dt[0] ],
                day = int( dt[1] ),
                hour = int( time[0] ),
                minute = int( time[1] ),
                second = int( time[2] )
            )


        logs_array = []
        #year = int( str(log_file_path)[-8:-4] ) #extract year from file name
        

        with open(self.file_path, 'r') as file:
            for line in file:
                for code in logs_of_interest:
                    if code in line:
                        timestamp = format_timestamp( line[:15], self.date.year )
                        log = line[16:-1] #remove newline escape
                        logs_array.append( [timestamp, log] ) 
                        break 

        self.logs_array = logs_array


    def clean_log(self, z_threshold: float = 2.5): 
        """
        Convert log array to DataFrame and remove outliers 
        based on unique mac addresses

        Parameters:
            z_threshold (float): z score threshold for removing outliers
        """

        def get_outliers(count_dict: dict, z_threshold: float):
            """ 
            Given a dictionary containing the total occurrence count of each mac,
            calculate z scores for each mac address and return list of outlier mac addresses .

            Parameters:
                count_dict (dict): Dictionary of mac_address-count pairs
                z_threshold (float): Z score threshold for removing outliers

            Returns:
                outliers (list): list of mac addresses that are outliers
            """
            mac_counts = pd.Series(count_dict)
            mean = mac_counts.mean()
            std = mac_counts.std()
            z = mac_counts.apply( lambda x: (x - mean) / std )
            abs_z = np.abs(z)
            outlier_locs = np.where(abs_z > z_threshold)
            outliers = mac_counts.iloc[outlier_locs].index

            return list(outliers)


        pattern = re.compile(r'([0-9a-f]{2}(?::[0-9a-f]{2}){5})', re.IGNORECASE)
        count_dict = dict()
        log_index_cache = dict()

        # count occurences and store indices for each mac address  
        for idx, log in enumerate(self.logs_array):

            # detect mac address from regex pattern
            macs = re.findall(pattern, log[1])

            if count_dict.get( macs[0] ) is None:
                count_dict[ macs[0] ] = 1
                log_index_cache[ macs[0] ] = [idx]
            else:
                count_dict[ macs[0] ] += 1
                log_index_cache[ macs[0] ].append(idx)

        #get list of outliers
        outliers = get_outliers(count_dict, z_threshold)

        #unpack indices for each outlier
        indices = []
        for o in outliers:
            for idx in log_index_cache[o]:
                indices.append(idx)

        #convert to dataframe and drop outliers by index 
        logs_df = pd.DataFrame(self.logs_array, columns = ['timestamp', 'log']).drop(index = indices)

        self.logs_df = logs_df


    def aggregate_data(self):
    	"""
		Format the log dataframe so that it can be aggregated
    	"""

        def get_building_codes(log: str):
        	"""
        	Given a log, extract the building code using regex 
        	"""
            pattern1 = re.compile('EXT-[a-zA-Z]{4}')
            pattern2 = re.compile(r'([0-9a-f]{2}(?::[0-9a-f]{2}){5}-[a-zA-Z]{4})', re.IGNORECASE)

            building1 = re.findall(pattern1, log)
            building2 = re.findall(pattern2, log)

            if len(building1) > 0:
                return building1[0][-4:]
            if len(building2) > 0:
                return building2[0][-4:]
            return None


        # Format columns 
        self.logs_df['hour'] = self.logs_df.timestamp.dt.hour
        self.logs_df['building'] = self.logs_df['log'].apply(get_building_codes)

        # group by hour and building
        grouped_df = self.logs_df.groupby(['building', 'hour'], as_index=False).count()

        # Format columns 
        grouped_df['count'] = grouped_df['timestamp']
        grouped_df['timestamp'] = grouped_df['hour'].apply( lambda x: datetime(year = self.date.year, month = self.date.month, day = self.date.day, hour = x))
        grouped_df = grouped_df.drop(columns=['log', 'hour'])
        grouped_df = grouped_df.reindex(columns = ['timestamp', 'count', 'building'])

        self.logs_df = grouped_df 


