from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Q
from django.core.cache import cache
from .models import Transaction
from .serializers import TransactionSerializer
from django.http import HttpResponse
import time


def welcome_view(request):
    return HttpResponse("Welcome to NeoTechQuiz!")


class ClientTransactionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, client_id):
        # Define rate limit parameters
        RATE_LIMIT = 5  # Number of allowed requests
        TIME_WINDOW = 60  # Time window in seconds (e.g., 5 requests per minute)

        # Generate a unique cache key for the user
        user_key = f"rate-limit-{request.user.pk}"

        # Retrieve the current request count and timestamp for the user from the cache
        user_data = cache.get(user_key)

        current_time = time.time()

        if user_data:
            request_count, first_request_time = user_data

            # Check if the time window has expired
            if current_time - first_request_time < TIME_WINDOW:
                # If within time window, check the request count
                if request_count >= RATE_LIMIT:
                    return Response({'error': 'Rate limit exceeded. Please try again later.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
                else:
                    # Update the request count
                    request_count += 1
            else:
                # Reset the count if time window has expired
                request_count = 1
                first_request_time = current_time
        else:
            # If no data exists, initialize request count and timestamp
            request_count = 1
            first_request_time = current_time

        # Update the cache with the new request count and timestamp
        cache.set(user_key, (request_count, first_request_time), TIME_WINDOW)

        # Proceed with the original logic to handle the request
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        # Validate the date range if provided
        try:
            filter_conditions = Q(client_id=client_id)
            if start_date:
                filter_conditions &= Q(transaction_date__gte=start_date)
            if end_date:
                filter_conditions &= Q(transaction_date__lte=end_date)

            transactions = Transaction.objects.filter(filter_conditions)
        except ValueError:
            return Response({'error': 'Invalid date range or client ID.'}, status=status.HTTP_400_BAD_REQUEST)

        # Handle case if no transactions found
        if not transactions.exists():
            return Response({'error': 'No transactions found for the provided client ID.'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize and return the transactions
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
