import logging
import os
import secrets
import sys
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

from _paths import FATE_CORE_SRC_DIR, get_env_file
from branding import attach_branding, get_branding_payload, get_disclaimer_payload
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from utils.timezone import now_cn

if str(FATE_CORE_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(FATE_CORE_SRC_DIR))

try:
    load_dotenv(get_env_file(), override=False)
except FileNotFoundError:
    pass

SERVICE_HOST = os.getenv("FATE_SERVICE_HOST", "127.0.0.1")
SERVICE_PORT = int(os.getenv("FATE_SERVICE_PORT", "8001"))
API_TOKEN = os.getenv("FATE_API_TOKEN", "").strip()

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
from prediction_systems import prediction_systems_payload  # noqa: E402
from report_generator import (  # noqa: E402
    build_report_hide,
    generate_full_report,
    normalize_report_system,
    public_birth_place,
)
from web_ui import render_web_report_page  # noqa: E402

db.ensure_db()

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ApiPrincipal:
    role: str
    user_id: str | None = None

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"


def _cors_allow_origins() -> list[str]:
    raw = os.getenv("FATE_CORS_ALLOW_ORIGINS", "").strip()
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def _extract_auth_token(x_api_key: str | None, authorization: str | None) -> str:
    if x_api_key:
        return x_api_key.strip()
    if authorization:
        scheme, _, value = authorization.strip().partition(" ")
        if scheme.lower() == "bearer" and value:
            return value.strip()
    return ""


def _admin_tokens() -> list[str]:
    tokens = [API_TOKEN, os.getenv("FATE_API_ADMIN_TOKEN", "").strip()]
    return [token for token in dict.fromkeys(tokens) if token]


def _user_tokens() -> dict[str, str]:
    raw = os.getenv("FATE_API_USER_TOKENS", "").strip()
    if not raw:
        return {}

    mapping: dict[str, str] = {}
    for item in raw.split(","):
        user_id, sep, token = item.strip().partition(":")
        if sep and user_id.strip() and token.strip():
            mapping[user_id.strip()] = token.strip()
    return mapping


def _require_record_access(x_api_key: str | None, authorization: str | None) -> ApiPrincipal:
    admin_tokens = _admin_tokens()
    user_tokens = _user_tokens()
    if not admin_tokens and not user_tokens:
        raise HTTPException(status_code=403, detail="记录接口未启用")
    supplied = _extract_auth_token(x_api_key, authorization)
    if not supplied:
        raise HTTPException(status_code=403, detail="未授权")
    for token in admin_tokens:
        if secrets.compare_digest(supplied, token):
            return ApiPrincipal(role="admin")
    for user_id, token in user_tokens.items():
        if secrets.compare_digest(supplied, token):
            return ApiPrincipal(role="user", user_id=user_id)
    raise HTTPException(status_code=403, detail="未授权")


def _require_owner_or_admin(principal: ApiPrincipal, user_id: str) -> None:
    if principal.is_admin:
        return
    if principal.user_id == user_id:
        return
    raise HTTPException(status_code=403, detail="无权访问该记录")


app = FastAPI(title="八字排盘服务", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=_cors_allow_origins(), allow_methods=["*"], allow_headers=["*"])


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
    logger.info("API 请求参数校验失败: %s", exc.errors())
    return JSONResponse(
        status_code=422,
        content=attach_branding(
            {
                "success": False,
                "error": "请求参数无效",
                "statusCode": 422,
            }
        ),
    )


@app.exception_handler(Exception)
async def branded_exception_handler(_request, exc: Exception):
    logger.exception("未处理 API 异常")
    return JSONResponse(
        status_code=500,
        content=attach_branding(
            {
                "success": False,
                "error": "服务器内部错误",
                "statusCode": 500,
            }
        ),
    )


@app.get("/health")
def health():
    return attach_branding({"status": "ok"})


@app.get("/web", response_class=HTMLResponse)
def web_report(
    birthDate: str | None = None,
    birthTime: str | None = None,
    birthPlace: str | None = None,
    gender: str | None = None,
    name: str | None = None,
    reportSystem: str | None = None,
):
    """原生 HTML Web 版标准 Markdown 报告。"""
    return render_web_report_page(
        birth_date=birthDate,
        birth_time=birthTime,
        birth_place=birthPlace,
        gender=gender,
        name=name,
        report_system=reportSystem,
    )


@app.get("/api/v1/report/systems")
def list_report_systems():
    """列出当前可用和未来规划的独立输出体系。"""
    return attach_branding({"success": True, "data": {"systems": prediction_systems_payload()}})


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


