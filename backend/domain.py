from fastapi import APIRouter
from swatch_api import router as router_0
from caliper_api import router as router_1
from variance_api import router as router_2
from repair_api import router as router_3
from fabric_seed import seed
from variance_worker import run as run_job

router = APIRouter(prefix="/api")
router.include_router(router_0)
router.include_router(router_1)
router.include_router(router_2)
router.include_router(router_3)
