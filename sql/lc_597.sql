WITH fr_deduped AS (
    SELECT
        sender_id,
        send_to_id,
        MIN(request_date) AS request_date
    FROM FriendRequest
    GROUP BY 1, 2
),

ra_deduped AS (
    SELECT
        requester_id,
        accepter_id,
        MIN(accept_date) AS accept_date
    FROM RequestAccepted
    GROUP BY 1, 2
),

acceptance AS (
    SELECT
        r.sender_id,
        r.send_to_id,
        CASE
            WHEN a.accept_date IS NULL THEN 0
            ELSE 1
        END AS accepted
    FROM fr_deduped r
    LEFT JOIN ra_deduped a
        ON sender_id = requester_id AND send_to_id = accepter_id
)

SELECT
    CAST(SUM(accepted) AS DOUBLE) / COUNT(*) AS accept_rate
FROM acceptance
