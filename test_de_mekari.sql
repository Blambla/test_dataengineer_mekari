with employee_data as (
	select *, EXTRACT(year FROM age(resign_date,join_date))*12 + EXTRACT(month FROM age(resign_date,join_date)) as month_interval
	from (
		select employe_id, branch_id, salary, join_date,
		coalesce(resign_date,CURRENT_TIMESTAMP) as resign_date
		from test_de_mekari.employees
	) ab
), salary_acc as(
	select branch_id, sum(total_salary) as total_salary_accumulation
	from(
		select *, a.salary * a.month_interval as total_salary from employee_data a
	) ac
	group by branch_id
	order by total_salary_accumulation desc
), hour_acc as(
	select branch_id, sum(hours_interval) as hours_acc
	from(
		select a.timesheet_id, a.employee_id, b.branch_id, a.date, a.checkin, a.checkout,
		extract(epoch from(a.checkout - a.checkin))/3600 as hours_interval
		from test_de_mekari.timesheets a, test_de_mekari.employees b
		where a.employee_id = b.employe_id
	) ad
	group by branch_id
	order by hours_acc desc
), salary_per_hour as(
	select branch_id, round(total_salary_accumulation/hours_acc,0) as salary_per_hour
	from(
		select a.branch_id, a.total_salary_accumulation, b.hours_acc
		from salary_acc a
		inner join hour_acc b
		on a.branch_id = b.branch_id
	) ae
) select * from salary_per_hour
