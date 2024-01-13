-- Preferred for Uber (NoSQL)
SELECT
    e.name AS Employee
FROM Employee e
INNER JOIN Employee m
    ON e.managerId = m.id
    AND e.salary > m.salary;


-- Preferred for SQL
SELECT
    e.name AS Employee
FROM Employee e
INNER JOIN Employee m
    ON e.managerId = m.id
WHERE e.salary > m.salary;
