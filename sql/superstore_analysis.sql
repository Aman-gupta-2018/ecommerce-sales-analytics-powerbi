-- ============================================================================
-- SUPERSTORE E-COMMERCE SALES ANALYSIS — ADVANCED SQL QUERIES
-- ============================================================================
-- Dataset: Kaggle Superstore (Sample - Superstore.csv)
-- This file demonstrates advanced SQL skills:
--   CTEs, Window Functions (RANK, LAG, ROW_NUMBER), Conditional Aggregation,
--   Subqueries, Pivot Logic, and Business KPIs.
-- Written for SQL Server / PostgreSQL syntax (minor adjustments may be needed).
-- ============================================================================

-- ============================================================================
-- 1. HIGH-LEVEL KPIs
-- ============================================================================

-- 1.1 Overall business performance
SELECT
    COUNT(DISTINCT OrderID)                                          AS total_orders,
    COUNT(DISTINCT CustomerID)                                       AS total_customers,
    ROUND(SUM(Sales), 2)                                             AS total_revenue,
    ROUND(SUM(Profit), 2)                                            AS total_profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2)                         AS profit_margin_pct,
    ROUND(SUM(Sales) / COUNT(DISTINCT OrderID), 2)                   AS avg_order_value,
    ROUND(AVG(Discount) * 100, 2)                                    AS avg_discount_pct
FROM superstore;

-- 1.2 Year-over-year revenue growth using LAG window function
WITH yearly AS (
    SELECT
        YEAR(OrderDate)                                             AS year,
        ROUND(SUM(Sales), 2)                                        AS revenue
    FROM superstore
    GROUP BY YEAR(OrderDate)
)
SELECT
    year,
    revenue,
    LAG(revenue) OVER (ORDER BY year)                               AS prev_year_revenue,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY year))
        / LAG(revenue) OVER (ORDER BY year) * 100,
        2
    )                                                               AS yoy_growth_pct
FROM yearly
ORDER BY year;

-- ============================================================================
-- 2. REVENUE & PROFIT ANALYSIS
-- ============================================================================

-- 2.1 Revenue, profit, and margin by category & sub-category
SELECT
    Category,
    SubCategory,
    ROUND(SUM(Sales), 2)                                            AS revenue,
    ROUND(SUM(Profit), 2)                                           AS profit,
    ROUND(SUM(Profit) / NULLIF(SUM(Sales), 0) * 100, 2)             AS margin_pct,
    COUNT(DISTINCT OrderID)                                         AS orders
FROM superstore
GROUP BY Category, SubCategory
ORDER BY profit ASC;  -- Shows loss-makers at the top

-- 2.2 Monthly revenue trend with running total (cumulative sum)
WITH monthly_revenue AS (
    SELECT
        FORMAT(OrderDate, 'yyyy-MM')                                AS month,
        ROUND(SUM(Sales), 2)                                        AS revenue
    FROM superstore
    GROUP BY FORMAT(OrderDate, 'yyyy-MM')
)
SELECT
    month,
    revenue,
    ROUND(SUM(revenue) OVER (ORDER BY month), 2)                    AS running_total
FROM monthly_revenue
ORDER BY month;

-- 2.3 Revenue contribution percentage by category
SELECT
    Category,
    ROUND(SUM(Sales), 2)                                            AS revenue,
    ROUND(SUM(Sales) / SUM(SUM(Sales)) OVER () * 100, 2)            AS revenue_share_pct
FROM superstore
GROUP BY Category
ORDER BY revenue DESC;

-- ============================================================================
-- 3. DISCOUNT IMPACT ANALYSIS (KEY INSIGHT)
-- ============================================================================

-- 3.1 Profit impact of discount bands
SELECT
    CASE
        WHEN Discount = 0 THEN 'No Discount'
        WHEN Discount <= 0.10 THEN '1-10%'
        WHEN Discount <= 0.20 THEN '11-20%'
        WHEN Discount <= 0.30 THEN '21-30%'
        ELSE '30%+'
    END                                                             AS discount_band,
    COUNT(*)                                                        AS order_lines,
    ROUND(SUM(Sales), 2)                                            AS revenue,
    ROUND(SUM(Profit), 2)                                           AS profit,
    ROUND(AVG(Profit / NULLIF(Sales, 0)) * 100, 2)                  AS avg_margin_pct
