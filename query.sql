SELECT
    u.name AS user_name,
    o.order_id,
    p.name AS product_name,
    oi.quantity,
    p.price,
    o.total_amount,
    pay.status AS payment_status
FROM users AS u
JOIN orders AS o
    ON u.user_id = o.user_id
JOIN order_items AS oi
    ON o.order_id = oi.order_id
JOIN products AS p
    ON oi.product_id = p.product_id
JOIN payments AS pay
    ON o.order_id = pay.order_id
ORDER BY o.order_id;

