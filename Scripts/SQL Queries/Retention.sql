-- Calculate daily retention for a specific date range
WITH active_users AS (
    SELECT
        user_id,
        DATE_TRUNC('day', activity_date) AS activity_day
    FROM
        user_activity
    WHERE
        activity_date BETWEEN 'start_date' AND 'end_date'
),

retention_data AS (
    SELECT
        au.activity_day AS reference_day,
        COUNT(DISTINCT au.user_id) AS active_users,
        COUNT(DISTINCT CASE WHEN ra.activity_day = au.activity_day + 1 THEN ra.user_id END) AS retained_users
    FROM
        active_users au
    LEFT JOIN
        active_users ra ON au.user_id = ra.user_id
    GROUP BY
        au.activity_day
)

SELECT
    reference_day,
    active_users,
    retained_users,
    (retained_users * 100.0 / active_users) AS retention_rate
FROM
    retention_data
ORDER BY
    reference_day;

