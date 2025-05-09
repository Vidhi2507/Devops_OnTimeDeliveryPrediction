# Use a Python base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /POSTASSIGNMENT

# Copy the current directory contents into the container
COPY . /POSTASSIGNMENT

# Expose the port FastAPI will be running on
EXPOSE 5000

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the FastAPI app using Uvicorn
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
