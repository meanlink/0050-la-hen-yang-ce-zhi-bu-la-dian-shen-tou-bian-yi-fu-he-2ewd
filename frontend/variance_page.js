import {waitJob} from './base.js';
import {intro} from './readout.js';
import {feedback,onSubmit} from './submit.js';
import {batches,data,save} from './wax_client.js';
import {choose} from './wax_scope.js';
import {graph} from './component_readout.js';
export async function render(outlet,user){
 const list=await batches();
 outlet.innerHTML=`${intro('嵌套变异','仅在三台、每台两缝、每缝两次证据齐备后封存。方差说明返工应先排查哪一层。扣留批只补测涉事接缝，其余读数照用。')}
 <form class="toolrow">${choose(list)}${user.role==='reviewer'?'<button>锁定并拆解</button>':''}${feedback}</form><div class="split"><div class="est band"></div>
 <aside class="rulebook"><h2>放行边界</h2><p>台间分量不得超过 0.15 mm²，均值不得超过 1.20 mm。</p><h2>扣留复算</h2><p>扣留批补测涉事接缝后在此重算；达标即恢复交接，不达标继续停在扣留。</p></aside></div>`;
 const selector=outlet.querySelector('select');
 async function draw(){if(selector.value)outlet.querySelector('.est').innerHTML=graph(await data(selector.value,'variance'));}
 selector.onchange=draw;
 onSubmit(outlet.querySelector('form'),async()=>{let task=await save(selector.value,'variance');await waitJob(task.job_id);await draw();return '方差拆解已生成';});
 await draw();
}
