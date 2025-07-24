# Cube Visual

This project provides a simple web interface to query an OLAP cube and visualize
results in a spreadsheet‑like interface. The backend is built with **FastAPI**
and uses **pyadomd** and **pymdx** to query the cube. The frontend is built with
**React** and **TypeScript**.

## Requirements

- Python 3.10+
- Node.js 18+
- Access to an OLAP cube via ADOMD (set `ADOMD_CONNECTION` environment variable)

## Running the backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# run development server
./start.sh
```

The backend will be available at `http://localhost:8000`. Endpoints:

- `POST /query` – run an MDX query ({"mdx": "..."})
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
docker run -p 8000:8000 -e ADOMD_CONNECTION="<connection>" cube-backend
```

