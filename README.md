# Sports Calendar
The Sports Calendar is a backend-focused application designed to manage and serve sports events data. It provides an API for creating and reading events, along with related information, and serves this data to a frontend interface for users to view.

Key Features:
* Stores sports events in a SQLite database (`calendar_data.db`)
* Provides a REST/HTTP API via FastAPI for interacting with events
* Includes optional scripts to populate the database with sample data for testing


## Setup

### Prerequisites
* Python 3.10
* Dependencies from `requirements.txt` — install with:
```
pip install -r requirements.txt
```
## Steps
1) Create empty database file (`calendar_data.db`) in `/data` directory:

  * Linux / macOS:
  ```
  touch data/calendar_data.db
  ```
   * Windows:
  ```
  type nul > data\calendar_data.db
  ```

2) Run the database creation script:
  ```
  python src/backend/db/db.py
  ```

3) (Optional) Populate the database with sample data:
  ```
  python scripts/populate_db.py 
  ```

4) Start the backend API:
  ```
   uvicorn src.backend.api.main:app
  ```

   Swagger docs will be available at: `http://127.0.0.1:8000/docs`

5) Start the frontend:
  ```
  cd src/frontend
  python -m http.server 8000
  ```
  Frontend wil be available at: `http://localhost:8000`


## Project structure
```
Sports Calendar
│
├── /data
│   └── calendar_data.db        # SQLite database file
│
├── /scripts
│   └── populate_db.py          # Script to populate sample data
│
├── /seeds                      # JSON files used by populate_db
│
├── /src
│   ├── /backend
│   │   ├── /api
│   │   │   ├── main.py         # Run with uvicorn
│   │   │   └── /routes         # All API route modules
│   │   │
│   │   ├── /db
│   │   │   └── db.py           # Creates tables in the DB
│   │   │
│   │   ├── /models             # Pydantic models (requests & responses)
│   │   │
│   │   └── /services           # Business logic used by routers
│   │
│   └── /frontend               # Frontend UI
│
├── data-er-diagram.png         # ER diagram
│
├── data-exmpl.json             # Example data from instructions
│
└── requirements.txt            # Python dependencies
```

## Project assumptions / decisions