with tiv_2015_cnt AS (
    SELECT
        CAST(tiv_2015*100 AS INT) AS tiv_2015_x_100,
        COUNT(*) AS cnt
    FROM Insurance
    GROUP BY 1
)

SELECT
    SUM(a.tiv_2016) AS tiv_2016
FROM Insurance a
LEFT JOIN Insurance b
    ON b.pid != b.pid
    AND ABS(a.lat - b.lat) < 1e-16
    AND ABS(a.lon - b.lon) < 1e-16
JOIN tiv_2015_cnt c
    ON CAST(a.tiv_2015*100 AS INT) = c.tiv_2015_x_100
    AND c.cnt > 1
WHERE b.lat IS NULL
