import os
import json
import sqlite3
from typing import List, Tuple, Optional, Dict

from geopy.distance import distance as geodesic


# Path to SQLite DB file
DB_PATH = os.path.join(os.path.dirname(__file__), "scooter.db")


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def bootstrap_db(seed_json_path: str = "scooter_db.json") -> None:
    """
    Ensure schema exists. If table is empty, seed once from JSON file.
    """
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS scooters (
                id TEXT PRIMARY KEY,
                lat REAL NOT NULL,
                lng REAL NOT NULL,
                is_reserved INTEGER NOT NULL
            )
            """
        )
        cur.execute("SELECT COUNT(1) FROM scooters")
        count = int(cur.fetchone()[0])
        if count == 0:
            items: List[Dict] = []
            try:
                with open(seed_json_path, "r") as f:
                    items = json.load(f)
            except FileNotFoundError:
                items = []
            for it in items:
                cur.execute(
                    "INSERT OR REPLACE INTO scooters (id, lat, lng, is_reserved) VALUES (?,?,?,?)",
                    (
                        str(it.get("id")),
                        float(it.get("lat", 0.0)),
                        float(it.get("lng", 0.0)),
                        1 if it.get("is_reserved") else 0,
                    ),
                )
        conn.commit()


class Scooter:
    def __init__(self, scooter_id: str, lat: float, lng: float, is_reserved: bool) -> None:
        self.id = str(scooter_id)
        self.lat = float(lat)
        self.lng = float(lng)
        self.is_reserved = bool(is_reserved)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "lat": self.lat,
            "lng": self.lng,
            "is_reserved": self.is_reserved,
        }


def convert_db_to_dictlist(db: List[Scooter]) -> List[Dict]:
    return [s.to_dict() for s in db]


def load_all() -> List[Scooter]:
    """Return all scooters as Scooter objects."""
    bootstrap_db()
    items: List[Scooter] = []
    with get_conn() as conn:
        cur = conn.cursor()
        for row in cur.execute("SELECT id, lat, lng, is_reserved FROM scooters"):
            items.append(Scooter(str(row[0]), float(row[1]), float(row[2]), bool(int(row[3]))))
    return items


def load_available() -> List[Scooter]:
    """Return available scooters as Scooter objects."""
    bootstrap_db()
    items: List[Scooter] = []
    with get_conn() as conn:
        cur = conn.cursor()
        for row in cur.execute("SELECT id, lat, lng, is_reserved FROM scooters WHERE is_reserved = 0"):
            items.append(Scooter(str(row[0]), float(row[1]), float(row[2]), False))
    return items


def upsert_full(db: List[Scooter]) -> None:
    """Replace the entire scooters table with provided list."""
    bootstrap_db()
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM scooters")
        for s in db:
            cur.execute(
                "INSERT INTO scooters (id, lat, lng, is_reserved) VALUES (?,?,?,?)",
                (s.id, float(s.lat), float(s.lng), 1 if s.is_reserved else 0),
            )
        conn.commit()


def get_by_id(scooter_id: str) -> Optional[Scooter]:
    bootstrap_db()
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, lat, lng, is_reserved FROM scooters WHERE id = ?", (str(scooter_id),))
        row = cur.fetchone()
        if not row:
            return None
        return Scooter(str(row[0]), float(row[1]), float(row[2]), bool(int(row[3])))


def reserve(scooter_id: str) -> Tuple[Dict, int]:
    """Try to reserve a scooter. Returns (payload, http_status)."""
    bootstrap_db()
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, is_reserved FROM scooters WHERE id = ?", (str(scooter_id),))
        row = cur.fetchone()
        if not row:
            return {"msg": f"Error 422 - No scooter with id {scooter_id} was found."}, 422
        if int(row[1]) == 1:
            return {"msg": f"Error 422 - Scooter with id {scooter_id} is already reserved."}, 422
        cur.execute("UPDATE scooters SET is_reserved = 1 WHERE id = ?", (str(scooter_id),))
        conn.commit()
    return {"msg": f"Scooter {scooter_id} was reserved successfully."}, 200


def end_reservation(scooter_id: str, end_lat: float, end_lng: float) -> Tuple[Dict, int]:
    """End a reservation, update location, and return (payload, http_status)."""
    bootstrap_db()
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, lat, lng, is_reserved FROM scooters WHERE id = ?", (str(scooter_id),))
        row = cur.fetchone()
        if not row:
            return {"msg": f"Error 422 - No scooter with id {scooter_id} was found."}, 422
        if int(row[3]) != 1:
            return {"msg": f"Error 422 - No reservation for scooter {scooter_id} presently exists."}, 422

        old_location = (float(row[1]), float(row[2]))
        new_location = (float(end_lat), float(end_lng))
        distance_ridden = round(geodesic(old_location, new_location).m)
        _ = distance_ridden  # placeholder for a real pricing function

        # Dummy payment gateway: always succeed and return a fixed txn id
        txn_id = 379892831

        cur.execute(
            "UPDATE scooters SET is_reserved = 0, lat = ?, lng = ? WHERE id = ?",
            (float(end_lat), float(end_lng), str(scooter_id)),
        )
        conn.commit()
    return {
        "msg": f"Payment for scooter {scooter_id} was made successfully and the reservation was ended.",
        "txn_id": txn_id,
    }, 200


def search_available(lat: float, lng: float, radius_m: float) -> List[Dict]:
    """
    Return available scooters within radius (metres) of (lat, lng) as
    a list of dicts with id, lat, lng.
    """
    bootstrap_db()
    center = (float(lat), float(lng))
    out: List[Dict] = []
    with get_conn() as conn:
        cur = conn.cursor()
        for row in cur.execute("SELECT id, lat, lng FROM scooters WHERE is_reserved = 0"):
            loc = (float(row[1]), float(row[2]))
            d = geodesic(loc, center).m
            if d <= float(radius_m):
                out.append({"id": str(row[0]), "lat": float(row[1]), "lng": float(row[2])})
    return out

