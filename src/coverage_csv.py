import io
from src.coverage_df import coverage_df_gen
import csv

def coverage_df_to_csv(data):
    df = coverage_df_gen(data)
    csv_string = df.to_csv()
    si = io.StringIO(csv_string)
    return si.getvalue()