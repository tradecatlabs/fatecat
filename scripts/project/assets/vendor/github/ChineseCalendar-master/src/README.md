# Source files for building the package

## Files:

Almost all of the following HTML files have English, traditional Chinese and simplified Chinese versions. They have the same names but with \_chinese and \_simp as suffixes. Many html files in this directory work as it is, but a dozen of them need to be processed by the build script before they can be run properly.

- index.html: main HTML page showing the conversion between the Western calendar and Chinese calendar for any year between 722 BCE and 2200 CE. (need to be processed)
- table.html: HTML page showing a conversion table between the two calendars. (need to be processed)
- solarTerms.html: HTML page explaining the 24 solar terms.
- sexagenary.html: HTML page explaining the sexagenary cycle.
- rules.html: HTML page explaining the rules for the Chinese calendar.
- examples.html: HTML page demonstrating the computation of Chinese calendar. There is also a discussion about the exceptional year 2033. 
- rules_demysterified.html: HTML page explaining how the rules of the Chinese calendar manage to keep both the lunar cycle and cycle of seasons in sync with the calendar. There is also a discussion on the 19-year cycle and the average length of a year and a month in the Chinese calendar.
- computation.html: documentation of the calendar calculation used here.
- sunMoon.html: Times of Moon phases and 24 solar terms from -3500 to 3500. (need to be processed)
- Julian.html: Web-based Julian and Sexagenary Date Calculator (need to be processed)
- era_names.html/era_names_simp.html: Era/reign names used in the Chinese history (in Chinese). 
- era.js: javascript file for displaying the era/reign names in index_chinese.html
- chunqiu.html: documentation -- Reconstruction of the Chunqiu Calendar
- guliuli.html: documentation -- Computation of the Ancient Six Calendars
- QinHanCalendars.html: documentation -- Reconstruction of Calendars in the Qin and Early Han Dynasties
- QinHanSolarTerms.html: Dates of Selected Solar Terms in Qin and Early Han Dynasties
- MingCalendar.html: research article -- Lunar Conjunction Calculation in the Ming Dynasty and Corrections to the Ming Calendar Data
- discrepanciesQing.html: Discrepancies Between Modern Calculation and Historical Data (1645 - 1911) 
- 3500Calendars_errors.html/3500Calendars_errors_simp.html: Errors in the book 3500 Years of Calendars and Astronomical Phenomena (in Chinese)
- Shangyuan.html: An article on the Shangyuan system in ancient Chinese Astronomical Systems
- calendar.css: CSS file for the HTML pages mentioned above. 
- calendar_chinese.css: CSS file for the Chinese versions of the HTML pages mentioned above.
- header.js: JavaScript file for creating the header in all HTML pages, including the Chinese version of the HTML pages.
- calendarData.js: contains data used for conversion between the Western calendar and Chinese calendar, dates and times of the moon phases and 24 solar terms between -721 and 2200. I computed these data and put them into JSON format. This file is used by index.html, table.html and the Chinese version of these two files.
- calendar.js: JavaScript file for handling the activities on index.html, index_chinese and index_simp.html.
- table.js: JavaScript file for handling the activities on table.html, table_chinese.html and table_simp.html.
- split.js: JavaScript file for handling calendars in 221-280, 384-589 and 947-1279.
- ancientCalendars.js: contain functions that handle the calendars before 104 BCE.
- sunMoonData.js: Dates and times of moon phases and solar terms from -3501 to 3502 in JSON.
- sunMoon.js: JavaScript file for handling the activities on sunMoon.html, sunMoon_chinese.html and sunMoon_simp.html
- Julian.js: JavaScript file for handling the activities Julian.html, Julian_chinese.html and Julian_simp.html
- calendarEngLegend.png/calendarChiLegend.png/calendarSimLegend.png: image file used by index.html/index_chinese.html/index_simp.html.
- 24solarTermsEng.png/24solarTermsChi.png/24solarTermsSim.png: image file used by solarTerms.html/solarTerms_chinese.html/solarTerms_simp.html.
- NianAvg1.png, NianAvg2.png, YueAvg.png: image files used by rules_demysterified.html, rules_demysterified_chinese.html and rules_demysterified_simp.html.
- Dipper.jpg, Dipper_chinese.jpg, Dipper_simp.jpg, direction_branch.png, direction_branch_chinese.png, direction_branch_simp.png: image files used by sexagenary.html, sexagenary_chinese.html and sexagenary_simp.html
- QinHanConjTimeLag.jpg, QinHanConjTimeLag_chinese.jpg, QinHanConjTimeLag_simp.jpg: image files used by QinHanCalendars.html, QinHanCalendars_chinese.html and QinHanCalendars_simp.html
- TDBtimes.txt: TDB times of moon phases and 24 solar terms between 1600 and 3500 calculated from JPL ephemeris DE431 and using the IAU 2006/2000A precession-nutation model. 
- TDBtimes_extended.txt.gz: (gzipped) TDB times of moon phases and 24 solar terms between -4000 and 8000 calculated from JPL ephemeris DE431 and using the Vondrak et al 2011 precession model and IAU2000A nutation model.
- docs/sunMoon.pdf: PDF file explaining how I compute the times of the moon phases and 24 solar terms used for the calendar calculation. 
- docs/sunMoon_chinese.pdf: traditional Chinese version of docs/sunMoon.pdf
- docs/sunMoon_simp.pdf: simplified Chinese version of docs/sunMoon.pdf
