# Step 1: Base Image
FROM python:3.10-slim

# Step 2: Set the working directory
WORKDIR /app

# Step 3: Copy requirements.txt and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy the Django application code to the working directory
COPY . /app

# Step 5: Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Step 6: Run the wait script, migrations, and start the Django development server
CMD ["sh", "-c", "python manage.py wait_for_db && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

# Expose the port that the Django app runs on
EXPOSE 8000