FROM superstore
GROUP BY
    CASE
        WHEN Discount = 0 THEN 'No Discount'
        WHEN Discount <= 0.10 THEN '1-10%'
        WHEN Discount <= 0.20 THEN '11-20%'
        WHEN Discount <= 0.30 THEN '21-30%'
        ELSE '30%+'
    END
ORDER BY MIN(Discount);

-- 3.2 Compare discounted vs non-discounted profitability
SELECT
    CASE WHEN Discount > 0 THEN 'Discounted' ELSE 'No Discount' END AS order_type,
    COUNT(*)                                                        AS order_lines,
    ROUND(AVG(Profit / NULLIF(Sales, 0)) * 100, 2)                  AS avg_margin_pct,
    ROUND(SUM(Profit), 2)                                           AS total_profit,
    SUM(CASE WHEN Profit < 0 THEN 1 ELSE 0 END)                     AS loss_count,
    ROUND(100.0 * SUM(CASE WHEN Profit < 0 THEN 1 ELSE 0 END) / COUNT(*), 2) AS loss_rate_pct
FROM superstore
GROUP BY CASE WHEN Discount > 0 THEN 'Discounted' ELSE 'No Discount' END;

-- ============================================================================
-- 4. REGIONAL & GEOGRAPHIC ANALYSIS
-- ============================================================================

-- 4.1 Region performance with rank
SELECT
    Region,
    ROUND(SUM(Sales), 2)                                            AS revenue,
    ROUND(SUM(Profit), 2)                                           AS profit,
    ROUND(SUM(Profit) / NULLIF(SUM(Sales), 0) * 100, 2)             AS margin_pct,
    RANK() OVER (ORDER BY SUM(Profit) DESC)                         AS profit_rank
FROM superstore
GROUP BY Region
ORDER BY profit DESC;

-- 4.2 Top 10 states by profit and bottom 5 (loss-making)
SELECT TOP 10
    State,
    ROUND(SUM(Sales), 2)                                            AS revenue,
    ROUND(SUM(Profit), 2)                                           AS profit
FROM superstore
GROUP BY State
ORDER BY profit DESC;

SELECT TOP 5
    State,
    ROUND(SUM(Profit), 2)                                           AS profit
FROM superstore
GROUP BY State
ORDER BY profit ASC;

-- ============================================================================
-- 5. CUSTOMER ANALYSIS & SEGMENTATION
-- ============================================================================

-- 5.1 Customer segment (Consumer/Corporate/Home Office) performance
SELECT
    Segment,
    COUNT(DISTINCT CustomerID)                                      AS customers,
    COUNT(DISTINCT OrderID)                                         AS orders,
    ROUND(SUM(Sales), 2)                                            AS revenue,
    ROUND(SUM(Sales) / COUNT(DISTINCT CustomerID), 2)               AS revenue_per_customer,
    ROUND(SUM(Profit), 2)                                           AS profit
FROM superstore
GROUP BY Segment
ORDER BY revenue DESC;

-- 5.2 RFM Segmentation using window functions
--     (Recency, Frequency, Monetary — the industry-standard customer value model)
WITH customer_metrics AS (
    SELECT
        CustomerID,
        DATEDIFF(day, MAX(OrderDate), (SELECT MAX(OrderDate) FROM superstore)) AS recency_days,
        COUNT(DISTINCT OrderID)                                     AS frequency,
        ROUND(SUM(Sales), 2)                                        AS monetary
    FROM superstore
    GROUP BY CustomerID
),
rfm_scores AS (
    SELECT
        CustomerID,
        recency_days,
        frequency,
        monetary,
        -- NTILE: divide customers into 5 equal buckets per metric (5 = best)
        NTILE(5) OVER (ORDER BY recency_days DESC)                  AS r_score,  -- lower recency = higher score
        NTILE(5) OVER (ORDER BY frequency ASC)                      AS f_score,
        NTILE(5) OVER (ORDER BY monetary ASC)                       AS m_score
    FROM customer_metrics
)
SELECT
    CASE
        WHEN r_score + f_score + m_score >= 13 THEN 'Champions'
        WHEN r_score + f_score + m_score >= 10 THEN 'Loyal Customers'
        WHEN r_score >= 4 AND f_score <= 2 THEN 'New Customers'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk'
        WHEN r_score <= 2 AND m_score >= 3 THEN 'Cant Lose Them'
        WHEN r_score <= 2 THEN 'Lost/Hibernating'
        ELSE 'Need Attention'
    END                                                             AS rfm_segment,
    COUNT(*)                                                        AS customer_count,
    ROUND(SUM(monetary), 2)                                         AS segment_revenue,
    ROUND(AVG(monetary), 2)                                         AS avg_customer_value
