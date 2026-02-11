// Theme toggle with memory
(function () {
  const b = document.getElementById('themeToggle');
  const saved = localStorage.getItem('theme') || 'dark';
  document.body.classList.toggle('light', saved === 'light');
  b && b.addEventListener('click', () => {
    const next = document.body.classList.contains('light') ? 'dark' : 'light';
    document.body.classList.toggle('light', next === 'light');
    localStorage.setItem('theme', next);
  });
})();

// Chat (AJAX) - Aufgabe 2
(function () {
  const form = document.getElementById('chat-form');
  const input = document.getElementById('user-input');
  const win = document.getElementById('chat-window');
  const typing = document.getElementById('typing');
  const resetBtn = document.getElementById('reset-btn');

  if (!form || !win || !input) return;

  const sendUrl = form.dataset.sendUrl;
  const resetUrl = form.dataset.resetUrl;
  //if (!sendUrl) return; // not chatbot page, so don't run ajax chat here

  // 1) Auto focus
  input.focus();

  // 2) Enter sends (no newline)
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      form.requestSubmit();
    }
  });

  // 3) Send without page reload using fetch()
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const text = (input.value || '').trim();
    if (!text) return;

    // show user message immediately
    addBubble('user', text);

    input.value = '';
    input.disabled = true;
    typing && typing.classList.remove('hidden');

    try {
      const res = await fetch(sendUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });

      const data = await res.json();

      if (!data.ok) {
        addBubble('bot', 'Error: message could not be sent.');
      } else {
        addBubble('bot', data.bot.text);
      }
    } catch (err) {
      addBubble('bot', 'Network error.');
    } finally {
      typing && typing.classList.add('hidden');
      input.disabled = false;
      input.focus();
    }
  });

  // 4) Reset button clears session + reloads page
  if (resetBtn) {
    resetBtn.addEventListener('click', async () => {
      try {
        await fetch(resetUrl, { method: 'POST' });
      } catch (e) {
        // even if request fails, reset UI anyway
      }
      location.reload();
    });
  }

  function addBubble(role, text) {
    const wrap = document.createElement('div');
    wrap.className = role === 'user' ? 'bubble user' : 'bubble bot with-avatar';

    if (role === 'bot') {
      const av = document.createElement('img');
      av.className = 'bubble-avatar';
      const headerLogo = document.querySelector('.logo');
      av.src = headerLogo ? headerLogo.src : '';
      av.alt = 'Bot';
      wrap.appendChild(av);
    }

    const body = document.createElement('div');
    body.className = 'bubble-body';

    const msg = document.createElement('div');
    msg.className = 'bubble-text';
    msg.textContent = text;

    const meta = document.createElement('div');
    meta.className = 'meta';
    meta.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    body.appendChild(msg);
    body.appendChild(meta);
    wrap.appendChild(body);
    win.appendChild(wrap);
    win.scrollTop = win.scrollHeight;
  }
})();
