# Cube Visual

This project provides a simple web interface to query an OLAP cube and visualize
results in a spreadsheet‑like interface. The backend is built with **FastAPI**
and uses **pyadomd** and **pymdx** to query the cube. The frontend is built with
**React** and **TypeScript**.

## Requirements

- Python 3.10+
- Node.js 18+
- Access to an OLAP cube via ADOMD. Create a `.env` file inside `backend` with the variable `ADOMD_CONNECTION` set to your connection string (see `backend/.env.example`).

## Running the backend

Build and start the backend using Docker Compose:

```bash
docker compose up --build
```

The backend will be available at `http://localhost:8000`. Endpoints:

- `POST /query` – run an MDX query ({"mdx": "..."})
- `GET /fields` – list available cube dimensions and measures
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
