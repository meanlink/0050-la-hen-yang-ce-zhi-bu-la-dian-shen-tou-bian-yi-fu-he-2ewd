import {stats,table} from './readout.js';
import {labels} from './wax_scope.js';
export function graph({stage,result:r}){
 const groups=r?[
    ['修补台之间',r.bench_variance,r.sums.bench],
    ['台内接缝之间',r.seam_variance,r.sums.seam],
    ['接缝内重复',r.reading_variance,r.sums.repeat]
 ]:[];
 return stats([['流程阶段',labels[stage]],['总均值 / mm',r?.avg_depth??'—'],['校验',r?(r.requires_recheck?'要求补测':'可放行'):'待计算']])+
  table('不同来源的嵌套成分',['变异来源','方差分量 / mm²','平方和'],groups);
}
