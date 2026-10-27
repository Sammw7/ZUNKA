let tipoAtual='musica';
function setType(t,el){tipoAtual=t;document.querySelectorAll('.tab').forEach(b=>b.classList.remove('active'));el.classList.add('active');}
async function baixar(){
 const link=document.getElementById('linkInput').value.trim();
 const s=document.getElementById('status');
 if(!link.includes('http')){s.className='status error';s.textContent='Cola um link válido!';s.classList.remove('hidden');return;}
 s.className='status loading';s.textContent='⏳ Baixando de verdade... aguarde';s.classList.remove('hidden');
 try{
   const r = await fetch('/baixar',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url:link,tipo:tipoAtual})});
   const d = await r.json();
   if(d.ok){s.className='status success';s.textContent='✅ '+d.msg;}
   else{s.className='status error';s.textContent='❌ Erro: '+d.erro;}
 }catch(e){s.className='status error';s.textContent='❌ Erro de conexão';}
}
