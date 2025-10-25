async function getCareer() {
  const interests = document.getElementById('interest-input').value;
  if (!interests) return;
  const res = await fetch('http://127.0.0.1:5000/career', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ interests })
  });
  const data = await res.json();
  document.getElementById('career-result').innerHTML =
    "Your ideal career: <b>" + data.career + "</b>";
}
async function getMusic() {
  const mood = document.getElementById('mood-input').value;
  if (!mood) { document.getElementById('music-result').innerHTML = "Please type a mood!"; return;}
  const res = await fetch('http://127.0.0.1:5000/music', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ mood })
  });
  const data = await res.json();
  let html = "Suggested tracks:<ul>";
  for(const song of data.playlist) html += `<li>${song}</li>`;
  html += "</ul>";
  document.getElementById('music-result').innerHTML = html;
}
async function getMotivation() {
  try {
    const res = await fetch('http://127.0.0.1:5000/motivational');
    const data = await res.json();
    document.getElementById('motivational-quote').innerText = data.quote;
  } catch(e) {
    document.getElementById('motivational-quote').innerText = "Could not fetch quote!";
  }
}
async function getLifeSupport() {
  const situation = document.getElementById('situation-select').value;
  if (!situation) {
    document.getElementById('support-result').innerHTML = "Please select a situation!";
    return;
  }
  
  const res = await fetch('http://127.0.0.1:5000/life-support', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ situation })
  });
  const data = await res.json();
  
  let html = `<div style="background:linear-gradient(93deg, #ffd8bc 16%, #befff2 100%); padding:15px; border-radius:10px; text-align:left; box-shadow:0 2px 7px #ffb6e6a5;">
    <p style="font-weight:700; color:#f755ae; font-size:1.1em; margin-bottom:10px;">${data.message}</p>
    <p style="font-weight:600; color:#18b8a6; margin-bottom:8px;">Action Steps:</p>
    <ul style="margin:0; padding-left:20px; color:#23aec2;">`;
  
  data.steps.forEach(step => {
    html += `<li style="margin-bottom:5px;">${step}</li>`;
  });
  
  html += `</ul></div>`;
  document.getElementById('support-result').innerHTML = html;
}
async function getMotivation() {
  try {
    const res = await fetch('http://127.0.0.1:5000/motivational');
    const data = await res.json();
    document.getElementById('motivational-quote').innerHTML =
      "🌈 " + data.quote +
      `<br><a href="${data.youtube}" target="_blank" style="color:#fbbf24; font-weight:bold; margin-top:8px; display:inline-block;">Watch Motivation Video 👉</a>
      <br>
      <iframe width="100%" height="170" src="https://www.youtube.com/embed/${data.youtube.split('v=')[1]}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="border-radius:10px; margin-top:8px;"></iframe>`;
  } catch(e) {
    document.getElementById('motivational-quote').innerText = "Could not fetch quote!";
  }
}
