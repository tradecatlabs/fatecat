"""八字排盘数据模型"""

from typing import Any, Literal

from pydantic import BaseModel, Field

# ========== 请求模型 ==========


class BirthPlace(BaseModel):
    name: str = Field(..., description="地点名称")
    longitude: float = Field(..., ge=-180, le=180, description="经度")
    latitude: float = Field(..., ge=-90, le=90, description="纬度")
    timezone: str = Field(default="Asia/Shanghai", description="时区")


class BaziOptions(BaseModel):
    useTrueSolarTime: bool = Field(default=True, description="是否使用真太阳时")
    daylightSaving: Literal["auto", "on", "off"] = Field(default="auto", description="夏令时处理")
    midnightMode: Literal["early", "late"] = Field(default="early", description="早晚子时")
    calendarType: Literal["solar", "lunar"] = Field(default="solar", description="输入历法类型")


class BaziRequest(BaseModel):
    name: str | None = Field(default=None, description="姓名")
    gender: Literal["male", "female"] = Field(..., description="性别")
    birthDate: str = Field(..., description="出生日期 YYYY-MM-DD")
    birthTime: str = Field(..., description="出生时间 HH:MM:SS")
    birthPlace: BirthPlace | None = Field(default=None, description="出生地点")
    options: BaziOptions = Field(default_factory=BaziOptions)


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
