"""八字排盘数据模型"""

from datetime import datetime
from typing import Any, Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, Field, field_validator

# ========== 请求模型 ==========

ReportSystem = Literal["bazi", "ziwei"]


class BirthPlace(BaseModel):
    name: str = Field(..., description="地点名称")
    longitude: float = Field(..., ge=-180, le=180, description="经度")
    latitude: float = Field(..., ge=-90, le=90, description="纬度")
    timezone: str = Field(..., description="IANA 时区")
    locationId: str | None = Field(default=None, description="稳定地点 ID")
    coordinateSystem: Literal["WGS84"] = Field(default="WGS84", description="坐标系")
    coordinatePrecision: str | None = Field(default=None, description="坐标精度来源")

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("timezone 必填，且必须使用 IANA 时区")
        try:
            ZoneInfo(normalized)
        except ZoneInfoNotFoundError as exc:
            raise ValueError("timezone 必须是有效 IANA 时区，例如 Asia/Shanghai") from exc
        return normalized


class BaziOptions(BaseModel):
    useTrueSolarTime: bool = Field(default=True, description="是否使用真太阳时")
    daylightSaving: Literal["auto", "on", "off"] = Field(default="auto", description="夏令时处理")
    midnightMode: Literal["early", "late"] = Field(default="early", description="早晚子时")
    calendarType: Literal["solar", "lunar"] = Field(default="solar", description="输入历法类型")
    reportSystem: ReportSystem = Field(default="bazi", description="Markdown 报告输出体系")
    timeBasis: Literal["local_civil", "beijing_time", "utc"] = Field(
        default="local_civil",
        description="出生钟表口径",
    )
    foldChoice: Literal["earlier", "later"] | None = Field(
        default=None,
        description="夏令时回拨重复时刻选择",
    )


class BaziRequest(BaseModel):
    name: str | None = Field(default=None, description="姓名")
    gender: Literal["male", "female"] = Field(..., description="性别")
    birthDate: str = Field(..., description="出生日期 YYYY-MM-DD")
    birthTime: str = Field(..., description="出生时间 HH:MM 或 HH:MM:SS")
    birthPlace: BirthPlace | None = Field(default=None, description="出生地点")
    options: BaziOptions = Field(default_factory=BaziOptions)

    @field_validator("birthDate")
    @classmethod
    def validate_birth_date(cls, value: str) -> str:
        normalized = value.strip()
        try:
            datetime.strptime(normalized, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("birthDate 必须使用 YYYY-MM-DD 格式") from exc
        return normalized

    @field_validator("birthTime")
    @classmethod
    def validate_birth_time(cls, value: str) -> str:
        normalized = value.strip()
        if len(normalized) == 5:
            normalized = f"{normalized}:00"
        try:
            datetime.strptime(normalized, "%H:%M:%S")
        except ValueError as exc:
            raise ValueError("birthTime 必须使用 HH:MM 或 HH:MM:SS 格式") from exc
        return normalized


# ========== 六爻因子请求模型 ==========


class LiuyaoFactorRequest(BaseModel):
    item: str = Field(..., description="标的名称（交易对/商品名）")
    timestamp: str | None = Field(default=None, description="起卦时间（ISO 格式，可省略）")
    method: Literal["seeded", "random", "manual"] = Field(
        default="seeded",
        description="起卦方式：seeded=可复现，random=随机，manual=手动",
    )
    seed: str | None = Field(default=None, description="可复现 seed（seeded 可选）")
    cnts: list[int] | None = Field(default=None, description="手动起卦铜钱结果（6 个 0-3）")
    cycleHint: Literal["intraday", "1-3d", "1-2w", "1-3m"] | None = Field(default=None, description="强制周期（可选）")


# ========== 响应模型 ==========


class Pillar(BaseModel):
    stem: str = Field(..., description="天干")
    branch: str = Field(..., description="地支")
    fullName: str = Field(..., description="干支全称")
    nayin: str = Field(..., description="纳音")


class FourPillars(BaseModel):
    year: Pillar
    month: Pillar
    day: Pillar
    hour: Pillar


class HiddenStems(BaseModel):
    year: list[str]
    month: list[str]
    day: list[str]
    hour: list[str]


class PillarTenGod(BaseModel):
    stem: str = Field(..., description="天干十神")
    branch: list[str] = Field(..., description="地支藏干十神")


class TenGods(BaseModel):
    year: PillarTenGod
    month: PillarTenGod
    day: PillarTenGod
    hour: PillarTenGod


class ElementStat(BaseModel):
    count: int
    percentage: float
    stems: list[str] = Field(default_factory=list)
    branches: list[str] = Field(default_factory=list)
    items: list[str] = Field(default_factory=list)


class FiveElements(BaseModel):
    wood: ElementStat
    fire: ElementStat
    earth: ElementStat
    metal: ElementStat
    water: ElementStat


class DayMaster(BaseModel):
    stem: str
    element: str
    yinYang: Literal["阳", "阴"]
    strength: Literal[
        "身强",
        "中和偏强",
        "中和",
        "中和偏弱",
        "身弱",
        "旺",
        "偏旺",
        "偏弱",
        "弱",
    ]


class MajorFortunePillar(BaseModel):
    age: int
    year: int | None = None
    stem: str
    branch: str
    fullName: str


class MajorFortune(BaseModel):
    direction: Literal["顺行", "逆行"]
    startAge: int
    startYear: int
    pillars: list[MajorFortunePillar]


class AnnualFortune(BaseModel):
    year: int
    stem: str
    branch: str
    fullName: str


class Spirits(BaseModel):
    auspicious: list[str] = Field(default_factory=list)
    inauspicious: list[str] = Field(default_factory=list)


class TimeInfo(BaseModel):
    inputTime: str
    trueSolarTime: str | None = None
    lunarDate: str
    solarTerm: str


class BaziData(BaseModel):
    timeInfo: TimeInfo
    fourPillars: FourPillars
    hiddenStems: HiddenStems
    tenGods: TenGods
    fiveElements: FiveElements
    dayMaster: DayMaster
    majorFortune: MajorFortune
    annualFortune: list[AnnualFortune]
    spirits: Spirits | None = None
    voidBranches: Any = Field(default_factory=dict)


class Meta(BaseModel):
    calculatedAt: str
    algorithm: str = "traditional"
    version: str = "1.0.0"
    recordId: int | None = None


class BrandingInfo(BaseModel):
    name: str
    heroTitle: str
    sponsorText: str
    tagline: str
    tradecatRepo: str
    fatecatRepo: str
    dexScreenerUrl: str
    xUrl: str
    githubUrl: str
    huggingFaceUrl: str
    geminiGemUrl: str
    ca: str


class BaziResponse(BaseModel):
    disclaimer: str
    success: bool
    data: BaziData | None = None
    error: str | None = None
    meta: Meta
    branding: BrandingInfo


# ========== 六爻因子响应模型 ==========


class LiuyaoFactorData(BaseModel):
    item: str
    timestamp: str
    direction: Literal["up", "down", "neutral"]
    strength: float
    confidence: float
    cycle: Literal["intraday", "1-3d", "1-2w", "1-3m"]
    raw: dict
    explain: list[str]
    source: str
    version: str


class LiuyaoFactorResponse(BaseModel):
    disclaimer: str
    success: bool
    data: LiuyaoFactorData | None = None
    error: str | None = None
    meta: Meta
    branding: BrandingInfo
