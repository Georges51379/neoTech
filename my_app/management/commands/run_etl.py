from django.core.management.base import BaseCommand
import pandas as pd
from sqlalchemy import create_engine, text
import traceback
import os


class Command(BaseCommand):
    help = 'Run ETL process for clients and transactions data'

    def handle(self, *args, **kwargs):
        # Get the database host from the environment, default to 'localhost' for local usage
        db_host = os.getenv('DB_HOST', 'localhost')
        db_url = f'postgresql://postgres:postgres@{db_host}:5432/neo'
        engine = create_engine(db_url)

        try:
            # Extract Data
            self.stdout.write('Extracting data...')
            clients_df = pd.read_csv('clients.csv')
            transactions_df = pd.read_csv('transactions.csv')

            self.stdout.write(f'Extracted {len(clients_df)} clients and {len(transactions_df)} transactions.')

            # Transform Data
            self.stdout.write('Transforming data...')
            clients_df.fillna('', inplace=True)
            transactions_df.fillna(0, inplace=True)

            # Assuming a conversion rate (1 EUR = 1.1 USD)

            CONVERSION_RATE_EUR_TO_USD = 1.1

            clients_df['date_of_birth'] = pd.to_datetime(clients_df['date_of_birth']).dt.strftime('%Y-%m-%d')
            transactions_df['transaction_date'] = pd.to_datetime(transactions_df['transaction_date']).dt.strftime('%Y-%m-%d')
            clients_df['account_balance'] = clients_df['account_balance'].round(2)
            transactions_df['amount'] = transactions_df['amount'].round(2)
            clients_df['country'] = clients_df['country'].str.upper()
            transactions_df['currency'] = transactions_df['currency'].str.upper()
            transactions_df['amount'] = transactions_df.apply(
                lambda row: row['amount'] * CONVERSION_RATE_EUR_TO_USD if row['currency'] == 'EUR' else row['amount'],
                axis=1
            )
            transactions_df['currency'] = transactions_df['currency'].replace('EUR', 'USD')
            transactions_df['transaction_type'] = transactions_df['transaction_type'].str.lower()
            transactions_df['transaction_type'] = transactions_df['transaction_type'].replace({'buy': 'buy', 'sell': 'sell'})
            transactions_df = transactions_df[transactions_df['transaction_type'].isin(['buy', 'sell'])]
            clients_df['name'] = clients_df['name'].str.title()

            # Load Data
            self.stdout.write('Loading data into the database...')
            with engine.begin() as connection:  # Use `begin()` to handle transactions automatically
                for _, row in clients_df.iterrows():
                    self.stdout.write(f"Inserting client: {row['client_id']}")
                    upsert_query = text("""
                    INSERT INTO my_app_client (client_id, name, email, date_of_birth, country, account_balance)
                    VALUES (:client_id, :name, :email, :date_of_birth, :country, :account_balance)
                    ON CONFLICT (client_id) DO UPDATE SET
                        name = EXCLUDED.name,
                        email = EXCLUDED.email,
                        date_of_birth = EXCLUDED.date_of_birth,
                        country = EXCLUDED.country,
                        account_balance = EXCLUDED.account_balance;
                    """)
                    result = connection.execute(upsert_query, row.to_dict())
                    self.stdout.write(f"Rows affected: {result.rowcount}")
                    connection.execute(upsert_query, row.to_dict())

                for _, row in transactions_df.iterrows():
                    self.stdout.write(f"Inserting transaction: {row['transaction_id']}")
                    upsert_query = text("""
                    INSERT INTO my_app_transaction (transaction_id, transaction_type, transaction_date, amount, currency, client_id)
                    VALUES (:transaction_id, :transaction_type, :transaction_date, :amount, :currency, :client_id)
                    ON CONFLICT (transaction_id) DO UPDATE SET
                        client_id = EXCLUDED.client_id,
                        transaction_type = EXCLUDED.transaction_type,
                        amount = EXCLUDED.amount,
                        currency = EXCLUDED.currency
                    """)
                    result = connection.execute(upsert_query, row.to_dict())
                    self.stdout.write(f"Rows affected: {result.rowcount}")
                    connection.execute(upsert_query, row.to_dict())

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error occurred during loading: {e}"))
            traceback.print_exc()
        else:
            self.stdout.write(self.style.SUCCESS('ETL process completed successfully'))
