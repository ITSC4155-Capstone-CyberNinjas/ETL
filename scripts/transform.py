# transform.py

"""
This script performs transformation of the raw wifi logs into a tabular and structured format.
The transformation is largely an aggregation of counts of association success logs that is grouped
by building. Outliers are also removed based on z-score. Key packages used are pandas, regex, and
multiprocessing. Depending on the size of the file, the transformation typically takes from 20 seconds 
to 2 minutes to complete a file. This script will output each file as a .csv. Database ingestion
will be hangled by another script.
"""


import re
import os
import logging
import time  
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, date
from multiprocessing import Pool


class WifiLogTransformer:
    
    def __init__(self, file_path: str, date: datetime.date):
        self.file_path = Path(file_path)
        self.date = date
        self.file_name = file_path[-23:]
        self.log_df = None
        self.logs_array = None
        
        
    def read_and_filter_log(self, logs_of_interest: list = ['<501100>'] ):
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

        Assigns:
            log_array (List): 2d list of logs with timestamp separated into its own column

                                [ [{datetime 1}, {log contents 1}],
                                  [{datetime 2}, {log contents 2}],
                                    . . .
                                  [{datetime n}, {log contents n}] ]

        """

        def format_timestamp( timestamp: str ):
            """
            Given a timestamp from a log record, parse the
            string and create datetime object

            Parameters:
                timestamp (str): Raw string representation of timestamp from the log record

            Returns:
                datetime (datetime.datetime): Python datetime object 
            """

            dt = timestamp.split(' ')
            time = dt[-1].split(':')

            return datetime(
                year = self.date.year,
                month = self.date.month,
                day = self.date.day,
                hour = int( time[0] ),
                minute = int( time[1] ),
                second = int( time[2] )
            )
            

        logs_array = []        

        with open(self.file_path, 'r') as file:
            for line in file:
                for code in logs_of_interest:
                    if code in line:
                        timestamp = format_timestamp( line[:15] )
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


############################################################
#####                 Driver c:                        #####
############################################################

if __name__  == "__main__":

    DATA_PATH = Path("/media/calvinhathcock/Secondary SSD/ITSC_4155_Capstone/dataset/raw/wifi/var/log/remote/wireless-encoded")
    DEST_PATH = Path("/home/calvinhathcock/Documents/College/UNCC/Fall 2022/ITSC 4155/Project/transformed_data")
    LOG_PATH = Path("/home/calvinhathcock/Documents/College/UNCC/Fall 2022/ITSC 4155/Project/transformation_logs")
    
    logging.basicConfig(filename= LOG_PATH / Path('transformation.log'), encoding='utf-8', level=logging.INFO)


    def execute_transformer(file_path):

        logging.info(f'BEGINNING transformation of file: {file_path}')

        # append file to path
        file = DATA_PATH / file_path

        # format date
        date_str = str(file_path[-14:-4])
        date_array = [int(x) for x in date_str.split('-')]
        curr_date = date(date_array[2], date_array[0], date_array[1])
        
        # initialize and execute transformer
        try:
            logging.info(f'Initialzied transformer for: {file_path}')
            transformer = WifiLogTransformer(file_path, curr_date)

            logging.info(f'Read data for: {file_path}')
            transformer.read_and_filter_log()

            logging.info(f'Clean data for: {file_path}')
            transformer.clean_log()

            logging.info(f'Aggregating data for: {file_path}')
            transformer.aggregate_data()

        except:
            logging.error(f'FAILED transformation of file: {file_path}')
            logging.exception('')
            
            return

        # write file to disk
        transformer.logs_df.to_csv( DEST_PATH / Path("counts_" + transformer.file_name[:-4] + ".csv"), index=False)

        logging.info(f'FINISHED transformation of file: {file_path}')

    
    starttime = time.time()

    logging.info(f'Beginning transformation process at {starttime}')

    os.chdir(DATA_PATH)

    files = os.listdir(DATA_PATH)

    logging.info(f'Files to be transformed: {files}')

    pool = Pool()
    pool.map(execute_transformer, files)
    pool.close()

    endtime = time.time()

    logging.info(f'Finishing transformation process at {endtime}')
