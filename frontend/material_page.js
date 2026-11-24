import {intro,stats} from './readout.js';
import {batches,data} from './wax_client.js';
import {choose,labels} from './wax_scope.js';
import {swatches} from './swatch_tiles.js';
export async function render(outlet){
 const list=await batches();
 outlet.innerHTML=`${intro('小样配对','三张修补台各交直纹和斜纹接缝。接缝编号贯穿成对计量、方差分析和下游交接。')}<div class="toolrow">${choose(list)}</div><div class="swatches"></div>`;
 const selector=outlet.querySelector('select');
 async function draw(){const row=list.find(r=>r.code===selector.value);if(row)outlet.querySelector('.swatches').innerHTML=stats([['卷册阶段',labels[row.stage]],['试涂面料',row.fabric]])+swatches(await data(row.code,'swatches'));}
 selector.onchange=draw;await draw();
}
