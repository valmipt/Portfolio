WITH paying_users AS (
    SELECT
        user_id,
        DATE_TRUNC('month', payment_date) AS payment_month
    FROM
        payments
    WHERE
        payment_amount > 0
),

monthly_revenue AS (
    SELECT
        user_id,
        payment_month,
        SUM(payment_amount) AS monthly_revenue
    FROM
        paying_users
    GROUP BY
        user_id, payment_month
)

SELECT
    payment_month,
    AVG(monthly_revenue) AS arpu
FROM
    monthly_revenue
GROUP BY
    payment_month
ORDER BY
    payment_month;

