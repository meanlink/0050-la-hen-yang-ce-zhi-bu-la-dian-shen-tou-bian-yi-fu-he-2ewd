import {intro, table} from './readout.js';
import {feedback, onSubmit, options} from './submit.js';
import {benchOptions, choose, labels} from './wax_scope.js';
import {batches, benchHolds, registerHold, sweepHolds} from './wax_client.js';

const shortStage = stage => labels[stage] ?? stage;

export async function render(outlet, user){
  const list = await batches();
  const ids = list.map(x => x.code);
  const bench = {value:'A'};
  outlet.innerHTML = `${intro('量具失准扣留','一台量具失准会牵连多批织补件。按修补台登记扣留，受影响批次暂停交接，已放行的批次同样停在扣留；各批只补测涉事接缝，其余读数照用。')}
  <div class="split"><div class="stack"><div class="band holds"></div><div class="band batches"></div></div>
   ${user.role==='reviewer'?`<form class="entry sweep"><h2>按修补台登记扣留</h2>
     <label>受影响修补台<select name="bench">${options(benchOptions)}</select></label>
     <label>牵连批次<select name="batches" multiple size="4">${options(ids.map(id=>[id,id]))}</select></label>
     <p class="muted">按住多选；只勾选受同一台量具影响的批次。</p>
     <label>失准说明<textarea name="reason" required minlength="6" maxlength="200"></textarea></label>
     <button>登记扣留</button>${feedback}</form>`:''}
   ${user.role==='reviewer'?`<form class="entry single"><h2>单批补登扣留</h2>
     ${choose(list)}
     <label>受影响修补台<select name="sbench">${options(benchOptions)}</select></label>
     <label>失准说明<textarea name="sreason" required minlength="6" maxlength="200"></textarea></label>
     <button>补登扣留</button>${feedback}</form>`:''}</div>`;

  const holdsBand = outlet.querySelector('.holds');
  const batchesBand = outlet.querySelector('.batches');

  async function draw(){
    const [benchRows, batchRows] = await Promise.all([benchHolds(bench.value), batches()]);
    const active = benchRows[0]?.batches ?? [];
    holdsBand.innerHTML = table(`修补台 ${bench.value} 的未解除扣留`, ['批次','面料','扣留时间','说明','经办'],
      active.map(row => [row.batch, row.fabric, new Date(row.created_at).toLocaleString('zh-CN'), row.reason, row.manager]));
    batchesBand.innerHTML = table('批次交接状态与扣留台', ['批次','面料','阶段','扣留修补台','交接情况'],
      batchRows.map(row => [row.code, row.fabric, shortStage(row.stage),
        (row.hold_benches ?? []).join('、') || '—',
        row.stage==='held' ? '交接暂停，补测涉事接缝后复算' : (row.stage==='released' ? '已放行，可被扣留暂停' : '—')]));
  }

  outlet.querySelector('[name=bench]').onchange = event => { bench.value = event.target.value; draw(); };

  const sweepForm = outlet.querySelector('.sweep');
  onSubmit(sweepForm, async body => {
    const picked = [...sweepForm.querySelector('[name=batches]').selectedOptions].map(item => item.value);
    if (!picked.length) throw new Error('请至少选择一个牵连批次');
    const result = await sweepHolds({bench: body.bench, batches: picked, reason: body.reason});
    bench.value = body.bench;
    await draw();
    const duplicates = result.results.filter(r => r.duplicate).length;
    return duplicates ? `扣留已登记，${duplicates} 个批次已有扣留未重复登记` : '扣留已登记，交接停在扣留';
  });

  onSubmit(outlet.querySelector('.single'), async body => {
    const result = await registerHold(body.batch, {bench: body.sbench, reason: body.sreason});
    bench.value = body.sbench;
    await draw();
    return result.duplicate ? '该批次已在此修补台扣留，未重复登记' : '单批扣留已登记';
  });

  await draw();
}
