# Stage 2: Set up Flask backend
FROM python:3.9-slim

# Set working directory for the backend
WORKDIR /app/backend

# Install dependencies for Flask
RUN pip install --no-cache-dir flask flask_cors beautifulsoup4 requests

# Copy the Flask app code
COPY backend/ .

# Copy the frontend build files from the frontend stage
COPY frontend/build /app/backend/static


# Expose port 5000 (default for Flask)
EXPOSE 5000

# Start the Flask app
CMD ["flask", "--app", "get_prices.py", "run", "--host=0.0.0.0"]  