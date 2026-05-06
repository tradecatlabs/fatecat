[![GitHub release](https://img.shields.io/github/tag/tommitoan/bazica.svg?label=latest)](https://github.com/tommitoan/bazica/releases)
[![Go Reference](https://pkg.go.dev/badge/github.com/tommitoan/bazica.svg)](https://pkg.go.dev/github.com/tommitoan/bazica)
[![Go Report Card](https://goreportcard.com/badge/github.com/tommitoan/bazica)](https://goreportcard.com/report/github.com/tommitoan/bazica)
[![License](https://img.shields.io/badge/license-MIT-cyan)](https://github.com/tommitoan/bazica/blob/master/LICENSE)

<p align="center">
  <img style="float: right;" src="./Images/bazica-gopher.png" width=400>
</p>

# Bazica (Ba-zi Chart Calculator) 
Convert Solar Calendar to Bazi Chart (Chinese astrology) with the year, month, day and hour of birth information (in Go)

<div align="center">
  <img alt="Demo" src="./Images/bazica-screen.png" />
</div>

<h3 align="center">
  Demo Website<br/>
  <a href="https://bazica-web.tommitoan.com/" target="_blank">bazica-web.tommitoan.com</a>
</h3>

## Getting started with bazica 
### Prerequisites

- **[Go](https://go.dev/)**: any one of the **three latest major** [releases](https://go.dev/doc/devel/release) (we test it with these).

### Importing Bazica

With [Go module](https://github.com/golang/go/wiki/Modules) support, simply add the following import

```
import "github.com/tommitoan/bazica"
```

to your code, and then `go [build|run|test]` will automatically fetch the necessary dependencies.

Otherwise, run the following Go command to install the `bazica` package:

```sh
go get -u github.com/tommitoan/bazica@latest

go mod vendor # For fetching full model
```

## Get Data 

> [!CAUTION]
> You'll need to manually copy the relevant JSON files from the `data` folder into your project to utilize the data within your application.

This module provides data related to solar terms, zodiac signs, and the 60-year era cycle.

For your convenience, the data is also summarized in JSON files and located in the `data` folder.

To use this module:  
Clone or copy this repository to your project directory.
Access the JSON files located in the data folder.

Example:
```
Before Install              
├── your_project_folder
│   ├── app
│   ├── main.go
│   ├── go.mod

After Install and Clone `data` folder
├── your_project_folder
│   ├── app
│   ├── data
│   │   ├── lunar-new-year.json
│   │   ├── solar-term.json
│   │   ├── ...(updating)...
│   ├── main.go
│   ├── go.mod
```

## How to use

```go
package main

import (
	"encoding/json"
	"fmt"
	"github.com/tommitoan/bazica"
	"time"
)

func main() {
	// Calculate current ba-zi chart
	loc, _ := time.LoadLocation("Asia/Ho_Chi_Minh")
	now := time.Now()
	gender := 0 // 0 = female & 1 = male
	
	/* Example: 
	Time to calculate: 1990-12-31 6:30 - Timezone: HoChiMinh / Vietnam - Gender: Male
	loc, _ := time.LoadLocation("Asia/Ho_Chi_Minh")
	now := time.Date(1990, time.Month(12), 31, 6, 30, 0, 0, loc)
	gender := 1
	*/

	chart, err := bazica.GetBaziChart(now, loc, gender)
	if err != nil {
		fmt.Println(err)
	}
	jsonData, _ := json.Marshal(chart)
	fmt.Println(string(jsonData))
}
```
## Note
### Data Input Limitations:
Due to the specific calculations and algorithms used in this package, it is currently designed to handle date inputs ranging from January 1, 1900, to December 31, 2100.   
Dates before 1900 or after 2100 may fall outside the scope of supported calendar systems or lead to inaccurate results.

If you require calculations for dates outside this range, please consider alternative libraries or solutions.

###  Ho Chi Minh City 1975
Ho Chi Minh City (formerly Saigon) has gone through time zone changes throughout history. Notably:  
Before 1975: South Vietnam (including Saigon) used UTC+8.  
After 1975: The unified Vietnam adopted UTC+7.

## References

This project drew inspiration and information from the following sources:

* **[Thời Gian](https://www.thoigian.com.vn/)** - A comprehensive resource for understanding the Vietnamese calendar system.
* **[Chinese Fortune Calendar](https://www.chinesefortunecalendar.com/)** - Provided insights into the Chinese calendar, calculations, and cultural significance.


### Document
https://www.geomancy.net/forums/topic/10229-understand-the-chinese-lunar-and-xia-calendar-in-ba-zi-four-pillars-used-by-various-masters-and-why-not-to-totally-depend-on-just-the-xia-hsia-seasonal-solar-calendar-alone/

For a given date and time of birth, the Hsia Calendar is used to obtain the Heavenly Stems and Earthly Branches with which to construct the Four Pillars of Destiny (四柱) of a person. 
The Four Pillars of Destiny are also known as the Ba Zi (八字), literally the Eight Characters of a person's birth. 
In ancient China, one use of this form of divination was to select a suitable marriage partner.

The Four Pillars of Destiny are the Year Pillar, the Month Pillar, the Day Pillar and the Hour Pillar. 
Each Pillar is made up of two components, namely the Heavenly Stem and the Earthly Branch, both of which are read from the Hsia Calendar.

The Hsia Calendar is also used in various types of Feng Shui, or Chinese Geomancy, such as the Flying Star Feng Shui.

A ba zi chart done with mixed Lunar & Seasonal (Solar Term) Calendar will look like this:- 

```
Date time: 2024-07-05 22:00 UTC+7 (Vietnam)  

Year: Yang Wood - Dragon (Lunar Calendar Year)  
Month: Yang Metal - Horse (Solar-Term Calendar Month)  
Day: Yang Metal - Horse (Lunar Calendar Day)   
Hour: Yin Wood - Pig (Zodiac Hour)
```


