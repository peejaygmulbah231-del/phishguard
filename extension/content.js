const btn = document.createElement('div');
btn.id = 'phishguard-floating';
btn.textContent = '🛡️ PhishGuard';
btn.style.cssText = 'position:fixed;bottom:20px;right:20px;background:#1a73e8;color:white;padding:12px 20px;border-radius:25px;font-size:14px;font-weight:bold;cursor:pointer;z-index:2147483647;font-family:Arial;';

const panel = document.createElement('div');
panel.id = 'phishguard-panel';
panel.style.cssText = 'position:fixed;bottom:80px;right:20px;width:320px;background:white;border-radius:12px;padding:16px;font-size:13px;z-index:2147483647;box-shadow:0 4px 20px rgba(0,0,0,0.2);display:none;font-family:Arial;line-height:1.6;';

btn.addEventListener('click', async () => {
  btn.textContent = '🔍 Scanning...';

  const sender =
    document.querySelector('.gD')?.getAttribute('email') ||
    document.querySelector('[email]')?.getAttribute('email') ||
    'unknown@unknown.com';

  const subject =
    document.querySelector('h2.hP')?.innerText ||
    document.querySelector('.hP')?.innerText ||
    document.title || 'No subject';

  const bodyEl =
    document.querySelector('.a3s.aiL') ||
    document.querySelector('.a3s') ||
    document.querySelector('.ii.gt') ||
    document.querySelector('.aRs') ||
    document.querySelector('.aRu');

  const body = bodyEl ? bodyEl.innerText : '';

  try {
    const response = await fetch('http://127.0.0.1:8000/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sender, subject, body })
    });

    const result = await response.json();

    const colors = {
      DANGEROUS: { bg: '#fce8e6', border: '#ea4335', text: '#c62828' },
      SUSPICIOUS: { bg: '#fff3e0', border: '#fb8c00', text: '#e65100' },
      CLEAN:      { bg: '#e6f4ea', border: '#34a853', text: '#1b5e20' }
    };

    const c = colors[result.label] || colors.CLEAN;
    panel.style.display = 'block';
    panel.style.background = c.bg;
    panel.style.border = `2px solid ${c.border}`;
    panel.style.color = c.text;
    panel.textContent = '';

    const title = document.createElement('strong');
    title.style.fontSize = '14px';
    title.textContent = `${result.label} — Score: ${result.score}/100`;
    panel.appendChild(title);
    panel.appendChild(document.createElement('br'));
    panel.appendChild(document.createElement('br'));

    const exp = document.createElement('span');
    exp.textContent = result.explanation;
    panel.appendChild(exp);

    if (result.reasons.length > 0) {
      panel.appendChild(document.createElement('br'));
      panel.appendChild(document.createElement('br'));
      const reasons = document.createElement('small');
      reasons.style.opacity = '0.8';
      reasons.textContent = result.reasons.join(' · ');
      panel.appendChild(reasons);
    }

    btn.textContent = '🛡️ PhishGuard';

  } catch (err) {
    panel.style.display = 'block';
    panel.style.background = '#fce8e6';
    panel.style.border = '2px solid #ea4335';
    panel.style.color = '#c62828';
    panel.textContent = '⚠️ Cannot connect. Make sure uvicorn is running.';
    btn.textContent = '🛡️ PhishGuard';
  }
});

document.body.appendChild(panel);
document.body.appendChild(btn);
