import uuid
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from my_app.models import Client, Transaction
import datetime


class ClientTransactionsAPITest(APITestCase):

    def setUp(self):
        # Create a test client with a valid UUID for client_id
        self.client = Client.objects.create(
            client_id=uuid.uuid4(),  # Generate a valid UUID for client_id
            name="Test Grg",
            email="grg@example.com",
            date_of_birth="1990-01-01",
            country="USA",
            account_balance=1000.00
        )

        # Create test transactions for the client
        Transaction.objects.create(
            transaction_id=uuid.uuid4(),  # Generate a valid UUID for transaction_id
            client=self.client,
            transaction_type='buy',
            transaction_date=datetime.date(2024, 10, 1),
            amount=500.00,
            currency='USD'
        )

        Transaction.objects.create(
            transaction_id=uuid.uuid4(),  # Generate a valid UUID for transaction_id
            client=self.client,
            transaction_type='sell',
            transaction_date=datetime.date(2024, 9, 15),
            amount=-300.00,
            currency='USD'
        )

        # Create a test user
        self.user = self.create_test_user()
        self.api_client = APIClient()
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def create_test_user(self):
        from django.contrib.auth.models import User
        return User.objects.create_user(username="testuser", password="testpassword")

    def test_get_transactions(self):
        # Define the URL for the client transactions endpoint
        url = reverse('client-transactions', kwargs={'client_id': str(self.client.client_id)})

        # Add date range to the request
        start_date = '2024-09-01'
        end_date = '2024-10-31'
        response = self.api_client.get(url, {'start_date': start_date, 'end_date': end_date})

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response contains the expected data
        self.assertEqual(len(response.data), 2)

    def test_get_transactions_no_date_range(self):
        # Test fetching transactions without specifying a date range
        url = reverse('client-transactions', kwargs={'client_id': str(self.client.client_id)})
        response = self.api_client.get(url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_transactions_invalid_client_id(self):
        # Test with an invalid UUID as client_id
        invalid_client_id = str(uuid.uuid4())  # Generate a random valid UUID that does not exist in the DB
        url = reverse('client-transactions', kwargs={'client_id': invalid_client_id})
        response = self.api_client.get(url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
