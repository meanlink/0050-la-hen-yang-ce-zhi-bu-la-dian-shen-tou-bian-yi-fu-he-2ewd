import {options} from './submit.js';
export const labels={sampling:'计量中',sealed:'已封存',classified:'可签审',released:'已放行',recheck:'已派补测',held:'已扣留'};
export const choose=list=>`<label>试涂批次<select name="batch">${options(list.map(x=>[x.code,x.code+' · '+x.fabric]))}</select></label>`;
export const benchOptions=['A','B','C'].map(bench=>[bench,`${bench} 台`]);