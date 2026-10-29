import io

import pandas as pd

def csv_buffer_from_df(df):
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    return csv_buffer