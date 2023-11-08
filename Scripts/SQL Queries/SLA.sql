SELECT
    application_id,
    CASE
        WHEN DATE_ADD(submitted_timestamp, INTERVAL 1 HOUR) > processed_timestamp THEN 'Processed within SLA'
        ELSE 'SLA violation'
    END AS SLA_status
FROM applications;

