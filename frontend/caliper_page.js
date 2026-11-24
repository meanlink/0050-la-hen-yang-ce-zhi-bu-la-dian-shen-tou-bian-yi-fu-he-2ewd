import {intro,stats,table} from './readout.js';
import {feedback,onSubmit,options} from './submit.js';
import {batches,data,save,readingHistory} from './wax_client.js';
import {choose,labels} from './wax_scope.js';
export async function render(outlet,user){
 const list=await batches();
 outlet.innerHTML=`${intro('渗透计量','对同一道接缝登记两个位置的蜡痕深度，按毫米记数。在封存前可替换整对；扣留批只补测涉事接缝。')}<div class="toolrow">${choose(list)}</div><div class="split"><div class="pairs band"></div>
 <div class="stack">${user.role==='operator'?`<form class="entry"><h2>录入成对读数</h2><label>接缝<select name="seam"></select></label><div class="measure-pair">
 <label>第一次<input name="first" type="number" min="0" max="8" step=".01" required></label><label>第二次<input name="second" type="number" min="0" max="8" step=".01" required></label></div>
 <button>保存计量对</button>${feedback}</form>`:''}<div class="history rulebook"></div></div></div>`;
 const selector=outlet.querySelector('[name=batch]');
 async function draw(){
  if(!selector.value)return;
  const [rows,hist]=await Promise.all([data(selector.value,'swatches'),readingHistory(selector.value)]);
  const row=list.find(x=>x.code===selector.value), held=(row?.hold_benches??[]);
  const pairs=Object.groupBy(rows,r=>r.seam);
  outlet.querySelector('.pairs').innerHTML=
   (held.length?stats([['扣留修补台',held.join('、')],['阶段',labels[row.stage]]]):'')+
   table('接缝读数簿',['接缝','处理台','第一次 / mm','第二次 / mm','扣留'],Object.entries(pairs).map(([name,r])=>[name,r[0].bench,r[0].depth??'待录',r[1]?.depth??'待录',held.includes(r[0].bench)?'须补测':'—']));
  const field=outlet.querySelector('[name=seam]');
  if(field)field.innerHTML=options(Object.keys(pairs).map(x=>[x,held.includes(pairs[x][0].bench)?`${x}（涉事，须补测）`:x]));
  outlet.querySelector('.history').innerHTML=hist.history.length?table('已替换的旧读数',['接缝','序次','深度 / mm','原记录时间','替换时间'],
    hist.history.map(h=>[h.seam,h.pass,h.depth,new Date(h.recorded_at).toLocaleString('zh-CN'),new Date(h.retired_at).toLocaleString('zh-CN')])):'<h2>读数留痕</h2><p class="muted">替换整对时旧读数会留档，可在此追查。</p>';
 }
 selector.onchange=draw;
 onSubmit(outlet.querySelector('form'),async body=>{await save(selector.value,'readings',body);await draw();return '成对计量已保存';});
 await draw();
}
