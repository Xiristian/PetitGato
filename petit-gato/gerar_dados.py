import pyodbc
from faker import Faker
import random
from datetime import datetime
from urllib.parse import quote_plus

import os
from dotenv import load_dotenv

load_dotenv()


account_name = os.getenv("ADLS_ACCOUNT_NAME")
file_system_name = os.getenv("ADLS_FILE_SYSTEM_NAME")
directory_name = os.getenv("ADLS_DIRECTORY_NAME")
sas_token = os.getenv("ADLS_SAS_TOKEN")

# Configurações do SQL Server
server = os.getenv("SQL_SERVER")
database = os.getenv("SQL_DATABASE")
schema = os.getenv("SQL_SCHEMA")
username = os.getenv("SQL_USERNAME")
password = quote_plus(os.getenv("SQL_PASSWORD"))
driver = '{ODBC Driver 17 for SQL Server}'

connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"

# Lista de nomes e categorias temáticos
items = [
    "Catfé", "Catppuccino", "Gato pingado", "Mia não latte", "Affogato",
    "Miaukshake de morango", "Miaukshake de chocolate", "Gato quente",
    "Gatinho caramelado", "Miau-Chocolat", "Gatolate quente", "Felincha de limão",
    "Gateado mousse", "Miaunara", "Whiskerado", "Chafé com leite", "Gato frappé",
    "Meowcha verde", "Cookie de bigodes", "Miauccino de avelã", "Latte Gatinho",
    "FrapaGato Caramelado", "Miaulicano", "Gatoccino Romeu e Julieta",
    "Miaramelo Macchiato", "Gatolatte de Amêndoas", "Miaroma", "Miauccino Mentolado",
    "Capurrcino", "Megro gato", "Miaukie Cream", "Catlix de baunilha", 
    "Frapurrcino de Caramelo", "Cappurrcino", "Gateado de leite", "Gato-ffee",
    "Miarinha Latte", "Café com Gato", "Miaudorinha", "Latte Gatunho",
    "Meowcat Macchiato", "Miau Espresso", "Mocha Rafinhado", "Gatone de Caramelo",
    "Mooga Mocha", "Latte Gatúnico", "Café Meowmaid", "Chá Miaumato",
    "Frapurrcino de Morango", "Chafé Gelado", "Miaucalate de Menta", "Cafelinado",
    "Leite Gatado", "Miaudinho de Canela", "Latte de Noz-Moscada", "Capufelino",
    "Miarão Gelado", "Gato de Vinho", "Gato Affogato", "Latte Maçaricatto",
    "Catópolis", "Latte de Marshmallow", "Capurrcino de Limão", "Esfregatasso",
    "Café Bola de Pêlo", "Capurrcino de Mel", "Gatoscatto", "Latte Gatosão",
    "Felinário Frapuccino", "Café Rascunho de Gato", "Latte Framboesa",
    "Catlix de Chocolate", "Gato Café com Chantilly", "Miau de Cereja",
    "Meowssissippi Mudslide", "Cafelatte com Gatomix", "Café de Gatomel",
    "Latte Miauninho", "Miauwauki Gelado", "Frangelho de Gato", "Latte de Gato-Canela",
    "Gatoscuro Gelado", "Miaudrinho", "Macciagato", "Frapúrrino de Gengibre",
    "Latte Miaucado", "Gatoccino Melancia", "Café com Miaucha", "Felina Capurrcino",
    "Latte Bichano", "Miarte Latte", "Carumiau Capurrcino", "Gatomallow Frapuccino",
    "Moostachio Mocha", "Vanilla Catccino", "Felinato Frapuccino", "Capurrmón de caneca",
    "Chá Miauton", "Macallade de Frapuccino", "Café Miadês", "Lasgato Latte",
    "Gatia Mocha", "Miaulino Espresso", "Gatto Gelato", "Cafairo de Gato",
    "Latte Gateado", "Gato Bolhudo", "Miauto Milkshake", "Purrcellino Cappuccino",
    "Catinsel Frappuccino", "Catish Capurrccino", "Matcha Meowcha", "Frapegatto Gelado",
    "Miaillante Cappuccino", "Gatificante Mocha", "Latte Miaudiente",
    "Frapurrcino Pistache", "Caragato Latte", "Café Gattino", "Latte Nebulinha",
    "Gato Latte Caramelo", "Miaucat Gelado", "Latte Miaucake", "Gatocciato",
    "Miaurvado Espresso", "Gatola Mocha", "Café no Pêlo", "Latte Caturégico",
    "Meowmango Smoothie", "Felino Quente", "Café Miagalho", "Latte Gatômico",
    "Café Miauchocolatado", "Latte Gattoso", "Capurrcino de Hortelã",
    "Meowmy Sake", "Gatomousse", "Latte Miaucupido", "Capurrmón Gelado",
    "Meowjito", "Latte Gatudissimo", "Miarucino", "Gattie Milkshake de Amora",
    "Gato Tigrado", "Café Miaucremoso", "Miaudicínio", "Felizante Latte",
    "Capurrcino de Pessego", "Gato Milk Latte", "Miarino Mocha", "Catadoçura",
    "Café Quato", "Latte Beirmiau", "Miaulizado Espresso", "Latte Miautor",
    "Gatomelo Frapuccino", "Latte Miaulato", "Miaulina Gelada", "Frapurrcino de Melão",
    "Latte Miauberry", "Cataculino", "Capurrcino Espesso", "Gauffe de Gato"
]

