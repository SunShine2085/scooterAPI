Setup:
1. python -m venv venv
2. source venv/bin/activate (Windows: venv\Scripts\activate)
3. pip install -r requirements.txt
4. python app.py

App:
- UI: http://localhost:8080/
- API:
  GET /api/view_all_available
  GET /api/search?lat=...&lng=...&radius=...
  POST /api/reservation/start  { "id": "s1" }
  POST /api/reservation/end    { "id": "s1", "lat": 37.0, "lng": -122.0 }

Tests:
- pytest

Notes:
- Logging writes to logs/scooter_app.log via logger_config.py.
- /logs endpoint removed per request.
