import {intro,table} from './readout.js';
import {feedback,onSubmit,options} from './submit.js';
import {batches,data,save} from './wax_client.js';
import {choose} from './wax_scope.js';
export async function render(outlet,user){
 const list=await batches();
 outlet.innerHTML=`${intro('渗透计量','对同一道接缝登记两个位置的蜡痕深度，按毫米记数。在封存前可替换整对。')}<div class="toolrow">${choose(list)}</div><div class="split"><div class="pairs band"></div>
 ${user.role==='operator'?`<form class="entry"><h2>录入成对读数</h2><label>接缝<select name="seam"></select></label><div class="measure-pair">
 <label>第一次<input name="first" type="number" min="0" max="8" step=".01" required></label><label>第二次<input name="second" type="number" min="0" max="8" step=".01" required></label></div>
 <button>保存计量对</button>${feedback}</form>`:''}</div>`;
 const selector=outlet.querySelector('[name=batch]');
 async function draw(){
  if(!selector.value)return;
  const rows=await data(selector.value,'swatches'), pairs=Object.groupBy(rows,r=>r.seam);
  outlet.querySelector('.pairs').innerHTML=table('接缝读数簿',['接缝','处理台','第一次 / mm','第二次 / mm'],Object.entries(pairs).map(([name,r])=>[name,r[0].bench,r[0].depth??'待录',r[1]?.depth??'待录']));
  const field=outlet.querySelector('[name=seam]');
  if(field)field.innerHTML=options(Object.keys(pairs).map(x=>[x,x]));
 }
 selector.onchange=draw;
 onSubmit(outlet.querySelector('form'),async body=>{await save(selector.value,'readings',body);await draw();return '成对计量已保存';});
 await draw();
}
