// Timed prompt sequence, supplied by the author gallery (six ten-second segments).
const interactive=document.querySelector('#interactive');
const interactiveVideo=interactive.querySelector('video');
const promptList=records.get('interactive').prompts;
const list=interactive.querySelector('.all-prompts');
promptList.forEach((p,i)=>{const li=document.createElement('li');li.textContent=`${i*10}–${(i+1)*10}s: ${p}`;list.append(li);});
let promptEpoch=0;
const chapters=interactive.querySelector('.chapters');
promptList.forEach((p,i)=>{
  const b=document.createElement('button');b.textContent=`${i*10}s`;b.setAttribute('aria-label',`Inspect prompt ${i+1} at ${i*10} seconds`);
  b.onclick=async()=>{
    const token=++promptEpoch;interactiveVideo.pause();
    interactive.querySelector('.active-prompt').textContent='Loading selected moment…';
    try{await ready(interactiveVideo);if(token!==promptEpoch)return;await seekVideo(interactiveVideo,i*10);if(token===promptEpoch)showPrompt(i);}
    catch{interactive.querySelector('.active-prompt').textContent='Video could not load. Retry the selected moment or open the original clip.';}
  };chapters.append(b);
});
function showPrompt(i){interactive.querySelector('.active-prompt').textContent=`${i*10}–${(i+1)*10}s · ${promptList[i]}`;[...chapters.children].forEach((b,j)=>b.setAttribute('aria-current',String(i===j)));}
interactiveVideo.addEventListener('timeupdate',()=>showPrompt(Math.min(5,Math.floor(interactiveVideo.currentTime/10))));
showPrompt(0);
// The multi-prompt result has its own sequence disclosure, not an empty single prompt.
interactive.querySelector('.media-card details').remove();
