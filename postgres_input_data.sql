-- Create the Employee table
CREATE TABLE Employee (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    department VARCHAR(50),
    hire_date DATE,
    salary NUMERIC(10, 2)
);

-- Insert sample records into the Employee table
INSERT INTO Employee (first_name, last_name, department, hire_date, salary) VALUES
('Alice', 'Johnson', 'Engineering', '2021-03-15', 75000.00),
('Bob', 'Smith', 'Marketing', '2020-06-01', 58000.00),
('Carol', 'Davis', 'Human Resources', '2019-11-20', 62000.00),
('David', 'Miller', 'Engineering', '2022-01-10', 80000.00),
('Eva', 'Garcia', 'Finance', '2021-08-05', 67000.00),
('Frank', 'Williams', 'Sales', '2018-02-28', 71000.00),
('Grace', 'Brown', 'Marketing', '2023-05-12', 54000.00),
('Henry', 'Jones', 'Finance', '2017-10-30', 69000.00),
('Irene', 'Martinez', 'Engineering', '2020-07-19', 78000.00),
('Jack', 'Lee', 'Human Resources', '2019-03-25', 60000.00);
