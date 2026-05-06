package model

import "time"

type BaziChart struct {
	PersonalInfo *PersonalInfo `json:"personalInfo,omitempty"`
	FourPillar   *FourPillars  `json:"four_pillars"`
	LuckPillars  *LuckPillars  `json:"luck_pillars"`
}

type PersonalInfo struct {
	Name   string `json:"name"`
	Gender int    `json:"gender"`
}

type FourPillars struct {
	YearPillar  *YearPillar  `json:"year_pillar"`
	MonthPillar *MonthPillar `json:"month_pillar"`
	DayPillar   *DayPillar   `json:"day_pillar"`
	HourPillar  *HourPillar  `json:"hour_pillar"`
}

type LuckPillars struct {
	LuckPillars []*LuckPillar `json:"luck_pillars"`
}

type LuckPillar struct {
	Number        int           `json:"number"`
	HeavenlyStem  HeavenlyStem  `json:"heavenly_stem"`
	EarthlyBranch EarthlyBranch `json:"earthly_branch"`
	GanZhi        GanZhi        `json:"gan_zhi"`
	YearStart     int           `json:"year_start"`
	YearEnd       int           `json:"year_end"`
	Time          time.Time     `json:"time"`
}

type YearPillar struct {
	HeavenlyStem  HeavenlyStem  `json:"heavenly_stem"`
	EarthlyBranch EarthlyBranch `json:"earthly_branch"`
	GanZhi        GanZhi        `json:"gan_zhi"`
	Year          int           `json:"year"`
	LifeCycle     string        `json:"life_cycle"`
}

type MonthPillar struct {
	HeavenlyStem  HeavenlyStem  `json:"heavenly_stem"`
	EarthlyBranch EarthlyBranch `json:"earthly_branch"`
	GanZhi        GanZhi        `json:"gan_zhi"`
	Month         int           `json:"month"`
	LifeCycle     string        `json:"life_cycle"`
}

type DayPillar struct {
	HeavenlyStem  HeavenlyStem  `json:"heavenly_stem"`
	EarthlyBranch EarthlyBranch `json:"earthly_branch"`
	GanZhi        GanZhi        `json:"gan_zhi"`
	Day           int           `json:"day"`
	LifeCycle     string        `json:"life_cycle"`
}

type HourPillar struct {
	HeavenlyStem  HeavenlyStem  `json:"heavenly_stem"`
	EarthlyBranch EarthlyBranch `json:"earthly_branch"`
	GanZhi        GanZhi        `json:"gan_zhi"`
	Hour          TimeOfDay     `json:"hour"`
	LifeCycle     string        `json:"life_cycle"`
}

type GanZhi struct {
	Name         string `json:"name"`
	ElementName  string `json:"element_name"`
	ElementValue int    `json:"element_value"`
}

type TimeOfDay struct {
	Hour   int
	Minute int
}

type HeavenlyStem struct {
	Name      string `json:"name"`
	Value     int    `json:"value"`
	Character string `json:"character"`
	Spelling  string `json:"spelling"`
}

type EarthlyBranch struct {
	Name      string `json:"name"`
	Value     int    `json:"value"`
	Character string `json:"character"`
	Spelling  string `json:"spelling"`
}
