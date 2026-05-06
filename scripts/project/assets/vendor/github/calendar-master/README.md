# Chinese Lunar Calendar

It is a javascript program for Chinese lunnar calendar based on astronomical calculation. (Not completed yet)

A lunar month is the time between two successive syzygies. In Chinese lunar calendar, the time of new moon is used. Hence, the most important thing is to calculate the time of a straight-line configuration of Sun, Earth and Moon.

For more details, please see the [wiki](https://github.com/lhttjdr/calendar/wiki/Introduction).

## Principle

This project only use type(defined by contract function), function, and module(as namespace). Here I avoid any OOP or well-known design patterns.

## Todo

### Math

#### Basic Number System

- [X] `math.decimal`: union of `number` and `string`; e.g. sum numbers or numbers  represented as strings (2 implements:built-in `number`, high precision number using `decimal.js` library)
- [X] `math.vector`: general vector calculation
- [X] `math.quaternion`: rotation of coordinates
- [X] `math.dualnumber`: a kind of extended number, like complex number
- [X] `math.dualquaternion`: translation and rotation of coordinates

#### Tools

- [X] `math.angle`: compute radian, degree, hour ...represented as strings
- [X] `math.polynomial`: basic calculation about polynomial
- [X] `math.expression`: a tool for complicated formula with `decimal` (because JavaScript does not allow to overload operators)

#### 3d Coordinates

- [X] `math.coordinate.point`: 3d point data type under cartesian coordinates system or spherical coordinates system
- [X] `math.coordinate.descartes`: cartesian coordinates operations
- [X] `math.coordinate.sphere`: spherical coordinates operations

### Astronomy

#### Coordinates

- [X] `coordinate.point`: data types of 4 kinds celestial coordinate system
- [X] `coordinate.first-equatorial`: first equatorial coordinate system, HA-dec. system.
- [X] `coordinate.second-equatorial`: equatorial coordinate system
- [X] `coordinate.ecliptic`: ecliptic coordinate system
- [X] `coordinate.horizontal`: horizontal coordinate system

#### Sun Position

- [X] `ephemeries.vsop87`: translation from offical fortran code of VSOP87
  - Official Fortran Code: [ftp://ftp.imcce.fr/pub/ephem/planets/vsop87/](ftp://ftp.imcce.fr/pub/ephem/planets/vsop87/)
- [ ] `ephemeries.vsop2000`: translation from offical fortran code of VSOP2000
  - Official Fortran Code: [<del>ftp://syrte.obspm.fr/pub/polac/transit/vsop2000/</del>](ftp://syrte.obspm.fr/pub/polac/transit/vsop2000/) **not available**
- [ ] `ephemeries.vsop2010`: translation from offical fortran code of VSOP2010
  - Official Fortran Code: [ftp://ftp.imcce.fr/pub/ephem/planets/vsop2010/](ftp://ftp.imcce.fr/pub/ephem/planets/vsop2010/)
- [ ] `ephemeries.vsop2013`: translation from offical fortran code of VSOP2013
  - Official Fortran Code: [ftp://ftp.imcce.fr/pub/ephem/planets/vsop2013/](ftp://ftp.imcce.fr/pub/ephem/planets/vsop2013/)
- [ ] `ephemeries.vsop87.xjw`: a simplified version of VSOP87 by Jianwei Xu included in his *ShouXing Astronomical Calendar*

#### Moon Position

- [ ] `ephemeries.elp82b`: translation from offical fortran code of ELP-82B
  - Official Fortran Code: [ftp://cyrano-se.obspm.fr/pub/2_lunar_solutions/1_elp82b/](ftp://cyrano-se.obspm.fr/pub/2_lunar_solutions/1_elp82b/)

- [X] `ephemeries.elpmpp02`: translation from offical fortran code of ELP-MPP02
  - Official Fortran Code: [ftp://cyrano-se.obspm.fr/pub/2_lunar_solutions/2_elpmpp02/](ftp://cyrano-se.obspm.fr/pub/2_lunar_solutions/2_elpmpp02/)
- [ ] `ephemeries.elpmpp02.xjw`: a simplified version of ELP-MPP02 by Jianwei Xu included in his *ShouXing Astronomical Calendar*

#### Axial Precession (岁差)

- [X] `axial-precession.b03`: Bretagnon, P., Fienga, A., & Simon, J.-L. 2003, A&A, 400, 785
- [X] `axial-precession.iau2000`: IAU 1976 ecliptic precession (Lieske et al. 1977, A&A, 58, 1) and the precession part of the IAU 2000A equator adopted by IAU 2000 Resolution B1.6 (Mathews et al. 2002, J. Geophys. Res., 107, B4, 10.1029/2001JB000390)
- [X] `axial-precession.l77`:Lieske, J. H., Lederle, T., Fricke, W., & Morando, B. 1977, A&A, 58, 1
- [X] `axial-precession.p03`:Capitaine, N., Wallace, P. T., & Chapront, J. 2003b, A&A, 412, 567

#### Nutation (章动)

- [ ] `nutation.wahr`: John M. Wahr. The forced nutations of an elliptical, rotating, elastic and oceanless earth. Volume64, Issue3. March 1981. Pages 705-727
  - need more details
- [ ] `nutation.mhb2000`: Herring, T. A.; Mathews, P. M.; Buffett, B. A. Modeling of nutation-precession: Very long baseline interferometry results. Journal of Geophysical Research (Solid Earth), Volume 107, Issue B4, CiteID 2069, DOI 10.1029/2001JB000165
  - Offical Fortran Code: [http://www-gpsg.mit.edu/~tah/mhb2000/](http://www-gpsg.mit.edu/~tah/mhb2000/)
- [X] <del>`nutation.mhb2000.truncated`:</del> **need confirm**
- [ ] `nutation.iau2000A`: Nutation, IAU 2000A model (MHB_2000 without FCN). Annexe to IERS Conventions 2000, Chapter 5
  - Offical Fortran Code: [ftp://maia.usno.navy.mil/conventions/archive/2003/chapter5/NU2000A.f](ftp://maia.usno.navy.mil/conventions/archive/2003/chapter5/NU2000A.f)
- [ ] `nutation.iau2000B`: Nutation, IAU 2000B (truncated) model. Annexe to IERS Conventions 2000, Chapter 5
  - Offical Fortran Code: [ftp://maia.usno.navy.mil/conventions/archive/2003/chapter5/NU2000B.f](ftp://maia.usno.navy.mil/conventions/archive/2003/chapter5/NU2000B.f)

#### Atmospheric Refraction (大气折射)

- [X] `atmospheric-refraction.Smart`: Smart, W. M. 1965, Spherical Astronomy (Cambridge, Cambridge University), p.58
- [X] `atmospheric-refraction.Saemundsson`: Sæmundsson
- [X] `atmospheric-refraction.Meeus`
- [X] `atmospheric-refraction.Bennett`
- [X] `atmospheric-refraction.Bennett.improved`
- [X] `atmospheric-refraction.xjw`: a formula used by Jianwei Xu included in his *ShouXing Astronomical Calendar* 

#### Parallax (视差)

#### ΔT=TT-UT (地球时-世界时)

#### Aberration of Light (光行差)

### Lunar

- [ ] solar term (节气)
- [ ] syzygy (朔望)
- [ ] intercalation (置闰)