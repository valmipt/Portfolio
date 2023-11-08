-- Calculate DAU, WAU, and MAU
WITH user_activity_daily AS (
    SELECT
        DATE(activity_date) AS activity_day,
        user_id
    FROM
        user_activity
),
user_activity_weekly AS (
    SELECT
        DATE(activity_day) AS week_start,
        user_id
    FROM
        user_activity_daily
    GROUP BY
        week_start, user_id
),
user_activity_monthly AS (
    SELECT
        DATE_TRUNC('month', activity_day) AS month_start,
        user_id
    FROM
        user_activity_daily
    GROUP BY
        month_start, user_id
)
SELECT
    'DAU' AS period,
    activity_day AS date,
    COUNT(DISTINCT user_id) AS active_users
FROM
    user_activity_daily
GROUP BY
    activity_day
UNION ALL
SELECT
    'WAU' AS period,
    week_start AS date,
    COUNT(DISTINCT user_id) AS active_users
FROM
    user_activity_weekly
GROUP BY
    week_start
UNION ALL
SELECT
    'MAU' AS period,
    month_start AS date,
    COUNT(DISTINCT user_id) AS active_users
FROM
    user_activity_monthly
GROUP BY
    month_start
ORDER BY
    period, date;

