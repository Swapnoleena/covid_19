#!/usr/bin/env python3

# This script creates a new sqlite database based on the CSV is reiceives as an argument
# The sqlite database is used as an intermediate step to merge new data in existing CSVs

import sqlite3
import traceback
import os
import sys
import db_common as dc


__location__ = dc.get_location()

try:
    # load the csv to sqlite db
    assert len(sys.argv) == 2, "Call script with CSV file as parameter"
    columns, to_db = dc.load_csv(sys.argv[1])

    # create db
    DATABASE_NAME = os.path.join(__location__, 'data.sqlite')
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS data')
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS data (
            canton text NOT NULL,
            start_date text NOT NULL,
            end_date text NOT NULL,
            week text NOT NULL,
            year text NOT NULL,
            positive_tests integer,
            negative_tests integer,
            total_tests integer,
            positivity_rate float,
            source text,
            pcr_positive_tests integer,
            pcr_negative_tests integer,
            pcr_total_tests integer,
            pcr_positivity_rate float,
            ag_positive_tests integer,
            ag_negative_tests integer,
            ag_total_tests integer,
            ag_positivity_rate float,
            UNIQUE(canton, start_date, end_date, week, year)
        )
        '''
    )

    # add entries
    query = dc.insert_db_query(columns)
    c.executemany(query, to_db)
    conn.commit()
except Exception as e:
    print("Error: %s" % e, file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
    sys.exit(1)
finally:
    conn.close()
