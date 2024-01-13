SELECT
    t.id
FROM Weather t
INNER JOIN Weather y
    ON DATEDIFF(t.recordDate, y.recordDate) = 1
    AND t.temperature > y.temperature;
