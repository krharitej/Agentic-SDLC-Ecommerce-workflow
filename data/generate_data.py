import csv
import random
from pathlib import Path
from datetime import datetime, timedelta

base = Path('data')
base.mkdir(parents=True, exist_ok=True)

random.seed(42)

first_names = [
    'Ava', 'Liam', 'Noah', 'Emma', 'Olivia', 'Ethan', 'Mia', 'Sophia', 'Isabella', 'James',
    'Lucas', 'Charlotte', 'Henry', 'Harper', 'Amelia', 'Evelyn', 'Benjamin', 'William', 'Sebastian', 'Elijah'
]
last_names = [
    'Smith', 'Johnson', 'Brown', 'Lee', 'Garcia', 'Martinez', 'Davis', 'Miller', 'Wilson', 'Clark',
    'Lopez', 'Hall', 'Young', 'Allen', 'Wright', 'King', 'Scott', 'Green', 'Adams', 'Baker'
]
cities = [
    'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Seattle', 'Denver', 'Austin',
    'Boston', 'Miami', 'San Francisco', 'Atlanta', 'Dallas', 'Portland', 'San Diego'
]

num_users = 80
num_products = 60
num_orders = 70

users = []
for idx in range(1, num_users + 1):
    first = random.choice(first_names)
    last = random.choice(last_names)
    name = f"{first} {last}"
    email = f"{first.lower()}.{last.lower()}{idx}@example.com"
    age = random.randint(18, 70)
    city = random.choice(cities)
    users.append({
        'user_id': 1000 + idx,
        'name': name,
        'email': email,
        'age': age,
        'city': city,
    })

product_categories = {
    'Electronics': ['Noise-Canceling Headphones', '4K Monitor', 'Smart Speaker', 'Wireless Mouse', 'Mechanical Keyboard'],
    'Home & Kitchen': ['Air Fryer', 'Espresso Machine', 'Robot Vacuum', 'Ceramic Cookware Set', 'Weighted Blanket'],
    'Fitness': ['Adjustable Dumbbells', 'Yoga Mat', 'Smart Fitness Watch', 'Foam Roller', 'Resistance Bands'],
    'Beauty': ['Vitamin C Serum', 'Moisturizing Cream', 'Face Cleanser', 'Hair Dryer', 'Sunscreen SPF50'],
    'Outdoors': ['Insulated Water Bottle', 'Camping Tent', 'Hiking Backpack', 'Portable Grill', 'LED Lantern'],
    'Toys & Games': ['STEM Building Kit', 'Strategy Board Game', 'RC Drone', 'Puzzle Box', 'Learning Tablet']
}

products = []
product_id = 2000
for category, names in product_categories.items():
    for name in names:
        price = round(random.uniform(15, 600), 2)
        products.append({
            'product_id': product_id,
            'name': name,
            'category': category,
            'price': price,
        })
        product_id += 1

while len(products) < num_products:
    base_product = random.choice(products)
    product_id += 1
    variant_price = max(9.99, round(base_product['price'] * random.uniform(0.85, 1.15), 2))
    products.append({
        'product_id': product_id,
        'name': base_product['name'] + ' (Bundle)',
        'category': base_product['category'],
        'price': variant_price,
    })

orders = []
today = datetime.today()
for idx in range(1, num_orders + 1):
    user = random.choice(users)
    order_date = today - timedelta(days=random.randint(1, 180))
    orders.append({
        'order_id': 5000 + idx,
        'user_id': user['user_id'],
        'order_date': order_date.strftime('%Y-%m-%d'),
        'total_amount': 0.0,
    })

order_totals = {order['order_id']: 0.0 for order in orders}
order_items = []
item_id_counter = 9000
for order in orders:
    line_count = random.randint(1, 4)
    product_choices = random.sample(products, k=line_count)
    for product in product_choices:
        quantity = random.randint(1, 3)
        line_total = product['price'] * quantity
        order_totals[order['order_id']] += line_total
        order_items.append({
            'item_id': item_id_counter,
            'order_id': order['order_id'],
            'product_id': product['product_id'],
            'quantity': quantity,
        })
        item_id_counter += 1

for order in orders:
    order['total_amount'] = round(order_totals[order['order_id']], 2)

payment_methods = ['credit_card', 'debit_card', 'paypal', 'bank_transfer', 'gift_card']
payment_statuses = ['completed', 'pending', 'failed']
payments = []
for order in orders:
    status_weights = [0.8, 0.15, 0.05]
    status = random.choices(payment_statuses, weights=status_weights, k=1)[0]
    method = random.choice(payment_methods)
    payments.append({
        'payment_id': order['order_id'] + 10000,
        'order_id': order['order_id'],
        'method': method,
        'status': status,
    })

files = [
    ('users.csv', ['user_id', 'name', 'email', 'age', 'city'], users),
    ('products.csv', ['product_id', 'name', 'category', 'price'], products),
    ('orders.csv', ['order_id', 'user_id', 'order_date', 'total_amount'], orders),
    ('order_items.csv', ['item_id', 'order_id', 'product_id', 'quantity'], order_items),
    ('payments.csv', ['payment_id', 'order_id', 'method', 'status'], payments),
]

for filename, headers, rows in files:
    with (base / filename).open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

print('Data files created in', base.resolve())
