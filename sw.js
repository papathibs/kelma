const V='kelma-v39';
const CORE=['./','index.html','guide.html','instructions.txt','jszip.min.js','manifest.webmanifest','icon-180.png','icon-192.png','icon-512.png','setup/1-projects.jpg','setup/2-new-project.jpg','setup/3-name.jpg','setup/4-pin.jpg','setup/5-instructions.jpg','setup/6-paste.jpg','setup/starter.zip','setup/h1-menu.jpg','setup/h2-share.jpg','setup/h3-add.jpg','setup/w1-forward.jpg','setup/w2-share.jpg','setup/w3-copy.jpg','setup/x1-group.jpg','setup/x2-export.jpg','setup/x3-allmedia.jpg','setup/x4-clear.jpg','setup/x5-clearall.jpg'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(CORE)));self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
  const r=e.request;if(r.method!=='GET')return;const u=new URL(r.url);
  if(u.origin===location.origin){
    if(r.mode==='navigate'){e.respondWith(fetch(r).then(res=>{const cp=res.clone();caches.open(V).then(c=>c.put(r,cp));return res}).catch(()=>caches.match(r,{ignoreSearch:true}).then(m=>m||caches.match('index.html'))));return}
    e.respondWith(caches.match(r).then(m=>m||fetch(r)));return}
  if(u.hostname==='fonts.googleapis.com'||u.hostname==='fonts.gstatic.com'){
    e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{const cp=res.clone();caches.open(V).then(c=>c.put(r,cp));return res})))}
});
