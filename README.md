# Cube Visual

This project provides a simple web interface to query an OLAP cube and visualize
results in a spreadsheet‑like interface. The backend is built with **FastAPI**
and uses **pyadomd** (ADOMD.NET) to query the cube. The frontend is built with
**React** and **TypeScript**.

## Requirements

- Python 3.10+
- Node.js 18+
- A .NET runtime. The Docker image installs `dotnet-runtime-8.0` and sets
  `PYTHONNET_RUNTIME=coreclr`. When running directly on Windows install
  [.NET 8](https://dotnet.microsoft.com/download) and set the same environment
  variable so pythonnet loads the CoreCLR runtime.
- Access to an OLAP cube. Create a `.env` file inside `backend` with connection
  details for your cube (see `backend/.env.example`). The main settings are
  `ADOMD_DLL_PATH` and `ADOMD_CONN_STR`. If `ADOMD_CONN_STR` is not provided the
  example connection string

  ```python
  conn_str = (
      "Provider=MSOLAP;"
      "Data Source=server;"
      "Initial Catalog=Cube8;"
      "Integrated Security=SSPI;"
  )
  ```

  will be used.

## Running the backend

Build and start the backend using Docker Compose:

```bash
docker compose up --build
```

The backend will be available at `http://localhost:8000`. Endpoints:

- `POST /query` – run an MDX query ({"mdx": "..."})
- `GET /fields` – list available cube dimensions and measures
- `GET /health` – verify cube connection
- `GET /reports` – list saved reports
- `POST /reports` – save a new report ({"name": "Report", "mdx": "..."})

## Running the frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173` (Vite default). It
allows selecting cube fields, building tables with Excel‑like filters, and
creating configurable charts. Saved reports can be loaded and refreshed.

## Running the backend with Docker

```bash
cd backend
docker build -t cube-backend .
docker run -p 8000:8000 --env-file .env cube-backend
```


## Running the backend with Docker Compose

Ensure the `.env` file exists and run:

```bash
docker compose up --build
```

The backend will be available at `http://localhost:8000`.

## Running tests

Unit tests are located in the `tests` directory and use **pytest**. After
installing the backend dependencies simply run:

```bash
pip install -r backend/requirements.txt
pytest
```

The tests mock the cube connection, so they run without requiring access to an
actual OLAP server.

## Example: list cube measures

Use the helper script to print all measures from a cube. Set `CUBE_NAME` and connection variables in `.env` and run:

```bash
CUBE_NAME=NextGen python -m backend.app.list_measures
```
