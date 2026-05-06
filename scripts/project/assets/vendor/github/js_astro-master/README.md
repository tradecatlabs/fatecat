# js_astro
Sample code for astrological calculation written by JavaScript.

This library intent to:

* calculation of major planetary position(geocentric, apparent longitude) for 0-4000 A.D. within 1 arcminute.
* calculation of house cusp longitudes

## Requirement
### Environment
Newest Browser, but all comments are written in Japanese(Shift-JIS).

### Library
Some functions requires [spirntf.js](https://github.com/alexei/sprintf.js), but if you don't want to use function `cnv2*`, not required.

## License
Files in this repository are released under MIT license.

## Usage
### Calculate for planetary position
Include all libraries, and call `calPlanetPositon2` as:

```
var planetPosition = new Array();
planetPosition = calPlanetPosition2( year, month, day, hour, minute, longitude, latitude );
```

`calPlanetPosition2` returns array of 20 values:

* Julian day
* Planetary Position(Geocentric apparent ecliptic longitude): Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto
* Lunar Node & apogee Longitude(from approximate osculate orbital elements)
* Longitude of Ascendant, MC(Mid heaven)
	* All value is expressed in degree, without Julian day.
* Position of minor planets(Geocentric apparent ecliptic longitude): Ceres, Pallas, Juno, Vesta, Chiron

### Calculate for house cusp longitudes

Include all libraries, and call `calHouseCusp2` as:

```
var cuspLongitudes = new Array();
cuspLongitudes = calHouseCusp2( year, month, day, hour, minute, longitude, latitude, 1 );
```

Last Argument `1` means Placidus house system.

`calHouseCusp2` returns array of house cusp longitude(Index of this array starts **1**, **not 0**).

### Important notice
In this library, definition of major planets and minor planets is modern astrological, not currently astronomical.
I assume Pluto as major planet and Ceres as minor planet, which they are dwarf planets in currently astronomy.

**Positions of minor planets can calculate between December 30, 1924 12:00 TT and December 31, 2124 12:00 TT only.**

Timezone used in this library is **Japan Standard Time(UTC+0900)**. You may consider to wrapper function to convert your local timezone.
I never consider any Daylight Saving Time in past and future.

This library assumes **eastern geographical longitude and northern geographical latitude as plus**(eg. Tokyo: 139E42 = +139.70, 35N41 = +35.68).

## Demonstration
To test this library, try [this](http://astsakai.halfmoon.jp/fortune/platest_js.html).

## Errata for Leaflet written in Japanese
This library has a leaflet, and this leaflet has some error. Errata is [here](https://github.com/astsakai/js_astro/wiki/support).

