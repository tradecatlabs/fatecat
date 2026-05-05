import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

from _paths import FATE_CORE_SRC_DIR, get_env_file
from branding import attach_branding, get_branding_payload, get_disclaimer_payload
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from utils.timezone import now_cn

if str(FATE_CORE_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(FATE_CORE_SRC_DIR))

try:
    load_dotenv(get_env_file(), override=False)
except FileNotFoundError:
    pass

SERVICE_HOST = os.getenv("FATE_SERVICE_HOST", "0.0.0.0")
SERVICE_PORT = int(os.getenv("FATE_SERVICE_PORT", "8001"))

import db_v2 as db  # noqa: E402
from bazi_calculator import BaziCalculator  # noqa: E402
from fate_core.usecases import PureAnalysisInput, calculate_pure_analysis  # noqa: E402
from liuyao_factors import generate_factor  # noqa: E402
from models import (  # noqa: E402
    BaziData,
    BaziRequest,
    BaziResponse,
    BrandingInfo,
    LiuyaoFactorData,
    LiuyaoFactorRequest,
    LiuyaoFactorResponse,
    Meta,
    TimeInfo,
)
from report_generator import DEFAULT_HIDE as REPORT_HIDE  # noqa: E402

db.ensure_db()

app = FastAPI(title="八字排盘服务", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


def _branding_model() -> BrandingInfo:
    return BrandingInfo(**get_branding_payload())


def _disclaimer_model() -> str:
    return get_disclaimer_payload()


@app.exception_handler(HTTPException)
async def branded_http_exception_handler(_request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=attach_branding(
            {
                "success": False,
                "error": str(exc.detail),
                "statusCode": exc.status_code,
            }
        ),
    )


@app.exception_handler(RequestValidationError)
async def branded_validation_exception_handler(_request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=attach_branding(
            {
                "success": False,
                "error": "请求参数无效",
                "details": exc.errors(),
                "statusCode": 422,
            }
        ),
    )


@app.exception_handler(Exception)
async def branded_exception_handler(_request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=attach_branding(
            {
                "success": False,
                "error": str(exc),
                "statusCode": 500,
            }
        ),
    )


@app.get("/health")
def health():
    return attach_branding({"status": "ok"})


def _parse_bazi_request(req: BaziRequest) -> tuple[datetime, float, float]:
    birth_dt = datetime.strptime(f"{req.birthDate} {req.birthTime}", "%Y-%m-%d %H:%M:%S")
    if not req.birthPlace:
        raise HTTPException(status_code=400, detail="birthPlace 必填（经纬度用于真太阳时/风水/占星）")
    return birth_dt, req.birthPlace.longitude, req.birthPlace.latitude


def _build_bazi_data(result: dict, *, birth_dt: datetime, true_solar_time: datetime | None, timezone: str) -> BaziData:
    major_fortune = dict(result.get("majorFortune", {}))
    major_fortune["pillars"] = [
        {
            **pillar,
            "year": pillar.get("year", pillar.get("startYear")),
        }
        for pillar in major_fortune.get("pillars", [])
        if isinstance(pillar, dict)
    ]

    tz = ZoneInfo(timezone)
    return BaziData(
        timeInfo=TimeInfo(
            inputTime=birth_dt.replace(tzinfo=tz).isoformat(),
            trueSolarTime=true_solar_time.replace(tzinfo=tz).isoformat() if true_solar_time else None,
            lunarDate=f"{result['fourPillars']['year']['fullName']}年",
            solarTerm="",
        ),
        fourPillars=result["fourPillars"],
        hiddenStems=result.get("hiddenStems", {}),
        tenGods=result.get("tenGods", {}),
        fiveElements=result.get("fiveElements", {}),
        dayMaster=result.get("dayMaster", {}),
        majorFortune=major_fortune,
        annualFortune=result.get("annualFortune", []),
        voidBranches=result.get("voidInfo", {}),
    )


@app.post("/api/v1/bazi/simple")
def calculate_bazi_simple(req: BaziRequest):
    """简化八字计算 - 直接返回原始结果"""
    try:
        birth_dt, longitude, latitude = _parse_bazi_request(req)

        calculator = BaziCalculator(
            birth_dt,
            req.gender,
            longitude,
            latitude=latitude,
            name=req.name,
            birth_place=req.birthPlace.name,
            use_true_solar_time=req.options.useTrueSolarTime,
        )
        result = calculator.calculate(hide=REPORT_HIDE)

        return attach_branding({"success": True, "data": result})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/api/v1/bazi/pure-analysis")
def calculate_bazi_pure_analysis(req: BaziRequest):
    """纯命理分析 - 仅返回配置约束下的核心字段。"""
    try:
        birth_dt, longitude, latitude = _parse_bazi_request(req)
        payload = PureAnalysisInput(
            birth_dt=birth_dt,
            gender=req.gender,
            longitude=longitude,
            latitude=latitude,
            name=req.name,
            birth_place=req.birthPlace.name,
            use_true_solar_time=req.options.useTrueSolarTime,
        )
        result = calculate_pure_analysis(payload)
        return attach_branding(
            {
                "success": True,
                "data": result,
                "meta": {
                    "calculatedAt": now_cn().isoformat(),
                    "profile": "pure_analysis",
                },
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/api/v1/bazi/calculate", response_model=BaziResponse)
def calculate_bazi(req: BaziRequest, user_id: str | None = None):
    """计算八字排盘"""
    try:
        birth_dt, longitude, latitude = _parse_bazi_request(req)

        calculator = BaziCalculator(
            birth_dt,
            req.gender,
            longitude,
            latitude=latitude,
            name=req.name,
            birth_place=req.birthPlace.name,
            use_true_solar_time=req.options.useTrueSolarTime,
        )
        result = calculator.calculate(hide=REPORT_HIDE)

        ts_dt = calculator.true_solar_time if req.options.useTrueSolarTime else birth_dt
        data = _build_bazi_data(
            result,
            birth_dt=birth_dt,
            true_solar_time=ts_dt if req.options.useTrueSolarTime else None,
            timezone=req.birthPlace.timezone,
        )

        # 保存到数据库
        record_id = None
        if user_id:
            record_id = db.save_record(
                user_id=user_id,
                biz_type="bazi",
                name=req.name,
                gender=req.gender,
                calendar_type=req.options.calendarType,
                birth_date=req.birthDate,
                birth_time=req.birthTime,
                birth_place=req.birthPlace.name,
                longitude=longitude,
                latitude=latitude,
                dst=0,
                true_solar=1 if req.options.useTrueSolarTime else 0,
                early_zi=1 if req.options.midnightMode == "early" else 0,
                biz_data={"input": req.model_dump(), "result": result},
            )

        return BaziResponse(
            disclaimer=_disclaimer_model(),
            success=True,
            data=data,
            meta=Meta(calculatedAt=now_cn().isoformat(), recordId=record_id),
            branding=_branding_model(),
        )
    except Exception as e:
        return BaziResponse(
            disclaimer=_disclaimer_model(),
            success=False,
            error=str(e),
            meta=Meta(calculatedAt=now_cn().isoformat()),
            branding=_branding_model(),
        )


@app.post("/api/v1/liuyao/factor", response_model=LiuyaoFactorResponse)
def calculate_liuyao_factor(req: LiuyaoFactorRequest):
    """六爻量化因子 - 统一输出结构"""
    try:
        factor = generate_factor(
            item=req.item,
            timestamp=req.timestamp,
            method=req.method,
            seed=req.seed,
            cnts=req.cnts,
            cycle_hint=req.cycleHint,
        )
        data = LiuyaoFactorData(**factor.to_dict())
        return LiuyaoFactorResponse(
            disclaimer=_disclaimer_model(),
            success=True,
            data=data,
            meta=Meta(calculatedAt=now_cn().isoformat(), algorithm="liuyao-divicast", version="1.0.0"),
            branding=_branding_model(),
        )
    except Exception as e:
        return LiuyaoFactorResponse(
            disclaimer=_disclaimer_model(),
            success=False,
            error=str(e),
            meta=Meta(calculatedAt=now_cn().isoformat(), algorithm="liuyao-divicast", version="1.0.0"),
            branding=_branding_model(),
        )


@app.get("/api/v1/records/{record_id}")
def get_record(record_id: int):
    """获取记录"""
    record = db.get_record(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    return attach_branding({"success": True, "data": record})


@app.get("/api/v1/user/{user_id}/records")
def get_user_records(user_id: str, biz_type: str = None, limit: int = 10):
    """获取用户记录"""
    records = db.get_user_records(user_id, biz_type, limit)
    return attach_branding({"success": True, "data": records, "total": len(records)})


@app.delete("/api/v1/records/{record_id}")
def delete_record(record_id: int):
    """删除记录"""
    if db.delete_record(record_id):
        return attach_branding({"success": True})
    raise HTTPException(status_code=404, detail="Not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=SERVICE_HOST, port=SERVICE_PORT)
