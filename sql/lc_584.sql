SELECT
    c.name
FROM Customer c
LEFT JOIN Customer r
    ON c.referee_id = r.id
WHERE r.id IS NULL OR r.id != 2;


-- This doesn't work.  WHY?
SELECT
    c.name
FROM Customer c
LEFT JOIN Customer r
    ON c.referee_id = r.id
    AND r.id != 2;
