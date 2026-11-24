# 蜡痕样册 · 织补蜡点渗透变异复核

按修补接缝保留成对蜡印计量，把变异拆成班组、接缝和同缝测量三段，按结果放行织补批。

**模拟客户**　云间衣物修复社，三张修补台和两位面料复核员

**现有流程**　修补台记录两次渗透测量后直接取总均值。组间偏差被抵消，缺少对照样时也能写放行，修补后实际返件无法对照哪个接缝。

**业务交接**　来源为同种面料的试涂小样、两次测量和织补单。后台计算嵌套变异，复核员凭结果放行或登记补测工单。

## 一日工作剧本

1. 10:00 打开 WB-83，核对各修补台提供的两片接缝小样。
2. 10:15 查看编号 A-1 的成对测量值 0.8 mm、1.0 mm。
3. 10:30 齐备率读数要求每台两接缝，每缝两次相同计量方式。
4. 10:50 复核员冻结试涂，worker 分解台间、台内接缝和同缝变异。
5. 11:00 对均值 0.8 mm 的批次签放行。
6. 11:10 另见批次 WB-82 的台间差异。开补测动作，确认其无法签放行。
7. 11:40 查阅已签放行与须补测批次。

## 算法和演示边界

均衡嵌套方差分析使用各台均值和全局均值、各缝均值和台均值，以及观测值和缝均值的平方差。以自由度换算均方；同缝分量为 MS误差，台内分量为 max(0,(MS接缝−MS误差)/2)，台间分量为 max(0,(MS修补台−MS接缝)/4)。台间分量高于 0.15 mm² 或总均值高于 1.20 mm 时须补测。

目标是复核试涂批次的一致性。渗透单位为毫米，试算只支持均衡设计；开补测单时应复用同面料的新样。

## 快速启动

```sh
cp .env.example .env
docker compose up -d --build --wait
docker compose exec -T backend python -m scripts.seed_demo
```

- 前端浏览器地址为 `http://127.0.0.1:18444`。
- FastAPI 文档地址为 `http://127.0.0.1:19444/docs`。
- PostgreSQL 本地端口为 `17944`。后端与后台 worker 共用数据库事务和 Redis 健康探测。
- 开发 HTML、CSS、ES modules 后运行 `docker compose up -d --build frontend`。Python 代码修改后运行 `docker compose up -d --build backend worker`。
- `SEED_DEMO` 控制自动填充。可改三项宿主端口、`DEMO_PASSWORD`、`JWT_SECRET`、`POSTGRES_PASSWORD`。持久卷保存业务数据和队列状态。停机并保留数据使用 `docker compose down`。
- 技术栈为 Python 3.11、FastAPI、PostgreSQL 16、Redis 7、Nginx 与原生浏览器 JS。后端业务模块、SQL 迁移都在 `backend/`。界面和交互在 `frontend/`。

| 账号 | 密码 | 典型权限 |
|---|---|---|
| operator@demo.local | Demo2026! | 登记成对渗透读数 |
| reviewer@demo.local | Demo2026! | 冻结方差证据并签放行或补测 |
| viewer@demo.local | Demo2026! | 查阅记录和经计算的指标 |

共享角色和任务状态枚举分别位于 `backend/core.py` 的 `ROLES`、`JOB_STATES` 和 `frontend/base.js` 的 `roles`、`jobStates`。数据库检查约束与服务状态以相应 SQL 和模块为准。

许可证见 LICENSE。
