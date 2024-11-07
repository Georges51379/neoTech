from django.core.management.base import BaseCommand
import os
import psycopg2
from psycopg2.extras import RealDictCursor


class Command(BaseCommand):
    help = 'Refresh Materialized View'

    def handle(self, *args, **kwargs):
        db_host = os.getenv('DB_HOST', 'localhost')
        db_url = f'postgresql://postgres:postgres@{db_host}:5432/neo'

        try:
            # Connect to the PostgreSQL
            with psycopg2.connect(db_url, cursor_factory=RealDictCursor) as connection:
                with connection.cursor() as cursor:
                    # Refresh the view
                    cursor.execute("REFRESH MATERIALIZED VIEW client_transaction_summary;")
                    connection.commit()  # Commit to apply the refresh
            self.stdout.write(self.style.SUCCESS('Materialized view refreshed successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error occurred during materialized view refresh: {e}"))