FROM rfm_scores
GROUP BY
    CASE
        WHEN r_score + f_score + m_score >= 13 THEN 'Champions'
        WHEN r_score + f_score + m_score >= 10 THEN 'Loyal Customers'
        WHEN r_score >= 4 AND f_score <= 2 THEN 'New Customers'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk'
        WHEN r_score <= 2 AND m_score >= 3 THEN 'Cant Lose Them'
        WHEN r_score <= 2 THEN 'Lost/Hibernating'
        ELSE 'Need Attention'
    END
ORDER BY segment_revenue DESC;

-- 5.3 Top 10 customers by lifetime value
SELECT TOP 10
    CustomerName,
    CustomerID,
    COUNT(DISTINCT OrderID)                                         AS orders,
    ROUND(SUM(Sales), 2)                                            AS lifetime_value,
    ROUND(SUM(Profit), 2)                                           AS lifetime_profit,
    ROUND(AVG(Sales), 2)                                            AS avg_order_value
FROM superstore
GROUP BY CustomerName, CustomerID
ORDER BY lifetime_value DESC;

-- ============================================================================
-- 6. SHIPPING & OPERATIONS ANALYSIS
-- ============================================================================

-- 6.1 Ship mode performance and average delivery time
SELECT
    ShipMode,
    COUNT(DISTINCT OrderID)                                         AS orders,
    ROUND(AVG(DATEDIFF(day, OrderDate, ShipDate)), 2)               AS avg_shipping_days,
    MAX(DATEDIFF(day, OrderDate, ShipDate))                         AS max_shipping_days,
    ROUND(SUM(Profit), 2)                                           AS profit
FROM superstore
GROUP BY ShipMode
ORDER BY avg_shipping_days;

-- 6.2 Orders shipped late relative to expected window (ops quality metric)
SELECT
    ShipMode,
    SUM(CASE WHEN DATEDIFF(day, OrderDate, ShipDate) > expected_days THEN 1 ELSE 0 END) AS late_orders,
    COUNT(*)                                                        AS total_orders,
    ROUND(100.0 * SUM(CASE WHEN DATEDIFF(day, OrderDate, ShipDate) > expected_days THEN 1 ELSE 0 END)
          / COUNT(*), 2)                                            AS late_rate_pct
FROM (
    SELECT *,
        CASE
            WHEN ShipMode = 'Same Day' THEN 1
            WHEN ShipMode = 'First Class' THEN 2
            WHEN ShipMode = 'Second Class' THEN 4
            ELSE 6
        END                                                         AS expected_days
    FROM superstore
) t
GROUP BY ShipMode;

-- ============================================================================
-- 7. SEASONALITY & PRODUCT ANALYSIS
-- ============================================================================

-- 7.1 Monthly seasonality: average revenue by calendar month (year over year)
SELECT
    MONTH(OrderDate)                                                AS month_num,
    DATENAME(month, OrderDate)                                      AS month_name,
    ROUND(AVG(monthly_rev), 2)                                      AS avg_monthly_revenue
FROM (
    SELECT
        MONTH(OrderDate)                                            AS month_num,
        YEAR(OrderDate)                                             AS year_num,
        FORMAT(OrderDate, 'yyyy-MM')                                AS month_key,
        SUM(Sales)                                                  AS monthly_rev
    FROM superstore
    GROUP BY MONTH(OrderDate), YEAR(OrderDate), FORMAT(OrderDate, 'yyyy-MM')
) m
GROUP BY MONTH(OrderDate), DATENAME(month, OrderDate)
ORDER BY month_num;

-- 7.2 Best and worst selling products
SELECT TOP 10
    ProductName,
    Category,
    SubCategory,
    SUM(Quantity)                                                   AS units_sold,
    ROUND(SUM(Sales), 2)                                            AS revenue,
    ROUND(SUM(Profit), 2)                                           AS profit
