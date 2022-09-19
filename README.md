# test_dataengineer_mekari

Author: Mochamad Rizal Prasetyo

list of assumptions on employees table:
1. total month differences between resign_date and join_date is how long the employee work for the branch/company
2. if the resign date is null, then the date will be replace by current date to determine for how long the employee already work for the branch/company
3. salary was given each month to the employee

list of asssumptions on timesheets table:
1. if the employee didnt checkin or checkout, then that day the employee count as not working

calculation logic on  employees table:
1. rename employe_id to employee_id (only in python) 
2. find month difference between resign_date and join_date --> month_interval
3. multiply salary and month difference as total salary that branch/company should be given to the employee --> total_salary
4. sum total_salary column group by branch_id --> sql: total_salary_accumulation, python: total_salary
5. save the result in new table --> sql: salary_acc, python: dfe_acc

calculation logic on timesheets table:
1. left join timesheets table with employees table by employee_id
2. find time interval between checkout and checkin in hours --> hours_interval
3. sum hours_interval column group by branch_id --> sql: hours_acc, python: hours_interval
4. save the result in new table --> sql: hour_acc, python: dft_acc

after doing the calculation on each table, then:
1. inner join new table from the calculation on employees table and timesheets table --> sql: ae, python: df
2. divide (sql:total_salary_accumulation, python: total_salary) by (sql:hours_acc, python: hours_interval) to get salary per hour for each branch --> salary_per_hour
3. save the result in new table --> sql: salary_per_hour, python: salary_per_hour
