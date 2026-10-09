
function aiHouseTunePrimarySidebar(){
  const sidebar=document.querySelector('.md-sidebar--primary');
  const wrap=sidebar?.querySelector('.md-sidebar__scrollwrap');
  const content=document.querySelector('.md-content__inner');
  if(!sidebar||!wrap||!content)return;
  sidebar.classList.remove('ai-sidebar-needs-scroll');
  const header=document.querySelector('.md-header');
  const hh=header?header.getBoundingClientRect().height:0;
  const available=Math.max(320,window.innerHeight-hh-24);
  const navHeight=wrap.scrollHeight;
  const contentHeight=content.scrollHeight;
  if(navHeight>available && navHeight>contentHeight+40){
    sidebar.classList.add('ai-sidebar-needs-scroll');
    requestAnimationFrame(()=>{
      const active=wrap.querySelector('.md-nav__link--active, .md-nav__item--active > .md-nav__link');
      if(active){
        const ar=active.getBoundingClientRect(), wr=wrap.getBoundingClientRect();
        if(ar.top<wr.top+20||ar.bottom>wr.bottom-20) active.scrollIntoView({block:'center',behavior:'instant'});
      }
    });
  }
}
if(typeof document$!=='undefined')document$.subscribe(()=>{requestAnimationFrame(aiHouseTunePrimarySidebar)});
document.addEventListener('DOMContentLoaded',aiHouseTunePrimarySidebar);
window.addEventListener('resize',()=>requestAnimationFrame(aiHouseTunePrimarySidebar));
