// Theme toggle with memory
(function(){
  const b=document.getElementById('themeToggle');
  const saved=localStorage.getItem('theme')||'dark';
  document.body.classList.toggle('light', saved==='light');
  b&&b.addEventListener('click', ()=>{
    const next=document.body.classList.contains('light')?'dark':'light';
    document.body.classList.toggle('light', next==='light');
    localStorage.setItem('theme', next);
  });
})();

// Simple chat simulation 
(function(){
  const form=document.getElementById('chat-form');
  const input=document.getElementById('user-input');
  const win=document.getElementById('chat-window');
  const typing=document.getElementById('typing');
  if(!form||!win) return;

  form.addEventListener('submit', e=>{
    e.preventDefault();
    const text=(input.value||'').trim();
    if(!text) return;
    addBubble('user', text);
    input.value='';
    input.disabled=true;
    typing.classList.remove('hidden');
    setTimeout(()=>{
      typing.classList.add('hidden');
      addBubble('bot', 'Danke! (Demo-Antwort)');
      input.disabled=false;
      input.focus();
    }, 700);
  });

  function addBubble(role, text){
    const wrap=document.createElement('div');
    wrap.className = role==='user' ? 'bubble user' : 'bubble bot with-avatar';

    if(role==='bot'){
      const av=document.createElement('img');
      av.className='bubble-avatar';
      const headerLogo=document.querySelector('.logo');
      av.src=headerLogo?headerLogo.src:'';
      av.alt='Bot';
      wrap.appendChild(av);
    }

    const body=document.createElement('div');
    body.className='bubble-body';

    const msg=document.createElement('div');
    msg.className='bubble-text';
    msg.textContent=text;

    const meta=document.createElement('div');
    meta.className='meta';
    meta.textContent=new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});

    body.appendChild(msg);
    body.appendChild(meta);
    wrap.appendChild(body);
    win.appendChild(wrap);
    win.scrollTop = win.scrollHeight;
  }
})();
