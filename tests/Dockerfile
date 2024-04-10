# Use a base image that contains necessary tools to run tests (e.g., Python)
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy the source code files into the container
COPY . /app

# Add src/ directory to Python path within the container
RUN python -c "import sys; sys.path.append('/app/src')"

# Install necessary dependencies for running unit tests
RUN pip install -r tests/unit_tests_requirements.txt

# Command to run unit tests
CMD ["pytest", "tests/"]
