import {stats,table} from './readout.js';
import {labels} from './wax_scope.js';
export function graph({stage,result:r,hold_benches:held=[]}){
 const groups=r?[
    ['修补台之间',r.bench_variance,r.sums.bench],
    ['台内接缝之间',r.seam_variance,r.sums.seam],
    ['接缝内重复',r.reading_variance,r.sums.repeat]
 ]:[];
 const verdict=stage==='held'?'扣留中，补测复算达标才恢复交接':(r?(r.requires_recheck?'要求补测':'可放行'):'待计算');
 return stats([['流程阶段',labels[stage]??stage],['总均值 / mm',r?.avg_depth??'—'],['扣留修补台',held.join('、')||'—'],['校验',verdict]])+
  table('不同来源的嵌套成分',['变异来源','方差分量 / mm²','平方和'],groups);
}
