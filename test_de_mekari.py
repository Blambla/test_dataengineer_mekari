import pandas as pd
import numpy as np
import math
from datetime import datetime

def main():
    #import table
    #dfe = pd.read_csv("employees.csv")
    #dft = pd.read_csv("timesheets.csv")

    #processing employees table
    dfe = dfe.rename(columns={'employe_id': 'employee_id'})
    dfe['join_date'] = pd.to_datetime(dfe['join_date'])
    dfe['resign_date'] = pd.to_datetime(dfe['resign_date'])
    dfe['resign_date'] = dfe['resign_date'].fillna(datetime.today().strftime('%Y-%m-%d'))
    dfe['month_interval'] = ((dfe.resign_date - dfe.join_date)/np.timedelta64(1, 'M')).apply(lambda x:math.floor(x))
    dfe['total_salary'] = dfe.salary * dfe.month_interval
    dfe_acc = dfe.groupby(['branch_id'])['total_salary'].sum().reset_index()

    #processing timesheets table
    dft = pd.merge(dft,dfe[['employee_id','branch_id']], on='employee_id',how='left')
    dft['date'] = pd.to_datetime(dft['date'])
    dft['checkin'] = pd.to_datetime(dft['checkin'], format = '%H:%M:%S')
    dft['checkout'] = pd.to_datetime(dft['checkout'], format = '%H:%M:%S')
    dft['hours_interval'] = (dft.checkout - dft.checkin) / pd.Timedelta(hours=1)
    dft_acc = dft.groupby(['branch_id'])['hours_interval'].sum().reset_index()

    #processing salary per hour
    df = pd.merge(dfe_acc,dft_acc, on='branch_id',how='inner')
    df['salary_per_hour'] = round(df.total_salary / df.hours_interval)
    df_final = df[['branch_id','salary_per_hour']]
    
    #show salary per hour each branch
    df_final

if __name__ == "__main__":
    main()
