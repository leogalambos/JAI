
(function(){
  function renderMermaid(){
    if(!window.mermaid) return;
    try{
      window.mermaid.initialize({startOnLoad:false,securityLevel:'loose',theme:document.body.getAttribute('data-md-color-scheme')==='slate'?'dark':'neutral'});
      var nodes=document.querySelectorAll('.mermaid:not([data-processed="true"])');
      if(nodes.length) window.mermaid.run({nodes:Array.from(nodes)});
    }catch(e){console.warn('Mermaid rendering failed; deterministic SVG diagrams remain available.',e);}
  }
  if(window.document$ && window.document$.subscribe){window.document$.subscribe(renderMermaid)}
  document.addEventListener('DOMContentLoaded',renderMermaid);
  window.addEventListener('load',renderMermaid);
})();
