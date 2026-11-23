
USE retail_sales;

-- 1. Total revenue

SELECT
    COUNT(*) AS total_orders,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM sales;


-- 2. City-wise revenue

SELECT
    city,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM sales
GROUP BY city
ORDER BY total_revenue DESC;


-- 3. Top 10 selling products

SELECT
    product_name,
    SUM(quantity) AS total_quantity
FROM sales
GROUP BY product_name
ORDER BY total_quantity DESC
LIMIT 10;


-- 4. Monthly revenue

SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS sales_month,
    ROUND(SUM(revenue), 2) AS monthly_revenue
FROM sales
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY sales_month;


-- 5. Order status analysis

SELECT
    order_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_status;


-- 6. Category-wise revenue

SELECT
    category,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM sales
GROUP BY category
ORDER BY total_revenue DESC;


-- 7. Customer-wise spending

SELECT
    customer_id,
    customer_name,
    ROUND(SUM(revenue), 2) AS total_spending
FROM sales
GROUP BY customer_id, customer_name
ORDER BY total_spending DESC
LIMIT 10;
