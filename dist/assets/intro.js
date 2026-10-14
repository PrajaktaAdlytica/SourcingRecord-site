(()=>{'use strict';
const root=document.getElementById('intro'),video=document.getElementById('intro-video');if(!root||!video)return;
const play=document.getElementById('intro-play'),hero=document.getElementById('home-hero'),status=document.getElementById('intro-status'),reduce=matchMedia('(prefers-reduced-motion: reduce)');let allowAdvance=false,finished=false;
function goToHero(){allowAdvance=false;video.pause();window.scrollTo({top:Math.ceil(window.scrollY+root.getBoundingClientRect().bottom),behavior:reduce.matches?'instant':'smooth'});hero.focus({preventScroll:true});}
async function start(replay=false){if(replay||video.ended){video.currentTime=0;finished=false;}allowAdvance=true;try{await video.play();status.textContent='Intro playing. You can skip to the homepage at any time.';}catch{allowAdvance=false;play.textContent='Play intro';status.textContent='Select Play intro, or Enter website to continue.';}}
play.addEventListener('click',()=>{if(video.paused)start(finished);else{video.pause();allowAdvance=false;}});
video.addEventListener('play',()=>{play.textContent='Pause intro';});video.addEventListener('pause',()=>{play.textContent=finished?'Replay intro':'Play intro';});
video.addEventListener('ended',()=>{finished=true;play.textContent='Replay intro';const visible=root.getBoundingClientRect().bottom>innerHeight*.5;if(allowAdvance&&visible)goToHero();});
video.addEventListener('error',()=>{allowAdvance=false;status.textContent='The film could not load. Enter website to continue.';play.textContent='Retry intro';});
document.querySelectorAll('[data-intro-skip]').forEach(el=>el.addEventListener('click',e=>{e.preventDefault();goToHero();}));
document.querySelectorAll('[data-intro-replay]').forEach(el=>el.addEventListener('click',e=>{e.preventDefault();root.scrollIntoView({behavior:reduce.matches?'instant':'smooth'});play.focus({preventScroll:true});start(true);}));
new IntersectionObserver(([entry])=>{if(!entry.isIntersecting&&!video.paused){allowAdvance=false;video.pause();}},{threshold:0}).observe(root);
document.addEventListener('visibilitychange',()=>{if(document.hidden){allowAdvance=false;video.pause();}});
// One playback per page arrival; returning by scrolling never restarts the film.
if(!reduce.matches&&!location.hash)start();
})();
