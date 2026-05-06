      subroutine VSOP87 (tdj,ivers,ibody,prec,lu,r,ierr)
*-----------------------------------------------------------------------
*
*     Reference : Bureau des Longitudes - PBGF9502
*
*     Object :
*
*     Substitution of time in VSOP87 solution written on a file.
*     The file corresponds to a version of VSOP87 theory and to a body.
*
*     Input :
*
*     tdj      julian date (real double precision).
*              time scale : dynamical time TDB.
*
*     ivers    version index (integer).
*              0: VSOP87 (initial solution).
*                 elliptic coordinates
*                 dynamical equinox and ecliptic J2000.
*              1: VSOP87A.
*                 rectangular coordinates
*                 heliocentric positions and velocities
*                 dynamical equinox and ecliptic J2000.
*              2: VSOP87A.
*                 spherical coordinates
*                 heliocentric positions and velocities
*                 dynamical equinox and ecliptic J2000.
*              3: VSOP87C.
*                 rectangular coordinates
*                 heliocentric positions and velocities
*                 dynamical equinox and ecliptic of the date.
*              4: VSOP87D.
*                 spherical coordinates
*                 heliocentric positions and velocities
*                 dynamical equinox and ecliptic of the date.
*              5: VSOP87E.
*                 rectangular coordinates
*                 barycentric positions and velocities
*                 dynamical equinox and ecliptic J2000.
*
*     ibody    body index (integer).
*              0: Sun
*              1: Mercury
*              2: Venus
*              3: Earth
*              4: Mars
*              5: Jupiter
*              6: Saturn
*              7: Uranus
*              8: Neptune
*              9: Earth-Moon barycenter
*
*     prec     relative precision (real double precision).
*
*              if prec is equal to 0 then the precision is the precision
*                 p0 of the complete solution VSOP87.
*                 Mercury    p0 =  0.6 10**-8
*                 Venus      p0 =  2.5 10**-8
*                 Earth      p0 =  2.5 10**-8
*                 Mars       p0 = 10.0 10**-8
*                 Jupiter    p0 = 35.0 10**-8
*                 Saturn     p0 = 70.0 10**-8
*                 Uranus     p0 =  8.0 10**-8
*                 Neptune    p0 = 42.0 10**-8
*
*              if prec is not equal to 0, let us say in between p0 and
*              10**-2, the precision is :
*                 for the positions :
*                 - prec*a0 au for the distances.
*                 - prec rd for the other variables.
*                 for the velocities :
*                 - prec*a0 au/day for the distances.
*                 - prec rd/day for the other variables.
*                   a0 is semi-major axis of the body.
*                 Mercury    a0 =  0.3871 ua
*                 Venus      a0 =  0.7233 ua
*                 Earth      a0 =  1.0000 ua
*                 Mars       a0 =  1.5237 ua
*                 Jupiter    a0 =  5.2026 ua
*                 Saturn     a0 =  9.5547 ua
*                 Uranus     a0 = 19.2181 ua
*                 Neptune    a0 = 30.1096 ua
*
*     lu       logical unit index of the file (integer).
*              The file corresponds to a version of VSOP87 theory and
*              a body, and it must be defined and opened before the
*              first call to subroutine VSOP87.
*
*     Output :
*
*     r(6)     array of the results (real double precision).
*
*              for elliptic coordinates :
*                  1: semi-major axis (au)
*                  2: mean longitude (rd)
*                  3: k = e*cos(pi) (rd)
*                  4: h = e*sin(pi) (rd)
*                  5: q = sin(i/2)*cos(omega) (rd)
*                  6: p = sin(i/2)*sin(omega) (rd)
*                     e:     eccentricity
*                     pi:    perihelion longitude
*                     i:     inclination
*                     omega: ascending node longitude
*
*              for rectangular coordinates :
*                  1: position x (au)
*                  2: position y (au)
*                  3: position z (au)
*                  4: velocity x (au/day)
*                  5: velocity y (au/day)
*                  6: velocity z (au/day)
*
*              for spherical coordinates :
*                  1: longitude (rd)
*                  2: latitude (rd)
*                  3: radius (au)
*                  4: longitude velocity (rd/day)
*                  5: latitude velocity (rd/day)
*                  6: radius velocity (au/day)
*
*     ierr     error index (integer).
*                  0: no error.
*                  1: file error (check up ivers index).
*                  2: file error (check up ibody index).
*                  3: precision error (check up prec parameter).
*                  4: reading file error.
*
*-----------------------------------------------------------------------
*
*     --------------------------------
*     Declarations and initializations
*     --------------------------------
*
      implicit double precision (a-h,o-z)
      character*7 bo,body(0:9)
      dimension r(6),t(-1:5),a0(0:9)
      data body/'SUN','MERCURY','VENUS','EARTH','MARS','JUPITER',
     .          'SATURN','URANUS','NEPTUNE','EMB'/
      data a0/0.01d0,0.3871d0,0.7233d0,1.d0,1.5237d0,5.2026d0,
     .        9.5547d0,19.2181d0,30.1096d0,1.d0/
      data dpi/6.283185307179586d0/
      data t/0.d0,1.d0,5*0.d0/
      data t2000/2451545.d0/
      data a1000/365250.d0/
      k=0
      ideb=0
*
      rewind (lu,err=500)
      do i=1,6
         r(i)=0.d0
      enddo
*
      t(1)=(tdj-t2000)/a1000
      do i=2,5
         t(i)=t(1)*t(i-1)
      enddo
*
      ierr=3
      if (prec.lt.0.d0.or.prec.gt.1.d-2) return
      q=dmax1(3.d0,-dlog10(prec+1.d-50))
*
*     -------------------------------------
*     File reading and substitution of time
*     -------------------------------------
*
100   continue
      read (lu,1001,end=400,err=500) iv,bo,ic,it,in
*
      if (ideb.eq.0) then
         ideb=1
         ierr=1
         if (iv.ne.ivers) return
         ierr=2
         if (bo.ne.body(ibody)) return
         ierr=0
         if (iv.eq.0) k=2
         if (iv.eq.2.or.iv.eq.4) k=1
      endif
*
      if (in.eq.0) goto 100
*
      p=prec/10.d0/(q-2)/(dabs(t(it))+it*dabs(t(it-1))*1.d-4+1.d-50)
      if (k.eq.0.or.(k.ne.0.and.ic.eq.5-2*k)) p=p*a0(ibody)
*
      do 200 n=1,in
         nn=n
         read (lu,1002,err=500) a,b,c
         if (dabs(a).lt.p) goto 300
         u=b+c*t(1)
         cu=dcos(u)
         r(ic)=r(ic)+a*cu*t(it)
         if (iv.eq.0) goto 200
         su=dsin(u)
         r(ic+3)=r(ic+3)+t(it-1)*it*a*cu-t(it)*a*c*su
200   continue
*
      goto 100
300   continue
*
      if (nn.eq.in) goto 100
*
      do n=nn+1,in
         read (lu,1002,err=500)
      enddo
      goto 100
*
400   continue
      if (iv.ne.0) then
         do i=4,6
            r(i)=r(i)/a1000
         enddo
      endif
*
      if (k.eq.0) return
*
      r(k)=dmod(r(k),dpi)
      if (r(k).lt.0.d0) r(k)=r(k)+dpi
      return
*
500   continue
      ierr=4
      return
*
*     -------
*     Formats
*     -------
*
1001  format (17x,i1,4x,a7,12x,i1,17x,i1,i7)
1002  format (79x,f18.11,f14.11,f20.11)
*
      end