categories = [
    "Café", "Café", "Café", "Café", "Café",
    "MilkShake", "MilkShake", "Bebida Quente", "Sobremesa", "Chocolate Quente",
    "Bebida Quente", "Sobremesa", "Sobremesa", "Bebida Gelada", "Bebida Alcoólica",
    "Bebida Quente", "Bebida Gelada", "Bebida Quente", "Sobremesa", "Bebida Quente",
    "Café", "Bebida Gelada", "Café", "Café", "Café", "Café", "Café", "Bebida Quente",
    "Café", "MilkShake", "Sobremesa", "Bebida Gelada", "Café", "Café", "Bebida Quente",
    "Café", "Bebida Quente", "Bebida Quente", "Bebida Alcoólica", "Bebida Quente",
    "Café", "Café", "Café", "Café", "Café", "Café", "Café", "Bebida Quente", 
    "Bebida Gelada", "Bebida Quente", "Bebida Quente", "Café", "Sobremesa", 
    "Bebida Quente", "Bebida Gelada", "Bebida Alcoólica", "Bebida Alcoólica", 
    "Café", "Café", "Café", "Bebida Quente", "Café", "Café", "Café", "Café",
    "Bebida Gelada", "Café", "Bebida Quente", "Café", "Café", "Café", "Café", 
    "Bebida Quente", "Bebida Quente", "Café", "Bebida Quente", "Bebida Quente",
    "Café", "Bebida Gelada", "Café", "Café", "Bebida Gelada", "Bebida Alcoólica",
    "Bebida Quente", "Café", "Bebida Quente", "Bebida Gelada", "Café", "Bebida Gelada",
    "Café", "Bebida Gelada", "Bebida Quente", "Café", "Bebida Quente", "Bebida Gelada",
    "Bebida Quente", "Café", "Bebida Alcoólica", "Café", "Café", "Café", "Café",
    "MilkShake", "Bebida Quente", "Bebida Gelada", "Café", "Bebida Gelada",
    "Bebida Quente", "Café", "Café", "Bebida Quente", "Café", "Sobremesa",
    "Café", "Bebida Quente", "Café", "Bebida Gelada", "Bebida Gelada", "Café",
    "Bebida Gelada", "Café", "Bebida Quente", "Bebida Alcoólica", "Café", "Café",
    "Café", "Bebida Gelada", "Bebida Quente", "Café", "Bebida Quente", "Sobremesa",
    "Bebida Quente", "Bebida Gelada", "Café", "Café", "Sobremesa", "Sobremesa",
    "Café", "MilkShake", "Café", "Café", "Sobremesa", "Bebida Gelada", "Café",
    "Café", "Café", "Café", "Bebida Gelada", "Café", "Café", "Bebida Quente",
    "Sobremesa", "Café", "Bebida Quente", "Bebida Gelada", "Café", "Café",
    "Café", "Café", "Café", "MilkShake", "Bebida Gelada", "Bebida Quente"
]

