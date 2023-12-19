from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from datetime import datetime
from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    @staticmethod
    def format_args_comma(sql, parameters: dict):
        sql += ", ".join([f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)])
        return sql, tuple(parameters.values())

    async def add_user(self,
                       first_name: str,
                       last_name: str,
                       user_type: str,
                       username: str,
                       password: str,
                       company_id: int,
                       photo: str = None,
                       auth_status: bool = False):
        created_at, updated_at = datetime.now(), datetime.now()
        sql = """INSERT INTO Users (first_name, last_name, user_type, username, password, company_id, photo, auth_status, created_at, updated_at)
                 VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10) RETURNING *"""
        return await self.execute(sql, first_name, last_name, user_type, username, password, company_id,
                                  photo, auth_status, created_at, updated_at, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_users(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_users_without_admin(self, **kwargs):
        sql = "SELECT * FROM Users WHERE user_type != 'admin' AND "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def delete_user(self, **kwargs):
        await self.delete_orders(waiter_id=kwargs['id'])
        sql = "DELETE FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, execute=True)

    async def update_user(self, user_id: int, **kwargs):
        sql = "UPDATE Users SET "
        sql, parameters = self.format_args_comma(sql, parameters=kwargs)
        sql += f" WHERE id = ${len(parameters) + 1}"
        parameters = (*parameters, user_id)
        print(f"SQL Query: {sql}")
        print(f"Parameters: {parameters}")
        return await self.execute(sql, *parameters, execute=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def select_company(self, **kwargs):
        sql = "SELECT * FROM Companies WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_categories(self, **kwargs):
        sql = "SELECT * FROM Categories WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def add_product(self,
                          name: str,
                          unit: str,
                          price: int,
                          photo: str,
                          category_id: int,
                          company_id: int,
                          description: str):
        created_at, updated_at = datetime.now(), datetime.now()
        sql = """INSERT INTO Products (name, unit, price, photo, category_id, company_id, description, created_at, updated_at)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) RETURNING *"""
        return await self.execute(sql, name, unit, price, photo, category_id, company_id, description, created_at,
                                  updated_at, fetchrow=True)

    async def select_products(self, **kwargs):
        sql = "SELECT * FROM Products WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_product(self, **kwargs):
        sql = "SELECT * FROM Products WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_category(self, **kwargs):
        sql = "SELECT * FROM Categories WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def delete_product(self, **kwargs):
        await self.delete_orders(product_id=kwargs['id'])
        sql = "DELETE FROM Products WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, execute=True)

    async def update_product(self, product_id: int, **kwargs):
        sql = "UPDATE Products SET "
        sql, parameters = self.format_args_comma(sql, parameters=kwargs)
        sql += f" WHERE id = ${len(parameters) + 1}"
        parameters = (*parameters, product_id)
        print(f"SQL Query: {sql}")
        print(f"Parameters: {parameters}")
        return await self.execute(sql, *parameters, execute=True)

    async def select_not_empty_tables(self, **kwargs):
        sql = "SELECT * FROM Tables WHERE is_active = TRUE AND "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_empty_tables(self, **kwargs):
        sql = "SELECT * FROM Tables WHERE is_active = FALSE AND "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_tables(self, **kwargs):
        sql = "SELECT * FROM Tables WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_table(self, **kwargs):
        sql = "SELECT * FROM Tables WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def delete_table(self, **kwargs):
        await self.delete_orders(table_id=kwargs['id'])
        sql = "DELETE FROM Tables WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, execute=True)

    async def update_table(self, table_id: int, **kwargs):
        sql = "UPDATE Tables SET "
        sql, parameters = self.format_args_comma(sql, parameters=kwargs)
        sql += f" WHERE id = ${len(parameters) + 1}"
        parameters = (*parameters, table_id)
        print(f"SQL Query: {sql}")
        print(f"Parameters: {parameters}")
        return await self.execute(sql, *parameters, execute=True)

    async def create_new_table(self, name: str, company_id: int):
        created_at, updated_at = datetime.now(), datetime.now()
        is_active = False
        sql = """INSERT INTO Tables (name, company_id, is_active, created_at, updated_at)
                    VALUES ($1, $2, $3, $4, $5) RETURNING *"""
        return await self.execute(sql, name, company_id, is_active, created_at, updated_at, fetchrow=True)

    async def select_orders(self, **kwargs):
        sql = "SELECT * FROM Orders WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_orders_products(self, **kwargs):
        sql = "SELECT * FROM Orders_Products WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_order(self, **kwargs):
        sql = "SELECT * FROM Orders WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_product_order(self, **kwargs):
        sql = "SELECT * FROM Product_Orders WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def create_new_order(self, table_id: int, product_id: int, weight: float, waiter_id: int, company_id: int,
                               service_fee: int, status: str):
        created_at, updated_at = datetime.now(), datetime.now()
        sql = """INSERT INTO Orders (table_id, product_id, weight, waiter_id, company_id, service_fee, status, created_at, updated_at)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) RETURNING *"""
        return await self.execute(sql, table_id, product_id, weight, waiter_id, company_id, service_fee, status,
                                  created_at, updated_at, fetchrow=True)

    async def update_order(self, order_id: int, **kwargs):
        sql = "UPDATE Orders SET "
        sql, parameters = self.format_args_comma(sql, parameters=kwargs)
        sql += f" WHERE id = ${len(parameters) + 1}"
        parameters = (*parameters, order_id)
        print(f"SQL Query: {sql}")
        print(f"Parameters: {parameters}")
        return await self.execute(sql, *parameters, execute=True)

    async def update_order_with_table_id(self, table_id: int, **kwargs):
        sql = "UPDATE Orders SET "
        sql, parameters = self.format_args_comma(sql, parameters=kwargs)
        sql += f" WHERE table_id = ${len(parameters) + 1}"
        parameters = (*parameters, table_id)
        print(f"SQL Query: {sql}")
        print(f"Parameters: {parameters}")
        return await self.execute(sql, *parameters, execute=True)

    async def delete_order(self, table_id: int):
        sql = "DELETE FROM Orders WHERE table_id = $1"
        return await self.execute(sql, table_id, execute=True)

    async def delete_orders(self, **kwargs):
        sql = "DELETE FROM Orders WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, execute=True)

    async def select_cooks(self):
        sql = "SELECT * FROM Users WHERE user_type = 'cook'"
        return await self.execute(sql, fetch=True)

    async def get_statistics(self, company_id: int, date_from: datetime):
        sql = """SELECT
                    o.created_at AS "ordered_at",
                    string_agg(p.name, ', ') AS "products",
                    t.name AS "table_name",
                    u.first_name || ' ' || u.last_name AS "waiter",
                    SUM(p.price * o.weight) AS "total_products_price",
                    (SUM(p.price * o.weight) * 0.01 * o.service_fee) AS "service_fee",
                    SUM(o.weight * p.price) + (SUM(o.weight * p.price) * 0.01 * o.service_fee) AS "total_price"
                FROM
                    orders o
                JOIN
                    products p ON o.product_id = p.id
                JOIN
                    tables t ON o.table_id = t.id
                JOIN
                    users u ON o.waiter_id = u.id
                WHERE
                    o.company_id = $1 AND o.created_at >= $2
                GROUP BY
                    o.created_at, t.name, u.first_name, u.last_name, o.service_fee
                ORDER BY
                    o.created_at;
                    """
        return await self.execute(sql, company_id, date_from, fetch=True)

    async def best_selling_product(self, company_id: int, date_from: datetime):
        sql = """SELECT
                    p.name AS "name",
                    SUM(o.weight) AS "total_weight",
                    SUM(o.weight * p.price) AS "total_price"
                FROM
                    orders o
                JOIN
                    products p ON o.product_id = p.id
                WHERE
                    o.company_id = $1 AND o.created_at >= $2
                GROUP BY
                    p.name
                ORDER BY
                    SUM(o.weight) DESC
                    """
        return await self.execute(sql, company_id, date_from, fetch=True)

    async def order_count(self, company_id: int, date_from: datetime):
        sql = """SELECT
                    COUNT(DISTINCT o.created_at) AS "total_orders"
                FROM
                    orders o
                WHERE 
                    o.company_id = $1 AND o.created_at >= $2
                    """
        return await self.execute(sql, company_id, date_from, fetchrow=True)

    async def total_price(self, company_id: int, date_from: datetime):
        sql = """SELECT
                    SUM(o.weight * p.price) AS "total_price"
                FROM
                    orders o
                JOIN
                    products p ON o.product_id = p.id
                WHERE 
                    o.company_id = $1 AND o.created_at >= $2
                    """
        return await self.execute(sql, company_id, date_from, fetchrow=True)

    async def total_service_fee(self, company_id: int, date_from: datetime):
        sql = """SELECT SUM(service_fee) AS "total_service_fee"
        FROM (
            SELECT SUM(o.weight * p.price) * 0.01 * o.service_fee AS "service_fee"
            FROM orders o
            JOIN products p ON o.product_id = p.id
            WHERE o.company_id = $1 AND o.created_at >= $2
            GROUP BY o.service_fee
        ) AS service_fee;
                    """
        return await self.execute(sql, company_id, date_from, fetchrow=True)

    async def total_price_by_waiter(self, company_id: int, waiter_id: int, date_from: datetime):
        sql = """SELECT
                    SUM(o.weight * p.price) AS "total_price"
                FROM
                    orders o
                JOIN
                    products p ON o.product_id = p.id
                WHERE 
                    o.company_id = $1 AND o.waiter_id = $2 AND o.created_at >= $3
                    """
        return await self.execute(sql, company_id, waiter_id, date_from, fetchrow=True)

    async def total_service_fee_by_waiter(self, company_id: int, waiter_id: int, date_from: datetime):
        sql = """SELECT SUM(service_fee) AS "total_service_fee"
        FROM (
            SELECT SUM(o.weight * p.price) * 0.01 * o.service_fee AS "service_fee"
            FROM orders o
            JOIN products p ON o.product_id = p.id
            WHERE o.company_id = $1 AND o.waiter_id = $2 AND o.created_at >= $3
            GROUP BY o.service_fee
        ) AS service_fee;
                    """
        return await self.execute(sql, company_id, waiter_id, date_from, fetchrow=True)

    async def get_order_count_by_waiter(self, company_id: int, waiter_id: int, date_from: datetime):
        sql = """SELECT
                    COUNT(DISTINCT o.created_at) AS "total_orders"
                FROM
                    orders o
                WHERE 
                    o.company_id = $1 AND o.waiter_id = $2 AND o.created_at >= $3
                    """
        return await self.execute(sql, company_id, waiter_id, date_from, fetchrow=True)

    async def get_statistics_by_products(self, company_id: int, date_from: datetime, ):
        """
        for example:
        Mahsulotlar statistikasi:
        Nomi    | Soni | Jami narxi
        Shashlik| 10   | 10000
        """
        sql = """SELECT
                    p.name AS "product_name",
                    SUM(o.weight) AS "total_weight",
                    SUM(o.weight * p.price) AS "total_price"
                FROM
                    orders o
                JOIN
                    products p ON o.product_id = p.id
                WHERE
                    o.company_id = $1 AND o.created_at >= $2
                GROUP BY
                    p.name;
                    """
        return await self.execute(sql, company_id, date_from, fetch=True)
