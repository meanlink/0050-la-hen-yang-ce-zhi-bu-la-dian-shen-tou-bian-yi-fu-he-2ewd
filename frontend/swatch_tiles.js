import {h} from './base.js';
export function swatches(data) {
 const grouped=Object.groupBy(data,row=>row.seam);
 return `<div class="swatch-roll">${Object.entries(grouped).map(([name,rows])=>`<article class="swatch"><h2>${h(name)}</h2><p>${h(rows[0].bench)} 台 · ${h(rows[0].weave)}</p><small>${rows.filter(r=>r.pass).length}/2 次计量</small></article>`).join('')}</div>`;
}
