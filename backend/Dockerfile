FROM python:3.11-slim

# Install git (for dependencies fetched from VCS) and the .NET runtime
RUN apt-get update \
    && apt-get install -y --no-install-recommends git dotnet-runtime-8.0 \
    && rm -rf /var/lib/apt/lists/*

# Use .NET (CoreCLR) with pythonnet
ENV PYTHONNET_RUNTIME=coreclr

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
