import {h} from './base.js';
import {intro} from './readout.js';
import {feedback,onSubmit} from './submit.js';
import {batches,data,save} from './wax_client.js';
import {choose} from './wax_scope.js';
export async function render(outlet,user){
 const list=(await batches()).filter(x=>['classified','released','recheck'].includes(x.stage));
 outlet.innerHTML=`${intro('放行补测','合格批交织补台继续处理，超限批签发另起小样的补测。已签凭据附收件人和具体动作。')}<div class="toolrow">${choose(list)}</div><div class="split"><section class="ticket rulebook"></section>
 ${user.role==='reviewer'&&list.length?`<form class="entry"><h2>签发下游动作</h2><label>类型<select name="decision"><option value="release">放行织补</option><option value="recheck">退回补测</option></select></label>
 <label>收件台/人员<input name="destination" required minlength="2"></label><label>工作说明<textarea name="note" required minlength="6"></textarea></label><button>签动作</button>${feedback}</form>`:''}</div>`;
 const selector=outlet.querySelector('[name=batch]');
 async function draw(){
  const record=selector.value?await data(selector.value,'dispatch'):null;
  outlet.querySelector('.ticket').innerHTML=record?`<h2>${record.decision==='release'?'已放行':'已派补测'}</h2><p>${h(record.destination)} · ${h(record.note)}</p><small>${h(record.manager)}</small>`:'<h2>待签审</h2><p>复核员从方差页核对本批的分量。</p>';
 }
 selector.onchange=draw;
 onSubmit(outlet.querySelector('form'),async item=>{await save(selector.value,'dispatch',item);await draw();return '交接动作已签';});
 await draw();
}
