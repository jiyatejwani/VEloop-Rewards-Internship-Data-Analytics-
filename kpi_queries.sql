-- ============================================================================
-- VELOOP Rewards - KPI definitions in SQL
-- Data Analyst Internship, Task 01 (companion to the KPI Catalogue, #11)
--
-- Written against the logical data model (see the Data Dictionary, #9).
-- KPIs 1-7 are computable from the SUPPLIED simulated data.
-- KPIs 8-10 depend on PROPOSED tables that do not exist yet and are shown
-- to document what instrumentation is required before they can be measured.
--
-- NOTE: all data is SIMULATED / FICTIONAL - results are not actual VELOOP figures.
-- ============================================================================

-- 1. New registrations by month
SELECT date_trunc('month', registration_datetime) AS month,
       COUNT(*)                                    AS new_users
FROM users
GROUP BY 1
ORDER BY 1;

-- 2. Daily Active Users (DAU) = distinct users with a qualifying activity that day
SELECT activity_date,
       COUNT(DISTINCT user_id) AS dau
FROM daily_activity
WHERE active_flag = 'Yes'
GROUP BY activity_date
ORDER BY activity_date;

-- 3. Monthly Active Users (MAU)
SELECT date_trunc('month', activity_date) AS month,
       COUNT(DISTINCT user_id)            AS mau
FROM daily_activity
WHERE active_flag = 'Yes'
GROUP BY 1
ORDER BY 1;

-- 4. Task completion rate = completed attempts / all attempts
SELECT ROUND(100.0 * SUM(CASE WHEN task_status = 'Completed' THEN 1 ELSE 0 END)
             / COUNT(*), 1) AS task_completion_rate_pct
FROM task_activity;

-- 5. Task failure breakdown by reason
SELECT failure_reason,
       COUNT(*) AS attempts
FROM task_activity
WHERE task_status IN ('Failed', 'Abandoned')
  AND failure_reason IS NOT NULL
GROUP BY failure_reason
ORDER BY attempts DESC;

-- 6. Feature adoption rate = unique users of a feature / all users
SELECT fe.feature_name,
       COUNT(DISTINCT fe.user_id) AS users,
       ROUND(100.0 * COUNT(DISTINCT fe.user_id)
             / (SELECT COUNT(*) FROM users), 1) AS adoption_pct
FROM feature_events fe
GROUP BY fe.feature_name
ORDER BY users DESC;

-- 7. New-user D7 retention = cohort active on day 7 after registration
WITH cohort AS (
    SELECT user_id, CAST(registration_datetime AS DATE) AS reg_date
    FROM users
)
SELECT ROUND(100.0 * COUNT(DISTINCT d.user_id) / COUNT(DISTINCT c.user_id), 1)
       AS d7_retention_pct
FROM cohort c
LEFT JOIN daily_activity d
       ON d.user_id = c.user_id
      AND d.activity_date = c.reg_date + INTERVAL '7 day'
      AND d.active_flag = 'Yes';

-- ----------------------------------------------------------------------------
-- PROPOSED KPIs - require tables that do not exist in the supplied data.
-- Included to specify the instrumentation needed (see Coverage Matrix, #3).
-- ----------------------------------------------------------------------------

-- 8. [PROPOSED] Reward credit volume - needs the rewards_ledger table
-- SELECT currency_unit, SUM(amount) AS credited
-- FROM rewards_ledger
-- WHERE reward_state = 'credited'
-- GROUP BY currency_unit;

-- 9. [PROPOSED] Withdrawal completion rate - needs the withdrawals table
-- SELECT ROUND(100.0 * SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END)
--              / COUNT(*), 1) AS withdrawal_completion_pct
-- FROM withdrawals;

-- 10. [PROPOSED] Referral conversion rate - needs the referrals table
-- SELECT ROUND(100.0 * SUM(CASE WHEN status = 'converted' THEN 1 ELSE 0 END)
--              / COUNT(*), 1) AS referral_conversion_pct
-- FROM referrals;
