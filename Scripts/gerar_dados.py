import psycopg2
from faker import Faker
import random

fake = Faker('pt_BR')

#import pyodbc

# Conexão ao banco de dados SQL Server
#conn = pyodbc.connect(
#    'Driver={SQL Server};'
#    'Server=seu_servidor;'
#    'Database=seu_banco_de_dados;'
#    'UID=seu_usuario;'
#    'PWD=sua_senha;'
#)
#cursor = conn.cursor()

# Conexão ao banco de dados
conn = psycopg2.connect(
    host="localhost",
    database="satc-teste",
    user="postgres",
    password="postgres"
)
cur = conn.cursor()

def insert_categories():
    categories = [
        'Cafés', 'Milkshakes', 'Bolos e pães', 'Salgados', 'Sucos',
        'Sanduíches e Hamburgueres', 'Doces variados'
    ]
    cur.executemany("INSERT INTO category (description) VALUES (%s);", [(cat,) for cat in categories])
    conn.commit()
    print("Categorias inseridas com sucesso!")

def insert_items():
    items = [
        (1, 'Catfé', 2.50, True),
        (1, 'Catppuccino', 5.00, True),
        (1, 'Gato pingado', 2.50, True),
        (1, 'Mia não latte', 4.00, True),
        (1, 'Affogato', 9.00, True),
        (2, 'Miaukshake de morango', 10.00, True),
        (2, 'Miaukshake de chocolate', 10.00, True),
        (2, 'Miaukshake de baunilha', 10.00, True),
        (3, 'Catcake de morango', 8.00, True),
        (3, 'Catcake de brigadeiro', 8.00, True),
        (3, 'Catcake de limão', 8.00, False),
        (3, 'Amassando pãozinho', 20.00, True),
        (4, 'Salgato de frango', 8.00, True),
        (4, 'Salgato de camarão', 9.00, True),
        (4, 'Salgato de palmito vegano', 8.00, True),
        (5, 'Catjuice de laranja', 6.00, True),
        (5, 'Catjuice de maracujá', 6.00, True),
        (5, 'Catjuice de morango', 6.00, True),
        (5, 'Catjuice de abacaxi', 6.00, False),
        (6, 'Catburguer vegano', 20.00, True),
        (6, 'Catburguer', 18.00, True),
        (7, 'Donucat', 7.00, True),
        (7, 'Petit gatô', 11.00, True)
    ]
    cur.executemany(
        "INSERT INTO item (categoryid, description, price, active) VALUES (%s, %s, %s, %s);", items)
    conn.commit()
    print("Itens inseridos com sucesso!")

def insert_coffeetables():
    tables = [(random.choice([True, False]),) for _ in range(10)]
    cur.executemany("INSERT INTO coffeetable (occupied) VALUES (%s);", tables)
    conn.commit()
    print("Mesas inseridas com sucesso!")

def insert_customers():
    customers = []
    for _ in range(10000):
        name = fake.name()
        phone = fake.phone_number()[:15]  # máximo 15 caracteres
        email = fake.email()[:50]  # máximo 50 caracteres
        cpf = fake.cpf().replace('.', '').replace('-', '')[:11]  # máximo 11 caracteres
        customers.append((name, phone, email, cpf))
    
    cur.executemany(
        "INSERT INTO customer (name, phone, email, cpf) VALUES (%s, %s, %s, %s);", customers)
    conn.commit()
    print("Clientes inseridos com sucesso!")

def insert_customerorders():
    orders = []
    for _ in range(10000):
        customerid = random.randint(1, 10000)
        tableid = random.randint(1, 10)
        total = round(random.uniform(10.0, 100.0), 2)
        date = fake.date_time_between(start_date='-3y', end_date='now')
        opened = random.choice([True, False])
        orders.append((customerid, tableid, total, date, opened))
    
    cur.executemany(
        "INSERT INTO customerorder (customerid, tableid, total, date, opened) VALUES (%s, %s, %s, %s, %s);", orders)
    conn.commit()
    print("Pedidos de clientes inseridos com sucesso!")

def insert_orderitems():
    order_items = []
    for _ in range(10000):
        orderid = random.randint(1, 10000)
        itemid = random.randint(1, 22)
        quantity = random.randint(1, 5)
        total_price = round(random.uniform(5.0, 50.0), 2) * quantity
        order_items.append((orderid, itemid, total_price, quantity))
    
    cur.executemany(
        "INSERT INTO orderitem (orderid, itemid, total_price, quantity) VALUES (%s, %s, %s, %s);", order_items)
    conn.commit()
    print("Itens de pedidos inseridos com sucesso!")

def insert_payments():
    payments = []
    for _ in range(10000):
        customerid = random.randint(1, 10000)
        orderid = random.randint(1, 10000)
        value = round(random.uniform(10.0, 100.0), 2)
        date = fake.date_time_between(start_date='-3y', end_date='now')
        payments.append((customerid, orderid, value, date))
    
    cur.executemany(
        "INSERT INTO payment (customerid, orderid, value, date) VALUES (%s, %s, %s, %s);", payments)
    conn.commit()
    print("Pagamentos inseridos com sucesso!")

# Inserindo dados nas tabelas
insert_categories()
insert_items()
insert_coffeetables()
insert_customers()
insert_customerorders()
insert_orderitems()
insert_payments()

# Fechar a conexão com o banco de dados
cur.close()
conn.close()
print("Banco de dados populado com sucesso!")
