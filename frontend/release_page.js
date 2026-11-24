import {h} from './base.js';
import {intro} from './readout.js';
import {feedback,onSubmit} from './submit.js';
import {batches,data,save} from './wax_client.js';
import {choose,labels} from './wax_scope.js';
export async function render(outlet,user){
 const list=(await batches()).filter(x=>['classified','released','recheck','held'].includes(x.stage));
 outlet.innerHTML=`${intro('放行补测','合格批交织补台继续处理，超限批签发另起小样的补测。已签凭据附收件人和具体动作。扣留中的批次交接暂停，补测复算达标后才恢复。')}<div class="toolrow">${choose(list)}</div><div class="split"><section class="ticket rulebook"></section>
 ${user.role==='reviewer'&&list.length?`<form class="entry"><h2>签发下游动作</h2><label>类型<select name="decision"><option value="release">放行织补</option><option value="recheck">退回补测</option></select></label>
 <label>收件台/人员<input name="destination" required minlength="2"></label><label>工作说明<textarea name="note" required minlength="6"></textarea></label><button>签动作</button>${feedback}</form>`:''}</div>`;
 const selector=outlet.querySelector('[name=batch]');
 async function draw(){
  if(!selector.value)return;
  const [records,row]=await Promise.all([data(selector.value,'dispatch'),batches().then(all=>all.find(x=>x.code===selector.value))]);
  const held=row&&(row.hold_benches??[]).length>0;
  const latest=records.at(-1);
  outlet.querySelector('.ticket').innerHTML=`${held?`<p class="muted">修补台 ${h(row.hold_benches.join('、'))} 已扣留，交接暂停；补测涉事接缝并复算达标后才恢复。</p>`:''}`+
   (latest?`<h2>${latest.decision==='release'?'已放行':'已派补测'}</h2><p>${h(latest.destination)} · ${h(latest.note)}</p><small>${h(latest.manager)} · ${new Date(latest.created_at).toLocaleString('zh-CN')}</small>`:'<h2>待签审</h2><p>复核员从方差页核对本批的分量。</p>')+
   (records.length>1?`<details><summary>既有 ${records.length} 张凭据</summary><ol>${records.slice(0,-1).map(r=>`<li>${h(labels[r.decision==='release'?'released':'recheck'])} · ${h(r.destination)} · ${h(r.manager)}</li>`).join('')}</ol></details>`:'');
 }
 selector.onchange=draw;
 onSubmit(outlet.querySelector('form'),async item=>{await save(selector.value,'dispatch',item);await draw();return '交接动作已签';});
 await draw();
}
