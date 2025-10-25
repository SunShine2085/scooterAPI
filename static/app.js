async function fetchAvailable() {
  const res = await fetch('/api/view_all_available');
  const data = await res.json();
  const container = document.getElementById('available');
  container.innerHTML = '';
  data.forEach(s => {
    const div = document.createElement('div');
    div.className = 'scooter';
    div.textContent = `${s.id} — (${s.lat.toFixed(4)}, ${s.lng.toFixed(4)})`;
    const btn = document.createElement('button');
    btn.textContent = 'Reserve';
    btn.onclick = () => reserve(s.id);
    div.appendChild(btn);
    container.appendChild(div);
  });
}

async function reserve(id) {
  const res = await fetch('/api/reservation/start', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({id})
  });
  const j = await res.json();
  document.getElementById('action_result').textContent = JSON.stringify(j);
  fetchAvailable();
}

async function endReservation() {
  const id = document.getElementById('e_id').value;
  const lat = document.getElementById('e_lat').value;
  const lng = document.getElementById('e_lng').value;
  const res = await fetch('/api/reservation/end', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({id, lat, lng})
  });
  const j = await res.json();
  document.getElementById('action_result').textContent = JSON.stringify(j);
  fetchAvailable();
}

document.getElementById('search_btn').onclick = async () => {
  const lat = document.getElementById('s_lat').value;
  const lng = document.getElementById('s_lng').value;
  const radius = document.getElementById('s_radius').value;
  const res = await fetch(`/api/search?lat=${lat}&lng=${lng}&radius=${radius}`);
  const j = await res.json();
  const container = document.getElementById('search_results');
  container.innerHTML = '';
  j.forEach(s => {
    const d = document.createElement('div');
    d.textContent = `${s.id} — (${s.lat.toFixed(4)}, ${s.lng.toFixed(4)})`;
    const btn = document.createElement('button');
    btn.textContent = 'Reserve';
    btn.onclick = () => reserve(s.id);
    d.appendChild(btn);
    container.appendChild(d);
  });
};

document.getElementById('reserve_btn').onclick = () => {
  const id = document.getElementById('r_id').value;
  reserve(id);
};

document.getElementById('end_btn').onclick = endReservation;

window.onload = fetchAvailable;
