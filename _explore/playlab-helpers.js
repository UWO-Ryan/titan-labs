// Installed into a Playlab embed tab to capture real transcripts (2026-10-21).
// __send(text) is done by the browser tool (focus, clear, type, Return); these read the result.
window.__clean = (el) => {
  const c = el.cloneNode(true);
  c.querySelectorAll('.katex-display, .katex').forEach(k => {
    if (k.parentElement && k.parentElement.closest('.katex')) return;
    const tex = k.querySelector('annotation');
    const t = (tex ? tex.textContent : k.innerText).replace(/\cdot/g, '·').replace(/\times/g, '×').replace(/\div/g, '÷').replace(/\frac\{([^}]*)\}\{([^}]*)\}/g, '$1/$2').replace(/\text\{([^}]*)\}/g, '$1').replace(/\[a-z]+/g, '').replace(/[{}]/g, '').trim();
    const span = document.createElement(k.classList.contains('katex-display') ? 'p' : 'span');
    span.setAttribute('data-math', '1'); span.textContent = t; k.replaceWith(span);
  });
  const keep = new Set(['P','STRONG','B','EM','I','UL','OL','LI','BR','CODE','PRE','TABLE','THEAD','TBODY','TR','TH','TD','BLOCKQUOTE','H1','H2','H3','H4','SPAN','HR']);
  const walk = (n) => { [...n.children].forEach(ch => { walk(ch); if (!keep.has(ch.tagName)) { ch.replaceWith(...ch.childNodes); } else { [...ch.attributes].forEach(a => { if (a.name !== 'data-math') ch.removeAttribute(a.name); }); } }); };
  walk(c);
  let h = c.innerHTML.replace(/<span>([\s\S]*?)<\/span>/g, '$1').replace(/<span data-math="1">([\s\S]*?)<\/span>/g, '<span class="math">$1</span>').replace(/<p data-math="1">([\s\S]*?)<\/p>/g, '<p class="math">$1</p>');
  return h.replace(/<(h[1-4])>([\s\S]*?)<\/\1>/g, '<p><strong>$2</strong></p>').replace(/<!--.*?-->/g, '').trim();
};
window.__turns = () => [...document.querySelectorAll('[data-message-id]')].map((m, i) => ({i, text: (m.querySelector('.prose') || m).innerText.trim(), html: window.__clean(m.querySelector('.prose') || m)}));
window.__editor = () => document.querySelector('[contenteditable="true"]');
window.__prep = () => { const e = window.__editor(); e.focus(); const r = document.createRange(); r.selectNodeContents(e); const s = getSelection(); s.removeAllRanges(); s.addRange(r); return 'ready'; };
window.__waitDone = async (n0, timeout = 150000) => {
  const t0 = Date.now(); let last = '', since = Date.now();
  while (Date.now() - t0 < timeout) {
    await new Promise(r => setTimeout(r, 1000));
    const ts = [...document.querySelectorAll('[data-message-id]')];
    const busy = [...document.querySelectorAll('button')].some(b => /stop/i.test(b.getAttribute('aria-label') || b.textContent));
    const cur = ts.length + '|' + (ts.length ? ts[ts.length - 1].innerText : '');
    if (cur !== last) { last = cur; since = Date.now(); }
    if (ts.length >= n0 + 2 && !busy && Date.now() - since > 3500) return {ok: true, n: ts.length, secs: (Date.now() - t0) / 1000, editor: window.__editor().innerText.trim()};
  }
  return {ok: false, n: document.querySelectorAll('[data-message-id]').length};
};
// Type one message (lines joined by paragraph breaks), send it, wait for the full reply.
window.__say = async (text) => {
  const n0 = document.querySelectorAll('[data-message-id]').length;
  window.__prep(); document.execCommand('delete');
  text.split('\n').forEach((line, i) => { if (i) document.execCommand('insertParagraph'); document.execCommand('insertText', false, line); });
  await new Promise(r => setTimeout(r, 300));
  const typed = window.__editor().innerText.replace(/\s+/g, ' ').trim();
  if (typed !== text.replace(/\s+/g, ' ').trim()) return {ok: false, why: 'editor mismatch', typed};
  document.querySelector('button[aria-label="Send message"]').click();
  const r = await window.__waitDone(n0);
  const sent = (window.__turns()[n0] || {}).text || '';
  r.sentOk = sent.replace(/\s+/g, ' ').trim() === text.replace(/\s+/g, ' ').trim();
  return r;
};
// Run a whole chat and post it to the local sink (_explore/sink.py).
window.__session = async (page, id, prompts, note = '') => {
  const log = [];
  for (const p of prompts) { const r = await window.__say(p); log.push(r); if (!r.ok || !r.sentOk) return {stopped: true, log}; }
  const body = JSON.stringify({at: new Date().toISOString(), url: location.href, turns: window.__turns().slice(1).map(t => t.html)});
  const res = await fetch(`http://127.0.0.1:8766/save?page=${page}&id=${id}` + (note ? '&note=' + encodeURIComponent(note) : ''), {method: 'POST', body});
  return {saved: await res.text(), secs: log.map(r => r.secs), replies: window.__turns().slice(2).filter((_, i) => i % 2 === 0).map(t => t.text.slice(0, 160))};
};
'helpers installed';