try:
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Criar tabelas
    cursor.execute("""
    IF OBJECT_ID('cat_customer', 'U') IS NOT NULL DROP TABLE cat_customer;
    IF OBJECT_ID('payment', 'U') IS NOT NULL DROP TABLE payment;
    IF OBJECT_ID('orderitem', 'U') IS NOT NULL DROP TABLE orderitem;
    IF OBJECT_ID('customerorder', 'U') IS NOT NULL DROP TABLE customerorder;
    IF OBJECT_ID('cat', 'U') IS NOT NULL DROP TABLE cat;
    IF OBJECT_ID('item', 'U') IS NOT NULL DROP TABLE item;
    IF OBJECT_ID('coffeetable', 'U') IS NOT NULL DROP TABLE coffeetable;
    IF OBJECT_ID('customer', 'U') IS NOT NULL DROP TABLE customer;
    IF OBJECT_ID('category', 'U') IS NOT NULL DROP TABLE category;

    CREATE TABLE category (
      categoryid INT IDENTITY(1,1) PRIMARY KEY,
      description VARCHAR(100) NOT NULL
    );

    CREATE TABLE item (
      itemid INT IDENTITY(1,1) PRIMARY KEY,
      categoryid INT NOT NULL,
      description VARCHAR(100) NOT NULL,
      active BIT NOT NULL DEFAULT 1,
      price DECIMAL(15,2) NOT NULL,
      cost DECIMAL(15,2) NOT NULL,
      CONSTRAINT fk_item__category FOREIGN KEY (categoryid) REFERENCES category (categoryid)
    );

    CREATE TABLE coffeetable (
      tableid INT IDENTITY(1,1) PRIMARY KEY,
      occupied BIT NOT NULL DEFAULT 0
    );

    CREATE TABLE customer (
      customerid INT IDENTITY(1,1) PRIMARY KEY,
      name VARCHAR(100) NOT NULL,
      phone VARCHAR(30),
      email VARCHAR(100),
      cpf VARCHAR(11)
    );

    CREATE TABLE customerorder (
      orderid INT IDENTITY(1,1) PRIMARY KEY,
      customerid INT NOT NULL,
      tableid INT NOT NULL,
      date DATETIME NOT NULL,
      opened BIT NOT NULL DEFAULT 0,
      CONSTRAINT fk_customerorder__table FOREIGN KEY (tableid) REFERENCES coffeetable (tableid),
      CONSTRAINT fk_customerorder__customer FOREIGN KEY (customerid) REFERENCES customer (customerid)
    );

    CREATE TABLE orderitem (
      orderitemid INT IDENTITY(1,1) PRIMARY KEY,
      orderid INT NOT NULL,
      itemid INT NOT NULL,
      quantity INT NOT NULL,
      CONSTRAINT fk_orderitem__customerorder FOREIGN KEY (orderid) REFERENCES customerorder (orderid),
      CONSTRAINT fk_orderitem__item FOREIGN KEY (itemid) REFERENCES item (itemid)
    );

    CREATE TABLE payment (
      paymentid INT IDENTITY(1,1) PRIMARY KEY,
      customerid INT NOT NULL,
      orderid INT NOT NULL,
      value DECIMAL(15,2) NOT NULL,
      date DATETIME NOT NULL,
      CONSTRAINT fk_payment__customer FOREIGN KEY (customerid) REFERENCES customer (customerid),
      CONSTRAINT fk_payment__customerorder FOREIGN KEY (orderid) REFERENCES customerorder (orderid)
    );

    CREATE TABLE cat (
      catid INT IDENTITY(1,1) PRIMARY KEY,
      name VARCHAR(100) NOT NULL,
      age INT NOT NULL,
      adoption_date DATETIME NOT NULL
    );

    CREATE TABLE cat_customer (
      cat_customerid INT IDENTITY(1,1) PRIMARY KEY,
      catid INT NOT NULL,
      customerid INT NOT NULL,
      adoption_date DATETIME NOT NULL,
      CONSTRAINT fk_cat_customer__cat FOREIGN KEY (catid) REFERENCES cat (catid),
      CONSTRAINT fk_cat_customer__customer FOREIGN KEY (customerid) REFERENCES customer (customerid)
    );
    """)
    conn.commit()

    # Gerar dados falsos
    fake = Faker()

    # Inserir dados nas tabelas independentes
    category_id_map = {}

    for category in set(categories):
        cursor.execute('''
            INSERT INTO category (description) OUTPUT INSERTED.categoryid VALUES (?)
        ''', category)
        category_id = cursor.fetchone()[0]
        category_id_map[category] = category_id
    conn.commit()

    # Inserir itens na tabela item com referência ao ID da categoria
    for description, category in zip(items, categories):
        category_id = category_id_map[category]
        active = fake.boolean()
        price = fake.pydecimal(left_digits=2, right_digits=2, positive=True, min_value=2)
        cost = fake.pydecimal(left_digits=2, right_digits=2, positive=True, max_value=price)
        cursor.execute("INSERT INTO item (categoryid, description, active, price, cost) VALUES (?, ?, ?, ?, ?)", (category_id, description, active, price, cost))

    for _ in range(30):
        # Inserir mesa de café
        occupied = fake.boolean()
        cursor.execute("INSERT INTO coffeetable (occupied) VALUES (?)", (occupied,))

    for _ in range(5000):
        # Inserir cliente
        name = fake.name()
        phone = fake.phone_number()
        email = fake.email()
        cpf = fake.bothify(text='###########')
        cursor.execute("INSERT INTO customer (name, phone, email, cpf) VALUES (?, ?, ?, ?)", (name, phone, email, cpf))
    conn.commit()

    # Inserir gatos
    for _ in range(2000):
        cat_name = fake.first_name()
        age = random.randint(1, 15)
        adoption_date = fake.date_time_between(start_date='-3y', end_date=datetime.now())
        cursor.execute("INSERT INTO cat (name, age, adoption_date) VALUES (?, ?, ?)", (cat_name, age, adoption_date))
    conn.commit()

    customer_ids = [i for i in range(1, 5001)]
    table_ids = [i for i in range(1, 31)]
    item_ids = [i for i in range(1, items.__len__())]
    cat_ids = [i for i in range(1, 2001)]

    # Inserir dados nas tabelas dependentes
    existing_order_ids = []

    for _ in range(10000):
        # Inserir pedido do cliente
        customer_id = random.choice(customer_ids)
        table_id = random.choice(table_ids)

        # Verificar se customer_id e table_id existem nas tabelas customer e coffeetable
        cursor.execute("SELECT 1 FROM customer WHERE customerid = ?", (customer_id,))
        if not cursor.fetchone():
            raise ValueError(f"customer_id {customer_id} não encontrado na tabela 'customer'")

        cursor.execute("SELECT 1 FROM coffeetable WHERE tableid = ?", (table_id,))
        if not cursor.fetchone():
            raise ValueError(f"table_id {table_id} não encontrado na tabela 'coffeetable'")

        date = fake.date_time_between(start_date='-3y', end_date=datetime.now())
        opened = fake.boolean()
        cursor.execute("INSERT INTO customerorder (customerid, tableid, date, opened) VALUES (?, ?, ?, ?)", (customer_id, table_id, date, opened))
        conn.commit()
        order_id = _ + 1
        cursor.execute("SELECT 1 FROM customerorder WHERE orderid = ?", (order_id,))

        if not cursor.fetchone():
            raise ValueError("Falha ao inserir na tabela 'customerorder'")

        existing_order_ids.append(order_id)

        # Inserir item do pedido
        for _ in range (random.randint(1,10)):
          item_id = random.choice(item_ids)
          quantity = random.randint(1, 10)
          cursor.execute("INSERT INTO orderitem (orderid, itemid, quantity) VALUES (?, ?, ?)", (order_id, item_id, quantity))
        conn.commit()

    # Calcular o total do pedido e inserir pagamentos
    for order_id in existing_order_ids:
        cursor.execute("SELECT customerid, date FROM customerorder WHERE orderid = ?", (order_id,))
        customer_id, date = cursor.fetchone()

        cursor.execute("SELECT SUM(quantity * price) FROM orderitem JOIN item ON orderitem.itemid = item.itemid WHERE orderid = ?", (order_id,))
        total_items = cursor.fetchone()[0] or 0
    
        cursor.execute("INSERT INTO payment (customerid, orderid, value, date) VALUES (?, ?, ?, ?)", (customer_id, order_id, total_items, date))
    conn.commit()

    # Inserir adoções de gatos por clientes
    for _ in range(2000):
        cat_id = cat_ids[_]
        customer_id = random.choice(customer_ids)
        adoption_date = fake.date_time_between(start_date='-3y', end_date=datetime.now())
        cursor.execute("INSERT INTO cat_customer (catid, customerid, adoption_date) VALUES (?, ?, ?)", (cat_id, customer_id, adoption_date))
    conn.commit()

    print("Dados gerados e inseridos com sucesso!")

except pyodbc.Error as ex:
    print(f"Erro ao conectar ao SQL Server: {ex}")

finally:
    try:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    except pyodbc.Error as ex:
        print(f"Erro ao fechar a conexão: {ex}")
