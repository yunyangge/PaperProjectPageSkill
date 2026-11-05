/* Original study player. Media records and provenance are supplied separately. */
const data = JSON.parse(document.querySelector('#media-data').textContent);
const records = new Map(data.media.map(m => [m.id, m]));
const time = s => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`;
function card(id, comparison = false) {
  const m = records.get(id);
  const figure = document.createElement('figure');
  figure.className = 'media-card';
  const video = document.createElement('video');
  video.poster = m.poster; video.preload = 'none'; video.playsInline = true;
  video.controls = false; video.muted = true;
  video.dataset.source = m.file; video.dataset.id = id;
  video.setAttribute('aria-label', m.title);
  const caption = document.createElement('figcaption');
  const title = document.createElement('strong'); title.textContent = m.title;
  const spec = document.createElement('span'); spec.className = 'meta';
  spec.textContent = `${m.width} × ${m.height} · ${time(m.duration)} · ${m.fps} fps playback`;
  caption.append(title, spec);
  const button = document.createElement('button');
  button.className = 'load-video'; button.textContent = comparison ? `Load ${m.title}` : 'Play video';
  const state = document.createElement('span'); state.className = 'player-state';
  state.setAttribute('aria-live', 'polite');
  const link = document.createElement('a'); link.href = m.source; link.target = '_blank'; link.rel = 'noopener'; link.textContent = 'Original clip ↗';
  const actions = document.createElement('div'); actions.className = 'media-actions'; actions.append(button, state, link);
  button.onclick = async () => {
    state.textContent = 'Loading…';
    try { await ready(video); if(!video.isConnected) return; await video.play(); } catch { state.textContent = 'Unable to play. Retry or open original.'; }
  };
  video.addEventListener('error', () => {state.textContent = 'Video unavailable. Retry or open original.'; button.textContent = 'Retry video';});
  video.addEventListener('playing', () => {state.textContent = ''; button.hidden = true;});
  video.addEventListener('canplay', () => {video.controls = true;});
  if(comparison) figure.append(caption,video,actions);
  else figure.append(video,caption,actions);
  if (m.cue) {const p = document.createElement('p'); p.className='cue';p.textContent=m.cue;figure.append(p);}
  if (!comparison) {
    const details = document.createElement('details');
    const summary = document.createElement('summary'); summary.textContent = 'Read full prompt';
    const p = document.createElement('p'); p.textContent = m.prompt;details.append(summary,p);figure.append(details);
  }
  if(!comparison) {
    const observer = new IntersectionObserver(entries => {if (!entries[0].isIntersecting) video.pause();}, {threshold:0});
    observer.observe(figure);
  }
  return figure;
}
function ready(video) {
  if (video.readyState >= 3 && !video.error) return Promise.resolve();
  return new Promise((resolve,reject) => {
    const timer=setTimeout(() => finish(new Error('timeout')),15000);
    function finish(error) {clearTimeout(timer);video.removeEventListener('canplay',ok);video.removeEventListener('error',bad);error?reject(error):resolve();}
    const ok=()=>finish(); const bad=()=>finish(new Error('media'));
    video.addEventListener('canplay',ok,{once:true});video.addEventListener('error',bad,{once:true});
    if(!video.src || video.error) {video.src=video.dataset.source;video.load();}
  });
}
document.querySelectorAll('[data-media]').forEach(el=>el.append(card(el.dataset.media)));
const root=document.querySelector('#comparison');
let epoch=0, group=[], playing=false, end=0;
const status=root.querySelector('[role=status]');
const timeline=root.querySelector('input[type=range]');
const stamp=root.querySelector('output');
function pause() {playing=false;group.forEach(v=>v.pause());root.querySelector('[data-action=play]').textContent='Play together';}
function select(index) {
  epoch++;pause();
  group.forEach(v=>{v.removeAttribute('src');v.load();});
  const config=data.comparisons[index];
  const grid=root.querySelector('.compare-grid');grid.replaceChildren(...config.media.map(id=>card(id,true)));
  group=[...grid.querySelectorAll('video')];end=Math.min(...config.media.map(id=>records.get(id).duration));
  timeline.max=end;timeline.value=0;stamp.textContent=`0:00 / ${time(end)}`;
  root.querySelector('.shared-prompt').textContent=config.prompt;
  const checkpoints=root.querySelector('.checkpoints');
  if(checkpoints) {
    checkpoints.replaceChildren(...[0,20,40,59].filter(t=>t<end).map(t=>{
      const b=document.createElement('button');b.textContent=`${time(t)}`;b.setAttribute('aria-label',`Inspect both videos at ${time(t)}`);b.onclick=()=>seek(t);return b;
    }));
  }
  root.querySelectorAll('[data-prompt]').forEach((b,i)=>b.setAttribute('aria-pressed',i===index?'true':'false'));
  status.textContent='Ready. Videos load on play.';
  group.forEach(v=>v.addEventListener('timeupdate',()=>{
    if(v===group[0]) {timeline.value=v.currentTime;stamp.textContent=`${time(v.currentTime)} / ${time(end)}`;}
    if(v.currentTime>=end-.08 && playing) {pause();status.textContent='Comparison finished. Replay to start again.';}
  }));
  group.forEach(v=>v.addEventListener('pause',()=>{
    if(playing) {epoch++;pause();status.textContent='Paused. Use Play together to resume the group.';}
  }));
}
async function play() {
  if(playing){epoch++;pause();status.textContent='Paused.';return;}
  const token=++epoch, active=[...group];status.textContent='Loading comparison…';
  const results=await Promise.allSettled(active.map(ready));
  if(token!==epoch) return;
  if(results.some(r=>r.status==='rejected')) {pause();status.textContent='A clip could not load. Retry, or play available clips individually.';return;}
  if(active[0].currentTime>=end-.1) active.forEach(v=>v.currentTime=0);
  const started=await Promise.allSettled(active.map(v=>v.play()));
  if(token!==epoch) {active.forEach(v=>v.pause());return;}
  if(started.some(r=>r.status==='rejected')) {pause();status.textContent='Playback blocked. Retry using the video controls.';return;}
  playing=true;root.querySelector('[data-action=play]').textContent='Pause together';status.textContent='Coordinated playback · not frame-locked';
}
root.querySelectorAll('[data-prompt]').forEach((b,i)=>b.onclick=()=>select(i));
root.querySelector('[data-action=play]').onclick=play;
async function seek(value,restart=false) {
  const token=++epoch, active=[...group], resume=playing;pause();status.textContent='Seeking…';
  const results=await Promise.allSettled(active.map(ready));
  if(token!==epoch)return;
  if(results.some(r=>r.status==='rejected')){status.textContent='Unable to seek all clips. Retry loading.';return;}
  const sought=await Promise.allSettled(active.map(v=>seekVideo(v,value)));
  if(token!==epoch)return;
  if(sought.some(r=>r.status==='rejected')){status.textContent='A clip cannot reach that time yet. Try after it loads, or open the original.';return;}
  timeline.value=value;stamp.textContent=`${time(value)} / ${time(end)}`;status.textContent='Paused at selected time.';
  if(resume||restart) await play();
}
function seekVideo(video,value) {
  const target=Math.min(value,Math.max(0,video.duration-.05));
  if(Math.abs(video.currentTime-target)<.05)return Promise.resolve();
  return new Promise((resolve,reject)=>{
    const timer=setTimeout(()=>finish(new Error('seek timeout')),10000);
    const finish=error=>{clearTimeout(timer);video.removeEventListener('seeked',done);video.removeEventListener('error',bad);error?reject(error):resolve();};
    const done=()=>finish(Math.abs(video.currentTime-target)<.25?null:new Error('seek not reached'));
    const bad=()=>finish(new Error('media'));
    video.addEventListener('seeked',done,{once:true});video.addEventListener('error',bad,{once:true});
    video.currentTime=target;
  });
}
root.querySelector('[data-action=restart]').onclick=()=>seek(0,true);
timeline.addEventListener('change',()=>seek(Number(timeline.value)));
new IntersectionObserver(entries=>{if(!entries[0].isIntersecting){epoch++;pause();}}, {threshold:0}).observe(root);
document.addEventListener('visibilitychange',()=>{if(document.hidden){epoch++;pause();document.querySelectorAll('video').forEach(v=>v.pause());}});
select(0);
