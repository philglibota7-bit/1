/* ---------- Menüsuche: Treffer schon beim Tippen, Pfeiltasten, Enter öffnet den ersten Treffer ---------- */
function siteSearch(o){
  var inp=o.input, list=o.list, note=o.note, items=null, hits=[], act=-1;
  function norm(s){ return (s||'').toLowerCase().replace(/ä/g,'ae').replace(/ö/g,'oe').replace(/ü/g,'ue').replace(/ß/g,'ss')
    .replace(/[^a-z0-9µ%+]+/g,' ').trim(); }
  function esc(s){ return String(s).replace(/[&<>"]/g,function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function prep(){
    if(items)return;
    items=o.items().map(function(it){ it.nt=norm(it.title); it.nk=norm((it.keys||[]).join(' ')); it.nx=norm(it.text); it.raw=(it.text||'').replace(/\s+/g,' ').trim(); return it; });
  }
  /* „eloxieren“ findet „eloxal“, „beschichtungen“ findet „beschichtung“ */
  function stems(t){ var r=[t]; if(t.length>5){ r.push(t.replace(/(ungen|ieren|en|er|es|e|n|s)$/,'')); } if(t.length>6)r.push(t.slice(0,5)); return r; }
  function hit(hay,t){ var s=stems(t); for(var i=0;i<s.length;i++){ if(s[i]&&hay.indexOf(s[i])>-1) return i===0?1:.6; } return 0; }
  function score(it,toks,whole){
    var sc=0;
    for(var i=0;i<toks.length;i++){
      var t=toks[i], a=hit(it.nt,t), b=hit(it.nk,t), c=hit(it.nx,t);
      if(!a&&!b&&!c) return 0;
      if(a) sc+=(' '+it.nt).indexOf(' '+t)>-1?34:22*a;
      sc+=b*16+c*4;
    }
    if(it.nt.indexOf(whole)===0) sc+=40; else if(it.nt.indexOf(whole)>-1) sc+=20;
    return sc+(it.boost||0);
  }
  function snippet(it,q){
    var txt=it.raw; if(!txt)return '';
    var w=q.toLowerCase().split(/\s+/).filter(Boolean), low=txt.toLowerCase(), pos=-1, len=0;
    for(var i=0;i<w.length&&pos<0;i++){ pos=low.indexOf(w[i]); len=w[i].length; }
    if(pos<0) return esc(txt.slice(0,90))+(txt.length>90?' …':'');
    var a=Math.max(0,pos-38), b=Math.min(txt.length,pos+len+56);
    return (a>0?'… ':'')+esc(txt.slice(a,pos))+'<mark>'+esc(txt.slice(pos,pos+len))+'</mark>'+esc(txt.slice(pos+len,b))+(b<txt.length?' …':'');
  }
  function show(arr,q){
    hits=arr; act=arr.length?0:-1;
    list.innerHTML=arr.map(function(it,i){
      return '<li role="option" id="q-o'+i+'" class="q-hit" data-i="'+i+'" aria-selected="'+(i===act)+'">'+
        '<span class="q-kind">'+esc(it.kind)+'</span><span class="q-title">'+esc(it.title)+'</span>'+
        (q?'<span class="q-snip">'+snippet(it,q)+'</span>':'')+'</li>';
    }).join('');
    list.hidden=!arr.length;
    inp.setAttribute('aria-expanded',arr.length?'true':'false');
    mark();
  }
  function mark(){
    [].forEach.call(list.children,function(li,i){ li.setAttribute('aria-selected',i===act); });
    if(act>-1){ inp.setAttribute('aria-activedescendant','q-o'+act); var el=list.children[act]; if(el&&el.scrollIntoView)el.scrollIntoView({block:'nearest'}); }
    else inp.removeAttribute('aria-activedescendant');
  }
  function run(){
    prep();
    var q=inp.value.trim(); note.textContent='';
    if(!q){ show(o.defaults?items.filter(function(it){return o.defaults.indexOf(it.title)>-1}).sort(function(a,b){return o.defaults.indexOf(a.title)-o.defaults.indexOf(b.title)}):[],''); return; }
    var whole=norm(q), toks=whole.split(' ').filter(Boolean);
    var r=items.map(function(it){ return {it:it,s:score(it,toks,whole)}; }).filter(function(x){return x.s>0})
      .sort(function(a,b){return b.s-a.s}).slice(0,7).map(function(x){return x.it});
    show(r,q);
    if(!r.length) note.textContent='Kein Treffer für „'+q+'“. Versuchen Sie z. B. Eloxal, Labor oder Kontakt.';
  }
  function pick(i){
    var it=hits[i]; if(!it)return;
    inp.value=''; list.hidden=true; hits=[]; inp.setAttribute('aria-expanded','false');
    o.onPick(it);
  }
  inp.addEventListener('input',run);
  inp.addEventListener('focus',run);
  inp.addEventListener('keydown',function(e){
    if(e.key==='ArrowDown'&&hits.length){ e.preventDefault(); act=(act+1)%hits.length; mark(); }
    else if(e.key==='ArrowUp'&&hits.length){ e.preventDefault(); act=(act-1+hits.length)%hits.length; mark(); }
    else if(e.key==='Enter'){ e.preventDefault(); if(!inp.value.trim()&&!hits.length){ note.textContent='Bitte einen Suchbegriff eingeben.'; return; } if(hits.length) pick(act<0?0:act); else run(); }
    else if(e.key==='Escape'&&inp.value){ e.preventDefault(); e.stopPropagation(); inp.value=''; run(); }
  });
  /* mousedown statt click: das Feld behält den Fokus, die Tastatur auf dem Handy klappt nicht vorher zu */
  list.addEventListener('mousedown',function(e){ e.preventDefault(); });
  list.addEventListener('click',function(e){ var li=e.target.closest('.q-hit'); if(li) pick(+li.dataset.i); });
  if(o.form) o.form.addEventListener('submit',function(e){ e.preventDefault(); if(hits.length) pick(act<0?0:act); else { run(); if(!hits.length&&!inp.value.trim()) note.textContent='Bitte einen Suchbegriff eingeben.'; } });
  if(o.button) o.button.addEventListener('click',function(e){ e.preventDefault(); if(hits.length) pick(act<0?0:act); else run(); });
  return { reset:function(){ inp.value=''; list.hidden=true; hits=[]; note.textContent=''; } };
}
/* Text eines Bereichs mit Leerzeichen zwischen den Elementen (textContent klebt Zellen und Zeilen zusammen) */
siteSearch.text=function(el,skip){
  var out=[], w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT,{acceptNode:function(n){
    for(var p=n.parentNode;p&&p!==el;p=p.parentNode){ if(p.nodeName==='SCRIPT'||p.nodeName==='STYLE'||p.nodeName==='SELECT'||(skip&&p.matches&&p.matches(skip))) return NodeFilter.FILTER_REJECT; }
    return NodeFilter.FILTER_ACCEPT; }});
  while(w.nextNode()) out.push(w.currentNode.nodeValue);
  return out.join(' ').replace(/\s+/g,' ').replace(/ ([,.;:)])/g,'$1').trim();
};