FROM superstore
GROUP BY ProductName, Category, SubCategory
ORDER BY revenue DESC;

SELECT TOP 10
    ProductName,
    ROUND(SUM(Profit), 2)                                           AS profit
FROM superstore
GROUP BY ProductName
ORDER BY profit ASC;  -- Biggest money-losers

-- 7.3 Products that lose money despite high sales volume
SELECT
    ProductName,
    SubCategory,
    SUM(Quantity)                                                   AS units_sold,
    ROUND(SUM(Sales), 2)                                            AS revenue,
    ROUND(SUM(Profit), 2)                                           AS profit
FROM superstore
GROUP BY ProductName, SubCategory
HAVING SUM(Sales) > 5000 AND SUM(Profit) < 0
ORDER BY profit ASC;

-- ============================================================================
-- 8. COHORT / REPEAT PURCHASE ANALYSIS
-- ============================================================================

-- 8.1 Repeat purchase rate: customers with more than one order
SELECT
    CASE
        WHEN order_count = 1 THEN '1 Order (One-time)'
        WHEN order_count = 2 THEN '2 Orders'
        WHEN order_count BETWEEN 3 AND 5 THEN '3-5 Orders'
        ELSE '6+ Orders'
    END                                                             AS order_count_band,
    COUNT(*)                                                        AS customers,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2)              AS share_pct
FROM (
    SELECT CustomerID, COUNT(DISTINCT OrderID) AS order_count
    FROM superstore
    GROUP BY CustomerID
) c
GROUP BY
    CASE
        WHEN order_count = 1 THEN '1 Order (One-time)'
        WHEN order_count = 2 THEN '2 Orders'
        WHEN order_count BETWEEN 3 AND 5 THEN '3-5 Orders'
        ELSE '6+ Orders'
    END
ORDER BY MIN(order_count);

-- 8.2 Time between consecutive orders (purchase cycle) using LAG
WITH ordered AS (
    SELECT
        CustomerID,
        OrderID,
        OrderDate,
        LAG(OrderDate) OVER (PARTITION BY CustomerID ORDER BY OrderDate) AS prev_order_date
    FROM (SELECT DISTINCT CustomerID, OrderID, OrderDate FROM superstore) distinct_orders
)
SELECT
    ROUND(AVG(DATEDIFF(day, prev_order_date, OrderDate)), 1)        AS avg_days_between_orders,
    MIN(DATEDIFF(day, prev_order_date, OrderDate))                  AS min_days,
    MAX(DATEDIFF(day, prev_order_date, OrderDate))                  AS max_days
FROM ordered
WHERE prev_order_date IS NOT NULL;

-- ============================================================================
-- 9. TOP PROFITABLE / UNPROFITABLE COMBINATIONS
-- ============================================================================

-- 9.1 Region x Category matrix (find underperformers)
SELECT
    Region,
    Category,
    ROUND(SUM(Sales), 2)                                            AS revenue,
    ROUND(SUM(Profit), 2)                                           AS profit,
    ROUND(SUM(Profit) / NULLIF(SUM(Sales), 0) * 100, 2)             AS margin_pct
FROM superstore
GROUP BY Region, Category
ORDER BY profit ASC;

-- 9.2 Detect anomaly: high sales, negative profit (red flag accounts)
SELECT
    CustomerName,
    Segment,
    ROUND(SUM(Sales), 2)                                            AS revenue,
    ROUND(SUM(Profit), 2)                                           AS profit
FROM superstore
GROUP BY CustomerName, Segment
HAVING SUM(Sales) > 1000 AND SUM(Profit) < 0
ORDER BY profit ASC;

-- ============================================================================
-- 10. PERFORMANCE: WEEKDAY vs WEEKEND + DAY-OF-WEEK ANALYSIS
-- ============================================================================

SELECT
    DATENAME(weekday, OrderDate)                                    AS day_of_week,
    COUNT(DISTINCT OrderID)                                         AS orders,
    ROUND(SUM(Sales), 2)                                            AS revenue,
    ROUND(AVG(Sales), 2)                                            AS avg_order_value
FROM superstore
GROUP BY DATENAME(weekday, OrderDate)
ORDER BY revenue DESC;