def _calculate_bazi_raw(req: BaziRequest, *, report_system: str = "bazi") -> tuple[dict, BaziCalculator, datetime]:
    birth_dt, longitude, latitude = _parse_bazi_request(req)
    report_hide = build_report_hide(report_system)
    display_birth_place = public_birth_place(req.birthPlace.name)
    calculator = BaziCalculator(
        birth_dt,
        req.gender,
        longitude,
        latitude=latitude,
        name=req.name,
        birth_place=display_birth_place,
        use_true_solar_time=req.options.useTrueSolarTime,
    )
    result = calculator.calculate(hide=report_hide)
    return result, calculator, birth_dt


@app.post("/api/v1/bazi/simple")
def calculate_bazi_simple(req: BaziRequest):
    """简化八字计算 - 直接返回原始结果"""
    try:
        result, _calculator, _birth_dt = _calculate_bazi_raw(req, report_system="bazi")

        return attach_branding({"success": True, "data": result})
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("简化八字计算失败")
        raise HTTPException(status_code=500, detail="服务器内部错误") from e


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
        logger.exception("纯分析计算失败")
        raise HTTPException(status_code=500, detail="服务器内部错误") from e


@app.post("/api/v1/bazi/calculate", response_model=BaziResponse)
def calculate_bazi(
    req: BaziRequest,
    user_id: str | None = None,
    x_fatecat_api_key: str | None = Header(default=None, alias="X-FateCat-API-Key"),
    authorization: str | None = Header(default=None),
):
    """计算八字排盘"""
    try:
        if user_id:
            principal = _require_record_access(x_fatecat_api_key, authorization)
            _require_owner_or_admin(principal, user_id)
        result, calculator, birth_dt = _calculate_bazi_raw(req, report_system="bazi")

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
                longitude=req.birthPlace.longitude,
                latitude=req.birthPlace.latitude,
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
    except HTTPException:
        raise
    except Exception:
        logger.exception("八字 API 计算失败")
        return BaziResponse(
            disclaimer=_disclaimer_model(),
            success=False,
            error="八字计算失败",
            meta=Meta(calculatedAt=now_cn().isoformat()),
            branding=_branding_model(),
        )


@app.post("/api/v1/report/markdown")
def generate_markdown_report(req: BaziRequest):
    """生成指定体系的 Markdown 报告。"""
    try:
        report_system = normalize_report_system(req.options.reportSystem)
        result, _calculator, _birth_dt = _calculate_bazi_raw(req, report_system=report_system)
        report_hide = build_report_hide(report_system)
        markdown = generate_full_report(result, hide=report_hide, report_system=report_system)
        return attach_branding(
            {
                "success": True,
                "data": {
                    "reportSystem": report_system,
                    "markdown": markdown,
                },
                "meta": {"calculatedAt": now_cn().isoformat()},
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Markdown 报告生成失败")
        raise HTTPException(status_code=500, detail="服务器内部错误") from e


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
    except Exception:
        logger.exception("六爻因子计算失败")
        return LiuyaoFactorResponse(
            disclaimer=_disclaimer_model(),
            success=False,
            error="六爻因子计算失败",
            meta=Meta(calculatedAt=now_cn().isoformat(), algorithm="liuyao-divicast", version="1.0.0"),
            branding=_branding_model(),
        )


@app.get("/api/v1/records/{record_id}")
def get_record(
    record_id: int,
    x_fatecat_api_key: str | None = Header(default=None, alias="X-FateCat-API-Key"),
    authorization: str | None = Header(default=None),
):
    """获取记录"""
    principal = _require_record_access(x_fatecat_api_key, authorization)
    record = db.get_record(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    _require_owner_or_admin(principal, str(record["userId"]))
    return attach_branding({"success": True, "data": record})


@app.get("/api/v1/user/{user_id}/records")
def get_user_records(
    user_id: str,
    biz_type: str = None,
    limit: int = 10,
    x_fatecat_api_key: str | None = Header(default=None, alias="X-FateCat-API-Key"),
    authorization: str | None = Header(default=None),
):
    """获取用户记录"""
    principal = _require_record_access(x_fatecat_api_key, authorization)
    _require_owner_or_admin(principal, user_id)
    records = db.get_user_records(user_id, biz_type, limit)
    return attach_branding({"success": True, "data": records, "total": len(records)})


@app.delete("/api/v1/records/{record_id}")
def delete_record(
    record_id: int,
    x_fatecat_api_key: str | None = Header(default=None, alias="X-FateCat-API-Key"),
    authorization: str | None = Header(default=None),
):
    """删除记录"""
    principal = _require_record_access(x_fatecat_api_key, authorization)
    record = db.get_record(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    _require_owner_or_admin(principal, str(record["userId"]))
    if db.delete_record(record_id):
        return attach_branding({"success": True})
    raise HTTPException(status_code=404, detail="Not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=SERVICE_HOST, port=SERVICE_PORT)
