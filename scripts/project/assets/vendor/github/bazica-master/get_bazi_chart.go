package bazica

import (
	"github.com/tommitoan/bazica/internal/fourpillars"
	"github.com/tommitoan/bazica/internal/luckpillars"
	"github.com/tommitoan/bazica/internal/ultis"
	"github.com/tommitoan/bazica/model"
	"time"
)

func GetBaziChart(dateTime time.Time, loc *time.Location, gender int, prefixPath ...string) (*model.BaziChart, error) {
	var baziChart model.BaziChart

	var path string
	if len(prefixPath) != 0 {
		path = prefixPath[0]
	}

	fourPillar, passed, remaining, err := fourpillars.GetFourPillars(dateTime, loc, path)
	if err != nil {
		return nil, err
	}
	baziChart.FourPillar = ultis.GetLifeCycleFromFourPillar(fourPillar)

	lucksPillar, err := luckpillars.GetLuckPillars(fourPillar, gender, passed, remaining, dateTime, path)
	if err != nil {
		return nil, err
	}
	baziChart.LuckPillars = lucksPillar

	return &baziChart, nil
}
