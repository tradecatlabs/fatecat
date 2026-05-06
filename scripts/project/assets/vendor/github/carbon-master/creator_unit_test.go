package carbon

import (
	"testing"
	"time"

	"github.com/stretchr/testify/suite"
)

type CreatorSuite struct {
	suite.Suite
}

func TestCreatorSuite(t *testing.T) {
	suite.Run(t, new(CreatorSuite))
}

func (s *CreatorSuite) TestCreateFromStdTime() {
	s.Run("empty timezone", func() {
		c := CreateFromStdTime(time.Now(), "")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("error timezone", func() {
		c := CreateFromStdTime(time.Now(), "xxx")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("without timezone", func() {
		c1 := time.Now()
		s.Equal(c1.Unix(), CreateFromStdTime(time.Now()).Timestamp())

		c2 := time.Now().In(time.Local)
		s.Equal(c2.Unix(), CreateFromStdTime(c2).Timestamp())
		s.Equal(c2.Unix(), CreateFromStdTime(c2, UTC).Timestamp())
	})

	s.Run("with timezone", func() {
		now := time.Now().In(time.Local)
		s.Equal(now.Unix(), CreateFromStdTime(now).Timestamp())
		s.Equal(now.Unix(), CreateFromStdTime(now, UTC).Timestamp())
	})
}

func (s *CreatorSuite) TestCreateFromTimestamp() {
	s.Run("empty timezone", func() {
		c := CreateFromTimestamp(0, "")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("error timezone", func() {
		c := CreateFromTimestamp(0, "xxx")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("without timezone", func() {
		s.Equal("1969-12-31 23:59:59 +0000 UTC", CreateFromTimestamp(-1).ToString())
		s.Equal("1970-01-01 00:00:00 +0000 UTC", CreateFromTimestamp(0).ToString())
		s.Equal("1970-01-01 00:00:01 +0000 UTC", CreateFromTimestamp(1).ToString())
		s.Equal("2022-04-12 03:55:55 +0000 UTC", CreateFromTimestamp(1649735755).ToString())
	})

	s.Run("with timezone", func() {
		s.Equal("1970-01-01 07:59:59 +0800 CST", CreateFromTimestamp(-1, PRC).ToString())
		s.Equal("1970-01-01 08:00:00 +0800 CST", CreateFromTimestamp(0, PRC).ToString())
		s.Equal("1970-01-01 08:00:01 +0800 CST", CreateFromTimestamp(1, PRC).ToString())
		s.Equal("2022-04-12 11:55:55 +0800 CST", CreateFromTimestamp(1649735755, PRC).ToString())
	})
}

func (s *CreatorSuite) TestCreateFromTimestampMilli() {
	s.Run("empty timezone", func() {
		c := CreateFromTimestampMilli(0, "")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("error timezone", func() {
		c := CreateFromTimestampMilli(0, "xxx")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("without timezone", func() {
		s.Equal("1969-12-31 23:59:59.999 +0000 UTC", CreateFromTimestampMilli(-1).ToString())
		s.Equal("1970-01-01 00:00:00 +0000 UTC", CreateFromTimestampMilli(0).ToString())
		s.Equal("1970-01-01 00:00:00.001 +0000 UTC", CreateFromTimestampMilli(1).ToString())
		s.Equal("2022-04-12 03:55:55.981 +0000 UTC", CreateFromTimestampMilli(1649735755981).ToString())
	})

	s.Run("with timezone", func() {
		s.Equal("1970-01-01 07:59:59.999 +0800 CST", CreateFromTimestampMilli(-1, PRC).ToString())
		s.Equal("1970-01-01 08:00:00 +0800 CST", CreateFromTimestampMilli(0, PRC).ToString())
		s.Equal("1970-01-01 08:00:00.001 +0800 CST", CreateFromTimestampMilli(1, PRC).ToString())
		s.Equal("2022-04-12 11:55:55.981 +0800 CST", CreateFromTimestampMilli(1649735755981, PRC).ToString())
	})
}

func (s *CreatorSuite) TestCreateFromTimestampMicro() {
	s.Run("empty timezone", func() {
		c := CreateFromTimestampMicro(0, "")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("error timezone", func() {
		c := CreateFromTimestampMicro(0, "xxx")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("without timezone", func() {
		s.Equal("1969-12-31 23:59:59.999999 +0000 UTC", CreateFromTimestampMicro(-1).ToString())
		s.Equal("1970-01-01 00:00:00 +0000 UTC", CreateFromTimestampMicro(0).ToString())
		s.Equal("1970-01-01 00:00:00.000001 +0000 UTC", CreateFromTimestampMicro(1).ToString())
		s.Equal("2022-04-12 03:55:55.981566 +0000 UTC", CreateFromTimestampMicro(1649735755981566).ToString())
	})

	s.Run("with timezone", func() {
		s.Equal("1970-01-01 07:59:59.999999 +0800 CST", CreateFromTimestampMicro(-1, PRC).ToString())
		s.Equal("1970-01-01 08:00:00 +0800 CST", CreateFromTimestampMicro(0, PRC).ToString())
		s.Equal("1970-01-01 08:00:00.000001 +0800 CST", CreateFromTimestampMicro(1, PRC).ToString())
		s.Equal("2022-04-12 11:55:55.981566 +0800 CST", CreateFromTimestampMicro(1649735755981566, PRC).ToString())
	})
}

func (s *CreatorSuite) TestCreateFromTimestampNano() {
	s.Run("empty timezone", func() {
		c := CreateFromTimestampNano(0, "")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("error timezone", func() {
		c := CreateFromTimestampNano(0, "xxx")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("without timezone", func() {
		s.Equal("1969-12-31 23:59:59.999999999 +0000 UTC", CreateFromTimestampNano(-1).ToString())
		s.Equal("1970-01-01 00:00:00 +0000 UTC", CreateFromTimestampNano(0).ToString())
		s.Equal("1970-01-01 00:00:00.000000001 +0000 UTC", CreateFromTimestampNano(1).ToString())
		s.Equal("2022-04-12 03:55:55.981566888 +0000 UTC", CreateFromTimestampNano(1649735755981566888).ToString())
	})

	s.Run("with timezone", func() {
		s.Equal("1970-01-01 07:59:59.999999999 +0800 CST", CreateFromTimestampNano(-1, PRC).ToString())
		s.Equal("1970-01-01 08:00:00 +0800 CST", CreateFromTimestampNano(0, PRC).ToString())
		s.Equal("1970-01-01 08:00:00.000000001 +0800 CST", CreateFromTimestampNano(1, PRC).ToString())
		s.Equal("2022-04-12 11:55:55.981566888 +0800 CST", CreateFromTimestampNano(1649735755981566888, PRC).ToString())
	})
}

func (s *CreatorSuite) TestCreateFromDateTime() {
	s.Run("empty timezone", func() {
		c := CreateFromDateTime(0, 0, 0, 0, 0, 0, "")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("error timezone", func() {
		c := CreateFromDateTime(0, 0, 0, 0, 0, 0, "xxx")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("without timezone", func() {
		s.Equal("-0001-11-30 00:00:00 +0000 UTC", CreateFromDateTime(0, 0, 0, 0, 0, 0).ToString())
		s.Equal("2020-08-05 13:14:15 +0000 UTC", CreateFromDateTime(2020, 8, 5, 13, 14, 15).ToString())
	})

	s.Run("with timezone", func() {
		s.Equal("-0001-11-30 00:00:00 +0805 LMT", CreateFromDateTime(0, 0, 0, 0, 0, 0, PRC).ToString())
		s.Equal("2020-08-05 13:14:15 +0800 CST", CreateFromDateTime(2020, 8, 5, 13, 14, 15, PRC).ToString())
	})
}

func (s *CreatorSuite) TestCreateFromDateTimeMilli() {
	s.Run("empty timezone", func() {
		c := CreateFromDateTimeMilli(0, 0, 0, 0, 0, 0, 0, "")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("error timezone", func() {
		c := CreateFromDateTimeMilli(0, 0, 0, 0, 0, 0, 0, "xxx")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("without timezone", func() {
		s.Equal("-0001-11-30 00:00:00 +0000 UTC", CreateFromDateTimeMilli(0, 0, 0, 0, 0, 0, 0).ToString())
		s.Equal("2020-08-05 13:14:15.999 +0000 UTC", CreateFromDateTimeMilli(2020, 8, 5, 13, 14, 15, 999).ToString())
	})

	s.Run("with timezone", func() {
		s.Equal("-0001-11-30 00:00:00 +0805 LMT", CreateFromDateTimeMilli(0, 0, 0, 0, 0, 0, 0, PRC).ToString())
		s.Equal("2020-08-05 13:14:15.999 +0800 CST", CreateFromDateTimeMilli(2020, 8, 5, 13, 14, 15, 999, PRC).ToString())
	})
}

func (s *CreatorSuite) TestCreateFromDateTimeMicro() {
	s.Run("empty timezone", func() {
		c := CreateFromDateTimeMicro(0, 0, 0, 0, 0, 0, 0, "")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("error timezone", func() {
		c := CreateFromDateTimeMicro(0, 0, 0, 0, 0, 0, 0, "xxx")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("without timezone", func() {
		s.Equal("-0001-11-30 00:00:00 +0000 UTC", CreateFromDateTimeMicro(0, 0, 0, 0, 0, 0, 0).ToString())
		s.Equal("2020-08-05 13:14:15.999999 +0000 UTC", CreateFromDateTimeMicro(2020, 8, 5, 13, 14, 15, 999999).ToString())
	})

	s.Run("with timezone", func() {
		s.Equal("-0001-11-30 00:00:00 +0805 LMT", CreateFromDateTimeMicro(0, 0, 0, 0, 0, 0, 0, PRC).ToString())
		s.Equal("2020-08-05 13:14:15.999999 +0800 CST", CreateFromDateTimeMicro(2020, 8, 5, 13, 14, 15, 999999, PRC).ToString())
	})
}

func (s *CreatorSuite) TestCreateFromDateTimeNano() {
	s.Run("empty timezone", func() {
		c := CreateFromDateTimeNano(0, 0, 0, 0, 0, 0, 0, "")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("error timezone", func() {
		c := CreateFromDateTimeNano(0, 0, 0, 0, 0, 0, 0, "xxx")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("without timezone", func() {
		s.Equal("-0001-11-30 00:00:00 +0000 UTC", CreateFromDateTimeNano(0, 0, 0, 0, 0, 0, 0).ToString())
		s.Equal("2020-08-05 13:14:15.999999999 +0000 UTC", CreateFromDateTimeNano(2020, 8, 5, 13, 14, 15, 999999999).ToString())
	})

	s.Run("with timezone", func() {
		s.Equal("-0001-11-30 00:00:00 +0805 LMT", CreateFromDateTimeNano(0, 0, 0, 0, 0, 0, 0, PRC).ToString())
		s.Equal("2020-08-05 13:14:15.999999999 +0800 CST", CreateFromDateTimeNano(2020, 8, 5, 13, 14, 15, 999999999, PRC).ToString())
	})
}

func (s *CreatorSuite) TestCreateFromDate() {
	s.Run("empty timezone", func() {
		c := CreateFromDate(0, 0, 0, "")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("error timezone", func() {
		c := CreateFromDate(0, 0, 0, "xxx")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("without timezone", func() {
		s.Equal("-0001-11-30 00:00:00 +0000 UTC", CreateFromDate(0, 0, 0).ToString())
		s.Equal("2020-08-05 00:00:00 +0000 UTC", CreateFromDate(2020, 8, 5).ToString())
	})

	s.Run("with timezone", func() {
		s.Equal("-0001-11-30 00:00:00 +0805 LMT", CreateFromDate(0, 0, 0, PRC).ToString())
		s.Equal("2020-08-05 00:00:00 +0800 CST", CreateFromDate(2020, 8, 5, PRC).ToString())
	})
}

func (s *CreatorSuite) TestCreateFromDateMilli() {
	s.Run("empty timezone", func() {
		c := CreateFromDateMilli(0, 0, 0, 0, "")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("error timezone", func() {
		c := CreateFromDateMilli(0, 0, 0, 0, "xxx")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("without timezone", func() {
		s.Equal("-0001-11-30 00:00:00 +0000 UTC", CreateFromDateMilli(0, 0, 0, 0).ToString())
		s.Equal("2020-08-05 00:00:00.999 +0000 UTC", CreateFromDateMilli(2020, 8, 5, 999).ToString())
	})

	s.Run("with timezone", func() {
		s.Equal("-0001-11-30 00:00:00 +0805 LMT", CreateFromDateMilli(0, 0, 0, 0, PRC).ToString())
		s.Equal("2020-08-05 00:00:00.999 +0800 CST", CreateFromDateMilli(2020, 8, 5, 999, PRC).ToString())
	})
}

func (s *CreatorSuite) TestCreateFromDateMicro() {
	s.Run("empty timezone", func() {
		c := CreateFromDateMicro(0, 0, 0, 0, "")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("error timezone", func() {
		c := CreateFromDateMicro(0, 0, 0, 0, "xxx")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("without timezone", func() {
		s.Equal("-0001-11-30 00:00:00 +0000 UTC", CreateFromDateMicro(0, 0, 0, 0).ToString())
		s.Equal("2020-08-05 00:00:00.999999 +0000 UTC", CreateFromDateMicro(2020, 8, 5, 999999).ToString())
	})

	s.Run("with timezone", func() {
		s.Equal("-0001-11-30 00:00:00 +0805 LMT", CreateFromDateMicro(0, 0, 0, 0, PRC).ToString())
		s.Equal("2020-08-05 00:00:00.999999 +0800 CST", CreateFromDateMicro(2020, 8, 5, 999999, PRC).ToString())
	})
}

func (s *CreatorSuite) TestCreateFromDateNano() {
	s.Run("empty timezone", func() {
		c := CreateFromDateNano(0, 0, 0, 0, "")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("error timezone", func() {
		c := CreateFromDateNano(0, 0, 0, 0, "xxx")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("without timezone", func() {
		s.Equal("-0001-11-30 00:00:00 +0000 UTC", CreateFromDateNano(0, 0, 0, 0).ToString())
		s.Equal("2020-08-05 00:00:00.999999999 +0000 UTC", CreateFromDateNano(2020, 8, 5, 999999999).ToString())
	})

	s.Run("with timezone", func() {
		s.Equal("-0001-11-30 00:00:00 +0805 LMT", CreateFromDateNano(0, 0, 0, 0, PRC).ToString())
		s.Equal("2020-08-05 00:00:00.999999999 +0800 CST", CreateFromDateNano(2020, 8, 5, 999999999, PRC).ToString())
	})
}

func (s *CreatorSuite) TestCreateFromTime() {
	s.Run("empty timezone", func() {
		c := CreateFromTime(0, 0, 0, "")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("error timezone", func() {
		c := CreateFromTime(0, 0, 0, "xxx")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("without timezone", func() {
		s.Equal("00:00:00", CreateFromTime(0, 0, 0).ToTimeString())
		s.Equal("13:14:15", CreateFromTime(13, 14, 15).ToTimeString())
	})

	s.Run("with timezone", func() {
		s.Equal("00:00:00", CreateFromTime(0, 0, 0, PRC).ToTimeString())
		s.Equal("13:14:15", CreateFromTime(13, 14, 15, PRC).ToTimeString())
	})
}

func (s *CreatorSuite) TestCreateFromTimeMilli() {
	s.Run("empty timezone", func() {
		c := CreateFromTimeMilli(0, 0, 0, 0, "")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("error timezone", func() {
		c := CreateFromTimeMilli(0, 0, 0, 0, "xxx")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("without timezone", func() {
		s.Equal("00:00:00", CreateFromTimeMilli(0, 0, 0, 0).ToTimeMilliString())
		s.Equal("13:14:15.999", CreateFromTimeMilli(13, 14, 15, 999).ToTimeMilliString())
	})

	s.Run("with timezone", func() {
		s.Equal("00:00:00", CreateFromTimeMilli(0, 0, 0, 0, PRC).ToTimeMilliString())
		s.Equal("13:14:15.999", CreateFromTimeMilli(13, 14, 15, 999, PRC).ToTimeMilliString())
	})
}

func (s *CreatorSuite) TestCreateFromTimeMicro() {
	s.Run("empty timezone", func() {
		c := CreateFromTimeMicro(0, 0, 0, 0, "")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("error timezone", func() {
		c := CreateFromTimeMicro(0, 0, 0, 0, "xxx")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("without timezone", func() {
		s.Equal("00:00:00", CreateFromTimeMicro(0, 0, 0, 0).ToTimeMicroString())
		s.Equal("13:14:15.999999", CreateFromTimeMicro(13, 14, 15, 999999).ToTimeMicroString())
	})

	s.Run("with timezone", func() {
		s.Equal("00:00:00", CreateFromTimeMicro(0, 0, 0, 0, PRC).ToTimeMicroString())
		s.Equal("13:14:15.999999", CreateFromTimeMicro(13, 14, 15, 999999, PRC).ToTimeMicroString())
	})
}

func (s *CreatorSuite) TestCreateFromTimeNano() {
	s.Run("empty timezone", func() {
		c := CreateFromTimeNano(0, 0, 0, 0, "")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("error timezone", func() {
		c := CreateFromTimeNano(0, 0, 0, 0, "xxx")
		s.True(c.HasError())
		s.Empty(c.ToString())
	})

	s.Run("without timezone", func() {
		s.Equal("00:00:00", CreateFromTimeNano(0, 0, 0, 0).ToTimeNanoString())
		s.Equal("13:14:15.999999999", CreateFromTimeNano(13, 14, 15, 999999999).ToTimeNanoString())
	})

	s.Run("with timezone", func() {
		s.Equal("00:00:00", CreateFromTimeNano(0, 0, 0, 0, PRC).ToTimeNanoString())
		s.Equal("13:14:15.999999999", CreateFromTimeNano(13, 14, 15, 999999999, PRC).ToTimeNanoString())
	})
}
