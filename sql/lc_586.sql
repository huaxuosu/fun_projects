WITH order_counts AS (
    SELECT
        customer_number,
        COUNT(*) AS order_count
    FROM Orders
    GROUP BY customer_number
)

SELECT
    o.customer_number
FROM
    Orders o
INNER JOIN order_counts c
    ON o.customer_number = c.customer_number
ORDER BY c.order_count DESC
LIMIT 1;
