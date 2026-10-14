const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'knowledge/index.html'),'utf8');
test('knowledge graph has seven reachable notes and reciprocal related links',()=>{
 const notes=[...html.matchAll(/<article id="([^"]+)"[\s\S]*?<\/article>/g)];
 assert.equal(notes.length,7);
 const graph=new Map(notes.map(m=>[m[1],[...m[0].matchAll(/href="#([^"]+)"/g)].map(x=>x[1]).filter(x=>x!=='main-content')]));
 for(const [id,related] of graph){
  assert.ok(html.slice(0,html.indexOf('<article')).includes(`href="#${id}"`),`${id} indexed`);
  for(const other of related)assert.ok(graph.get(other)?.includes(id),`${id} reciprocated by ${other}`);
 }
});
test('every local knowledge link resolves including fragments',()=>{
 for(const match of html.matchAll(/href="([^"]+)"/g)){
  const url=match[1];if(/^https?:/.test(url))continue;
  const [relative,fragment]=url.split('#');
  let destination=relative?.startsWith('/') ? path.join(root,relative.slice(1)) : path.resolve(root,'knowledge',relative||'index.html');
  if(fs.statSync(destination).isDirectory())destination=path.join(destination,'index.html');
  assert.ok(fs.existsSync(destination),url);
  if(fragment)assert.ok(fs.readFileSync(destination,'utf8').includes(`id="${fragment}"`),url);
 }
});
test('knowledge has discovery metadata and public evidence for every note',()=>{
 assert.match(html,/<link rel="canonical" href="https:\/\/ccancellieri.github.io\/knowledge\/">/);
 assert.match(fs.readFileSync(path.join(root,'sitemap.xml'),'utf8'),/https:\/\/ccancellieri.github.io\/knowledge\//);
 for(const match of html.matchAll(/<article[\s\S]*?<\/article>/g)){
  assert.match(match[0],/<h3>Public sources<\/h3>/);
  assert.match(match[0],/<h3>Choice and tradeoff<\/h3>/);
 }
 assert.match(fs.readFileSync(path.join(root,'index.html'),'utf8'),/href="\/knowledge\/"/);
});
