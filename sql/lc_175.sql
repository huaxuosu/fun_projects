-- Write your MySQL query statement below
SELECT
    p.firstName,
    p.lastName,
    a.city,
    a.state
FROM Person p
LEFT JOIN Address a
    ON p.personId = a.personId;


-- select all columns and all rows
SELECT
    *
FROM Person;


-- select some columns (specified by col names) and some rows (filtered by predicates)
SELECT
    lastName,
    firstName
FROM Person
WHERE personId = 2;

SELECT
    lastName,
    firstName
FROM Person
-- NOTE: string needs to use ' (single quote), NEVER uses " (double quote)
WHERE lastName = 'Wang';


-- data aggregation
SELECT
    -- Agg by column
    lastName,
    -- Agg function: count total # of rows
    COUNT(*) AS num_persons
FROM Person
-- omit WHERE clause so that we use all the rows in the table
GROUP BY lastName
ORDER BY lastName DESC;


-- HAVING clause
SELECT
    -- Agg by column
    lastName AS lname,
    -- Agg function: count total # of rows
    COUNT(*) AS num_persons
FROM Person
-- omit WHERE clause so that we use all the rows in the table
GROUP BY lastName
HAVING COUNT(*) > 1;


-- Handling NULL
-- Write your MySQL query statement below
SELECT
    p.firstName,
    p.lastName,
    a.city,
    a.state
FROM Person p
LEFT JOIN Address a
    ON p.personId = a.personId
WHERE a.personId IS NULL;

