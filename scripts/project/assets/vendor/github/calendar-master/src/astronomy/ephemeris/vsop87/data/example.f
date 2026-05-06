*     -----------------
*     PROGRAMME EXAMPLE
*     -----------------
*
*     Reference : Bureau des Longitudes - PBGF9502.
*
*     ------
*     Object
*     ------
*
*     This program is an example of use of VSOP87 subroutine.
*     It computes the coordinates of a planet for a version of VSOP87.
*     VSOP87 (main version) : elliptic coordinates J2000
*     VSOP87A : heliocentric rectangular coordinates J2000
*     VSOP87B : heliocentric spherical   coordinates J2000
*     VSOP87C : heliocentric rectangular coordinates of date
*     VSOP87D : heliocentric spherical   coordinates of date
*     VSOP87E : barycentric  rectangular coordinates J2000
*     The frame is referred to the dynamical equinox and ecliptic.
*     The time scale is the dynamical barycentric time TDB.
*
*     ------------
*     Declarations
*     ------------
*
      implicit double precision (a-h,o-z)
      logical fexist
      integer day,month,year,d0,h0,dt,datmod
      character rep,a(0:5)
      character*4 ext(0:9)
      character*6 prefix
      character*7 vers
      character*21 body(0:9)
      character*40 fich
      character*37 coord(4)
      character*39 reper(2)
      dimension r(6),kbody(0:8,0:5),maxbody(0:5),prec0(0:9)
      data a/' ','A','B','C','D','E'/
      data ext/'.sun','.mer','.ven','.ear','.mar','.jup',
     .         '.sat','.ura','.nep','.emb'/
      data body/'SUN','MERCURY','VENUS','EARTH','MARS','JUPITER',
     .          'SATURN','URANUS','NEPTUNE','EARTH-MOON BARYCENTER'/
      data coord/'Heliocentric elliptic coordinates.',
     .           'Heliocentric rectangular coordinates.',
     .           'Heliocentric spherical coordinates.',
     .           'Barycentric rectangular coordinates.'/
      data reper/'Dynamical equinox and ecliptic J2000.',
     .           'Dynamical equinox and ecliptic of date.'/
      data prec0/1.d-8,0.6d-8,2.5d-8,2.5d-8,10.d-8,35.d-8,70.d-8,
     .           8.d-8,42.d-8,2.5d-8/
      data kbody/1,2,4,5,6,7,8,9,10,
     .           1,2,3,4,5,6,7,8,9,
     .           1,2,3,4,5,6,7,8,10,
     .           1,2,3,4,5,6,7,8,10,
     .           1,2,3,4,5,6,7,8,10,
     .           0,1,2,3,4,5,6,7,8/
      data maxbody/7,8,7,7,7,8/
      data prefix/'VSOP87'/
      menu=4
      lu0=0
*
*     ----------------
*     Version and body
*     ----------------
*
100   continue
      if (menu.ne.1.and.menu.ne.4) goto 200
      call CLRSCR
      print 1000
      print 2001
      read (*,3001,iostat=nerr) ivers
      if (nerr.ne.0) goto 100
      if (ivers.lt.0.or.ivers.gt.5) goto 100
      vers='VSOP87'//a(ivers)
      call CLRSCR
      print 1000
      print 2002, vers
      do i=0,maxbody(ivers)
         nbody=kbody(i,ivers)
         print 2003, nbody,body(nbody)
      enddo
      print 2004
      read (*,3004,iostat=nerr) ibody
      if (nerr.ne.0) goto 100
      irep=0
      do i=0,maxbody(ivers)
         if (kbody(i,ivers).eq.ibody) irep=1
      enddo
      if (irep.eq.0) goto 100
      print 1001
      read 3000, rep
      if (rep.eq.'N'.or.rep.eq.'n') goto 100
*
*     ----------------
*     Open file VSOP87
*     ----------------
*
      lu=ivers*10+10+ibody
      if (lu0.ne.0.and.lu0.ne.lu) close (lu0)
      if (ivers.eq.0) fich=prefix//ext(ibody)
      if (ivers.ne.0) fich=prefix//a(ivers)//ext(ibody)
      inquire (file=fich,exist=fexist)
      if (fexist) then
         if (lu.ne.lu0) then
            open (lu,file=fich,status='old',iostat=nerr)
            if (nerr.ne.0) goto 610
            lu0=lu
         endif
      else
         goto 620
      endif
*
*     -------------
*     Datation mode
*     -------------
*
200   continue
      if (menu.ne.2.and.menu.ne.4) goto 300
      call CLRSCR
      print 1000
      print 2005
      read (*,3005,iostat=nerr) datmod
      if (nerr.ne.0) goto 200
      if (datmod.lt.1.or.datmod.gt.2) goto 200
      if (datmod.eq.1) then
         print 2006
         read (*,3006,iostat=nerr) t0
         if (nerr.ne.0) goto 200
         if (t0.lt.1.d0) goto 200
      else
         print 2007
         read (*,3007,iostat=nerr) d0
         if (nerr.ne.0) goto 200
         call DATEJD (d0,0,td)
         if (td.eq.0.d0) goto 200
         print 2008
         read (*,3008,iostat=nerr) h0
         if (nerr.ne.0) goto 200
         call DATEJD (d0,h0,t0)
         if (t0.eq.0.d0) goto 200
      endif
      t=t0
      print 2009
      read (*,3009,iostat=nerr) dt
      if (nerr.ne.0.or.dt.lt.0) goto 200
      nj=dt/1000000
      nh=mod(dt,1000000)/10000
      nm=mod(dt,10000)/100
      ns=mod(dt,100)
      if (nj.gt.100.or.nh.gt.24.or.nm.gt.60.or.ns.gt.60) goto 200
      pas=nj+nh/24.d0+nm/1440.d0+ns/86400.d0
      print 1001
      read 3000, rep
      if (rep.eq.'N'.or.rep.eq.'n') goto 200
*
*     --------------------------
*     Precision level (relative)
*     --------------------------
*
300   continue
      if (menu.ne.3.and.menu.ne.4) goto 400
      call CLRSCR
      print 1000
      print 2010
      read (*,3010,iostat=nerr) iprec
      if (nerr.ne.0) goto 300
      if (iprec.lt.1.or.iprec.gt.2) goto 300
      if (iprec.eq.1) then
         prec=0.d0
      else
         print 2011, prec0(ibody)
         read (*,3011,iostat=nerr) prec
         if (nerr.ne.0) goto 300
         if (prec.lt.prec0(ibody).or.prec.gt.1.d-2) goto 300
         print 1001
         read 3000, rep
         if (rep.eq.'N'.or.rep.eq.'n') goto 300
      endif
*
*     ----------------------------
*     Computation of the ephemeris
*     ----------------------------
*
400   continue
      print 2012
*
      call VSOP87 (t,ivers,ibody,prec,lu,r,ierr)
*
      if (ierr.ne.0) goto 600
      call JDDATE (t,idate,iheur)
      jdate=abs(idate)
      day=mod(jdate,100)
      month=mod(jdate/100,100)
      year=idate/10000
      nh=iheur/10000
      nm=mod(iheur/100,100)
      ns=mod(iheur,100)
      ic=1
      ir=1
      if (ivers.eq.1.or.ivers.eq.3) ic=2
      if (ivers.eq.2.or.ivers.eq.4) ic=3
      if (ivers.eq.5) ic=4
      if (ivers.eq.3.or.ivers.eq.4) ir=2
*
410   continue
      call CLRSCR
      if (prec.lt.prec0(ibody)) then
         print 4001, vers,body(ibody),coord(ic),reper(ir),
     .               day,month,year,t,nh,nm,ns
      else
         print 4002, vers,body(ibody),coord(ic),reper(ir),
     .               day,month,year,t,nh,nm,ns,prec
      endif
      if (ivers.eq.0) print 4003,r
      if (ivers.eq.1.or.ivers.eq.3.or.ivers.eq.5)
     .   print 4004, r(1),r(4),r(2),r(5),r(3),r(6)
      if (ivers.eq.2.or.ivers.eq.4)
     .   print 4005, r(1),r(4),r(2),r(5),r(3),r(6)
      print 2013
      read 3000, rep
      if (rep.ne.'+'.and.rep.ne.'-') goto 500
      if (dt.eq.0) goto 410
      if (rep.eq.'+') t=t+pas
      if (rep.eq.'-') t=t-pas
      goto 400
*
*     -------------------
*     Another computation
*     -------------------
*
500   continue
      call CLRSCR
      print 1000
      print 2014
      read (*,3014,iostat=nerr) menu
      if (nerr.ne.0) goto 500
      if (menu.lt.0.or.menu.gt.4) goto 500
      if (menu.ne.0) goto 100
      call CLRSCR
      print 1000
      print 2015
      pause ' Program terminated : Hit Enter'
      stop
*
*     ---------------
*     Errors Messages
*     ---------------
*
600   continue
      call CLRSCR
      print 1000
      if (ierr.eq.1) print 5001, ivers
      if (ierr.eq.2) print 5002, ibody
      if (ierr.eq.3) print 5003, prec
      if (ierr.eq.4) print 5004, fich
      pause ' Program terminated : Hit Enter'
      stop
610   continue
      call CLRSCR
      print 1000
      print 5005, fich
      pause ' Program terminated : Hit Enter'
      stop
620   continue
      call CLRSCR
      print 1000
      print 5006, fich
      pause ' Program terminated : Hit Enter'
      stop
*
*     -------
*     Formats
*     -------
*
1000  format (2x,'PLANETARY SOLUTION VSOP87'/
     .        2x,'-------------------------')
1001  format (/2x,'Confirm your choice (y/n) ? ',$)
*
2001  format (/2x,'Choice of the version'/
     .        /2x,'0 : VSOP87 (main solution), elliptic coordinates'
     .        /2x,'    dynamical equinox and ecliptic J2000'/
     .        /2x,'1 : VSOP87A, heliocentric rectangular coordinates'
     .        /2x,'    dynamical equinox and ecliptic J2000'/
     .        /2x,'2 : VSOP87B, heliocentric spherical coordinates'
     .        /2x,'    dynamical equinox and ecliptic J2000'/
     .        /2x,'3 : VSOP87C, heliocentric rectangular coordinates'
     .        /2x,'    dynamical equinox and ecliptic of the date'/
     .        /2x,'4 : VSOP87D, heliocentric spherical coordinates'
     .        /2x,'    dynamical equinox and ecliptic of the date'/
     .        /2x,'5 : VSOP87E, barycentric rectangular coordinates'
     .        /2x,'    dynamical equinox and ecliptic J2000'/
     .        /2x,'Enter your choice ? ',$)
2002  format (/2x,'Choice of the body in version ',a7/)
2003  format (2x,i1,' : ',a21)
2004  format (/2x,'Enter your choice ? ',$)
2005  format (/2x,'Datation mode'/
     .        /2x,'1 : computation with julian dates'
     .        /2x,'2 : computation with calendar dates'/
     .        /2x,'Enter your choice ? ',$)
2006  format (/2x,'Enter the initial julian date'
     .        /2x,'don''t forget the decimal point ---> ',$)
2007  format (/2x,'Enter the initial date'
     .        /2x,'format : +/-yyyymmdd -------------> ',$)
2008  format (/2x,'Enter the initial time'
     .        /2x,'format : hhmmss ------------------> ',$)
2009  format (/2x,'Enter the time step (<100 days)'
     .        /2x,'format : ddhhmmss ----------------> ',$)
2010  format (/2x,'Precision level'/
     .        /2x,'1 : computation with the complete solution'
     .        /2x,'2 : computation with a truncated solution'/
     .        /2x,'Enter your choice ? ',$)
2011  format (/2x,'Enter the relative precision level'
     .        /2x,'between ',f11.9,' and 0.01'
     .        /2x,'don''t forget the decimal point -----> ',$)
2012  format (/2x,'Wait Please . . .')
2013  format (/2x,77('-')//2x,'Choice of time :      next time -> +',
     .        '      previous time -> -      stop -> 0'/
     .        /2x,'Enter your choice ? ',$)
2014  format (/2x,'Another computation'/
     .        /2x,'0 : stop'/
     .        /2x,'1 : with new version or body'
     .        /2x,'2 : with new datation mode'
     .        /2x,'3 : with new precision level'/
     .        /2x,'4 : with new parameters'/
     .        /2x,'Enter your choice ? ',$)
2015  format (///)
*
3000  format (a)
3001  format (i2)
3004  format (i2)
3005  format (i2)
3006  format (f14.6)
3007  format (i10)
3008  format (i7)
3009  format (i9)
3010  format (i2)
3011  format (f12.9)
3014  format (i2)
*
4001  format (2x,'PLANETARY SOLUTION ',a7,5x,'BODY : ',a21
     .        /2x,77('-')//2x,a37,1x,a39/
     .        /2x,'Date : ',i2.2,' / ',i2.2,' / ',i5,
     .        t41,'Julian date : ',f14.6
     .        /2x,'Time : ',i2.2,'h ',i2.2,'m ',i2.2,'s TDB',
     .        t41,'Precision of the complete solution')
4002  format (2x,'PLANETARY SOLUTION ',a7,5x,'BODY : ',a21
     .        /2x,77('-')//2x,a37,1x,a39/
     .        /2x,'Date : ',i2.2,' / ',i2.2,' / ',i5,
     .        t41,'Julian date : ',f14.6
     .        /2x,'Time : ',i2.2,'h ',i2.2,'m ',i2.2,'s TDB',
     .        t41,'Relative precision : ',f10.9)
4003  format (/2x,'Semi-major axis :  ',f13.10,' au',
     .        t41,'Mean longitude :   ',f13.10,' rad'
     .        /2x,'k = e*cos(p) :     ',f13.10,' rad',
     .        t41,'h = e*sin(p) :     ',f13.10,' rad'
     .        /2x,'q = sin(g)*cos(G) :',f13.10,' rad',
     .        t41,'p = sin(g)*sin(G) :',f13.10,' rad'/
     .        /2x,'e : eccentricity',
     .        t41,'p : perihelion longitude'
     .        /2x,'g : semi-iclination',
     .        t41,'G : ascending node longitude')
4004  format (/2x,'X :',f14.10,' au',t41,'X'' :',f14.10,' ua/d'
     .        /2x,'Y :',f14.10,' au',t41,'Y'' :',f14.10,' ua/d'
     .        /2x,'Z :',f14.10,' au',t41,'Z'' :',f14.10,' ua/d')
4005  format (/2x,'Longitude :',f14.10,' rad',
     .        t41,'vitesse  :',f14.10,' rad/d'
     .        /2x,'Latitude : ',f14.10,' rad',
     .        t41,'vitesse  :',f14.10,' rad/d'
     .        /2x,'Radius :   ',f14.10,' au',
     .        t41,'vitesse  :',f14.10,' au/d')
*
5001  format (/2x,'*****  Error *****'/
     .        /2x,'Wrong version index : ',i1/)
5002  format (/2x,'*****  Error *****'/
     .        /2x,'Wrong body index : ',i1/)
5003  format (/2x,'*****  Error *****'/
     .        /2x,'Wrong precision level : ',d9.2/)
5004  format (/2x,'*****  Error *****'/
     .        /2x,'Fatal reading file error : ',a40/)
5005  format (/2x,'*****  Error *****'/
     .        /2x,'Fatal open file error : ',a40/)
5006  format (/2x,'***** File Error *****'/
     .        /2x,'Missing file : ',a40/)
*
      end
*
*
*
      subroutine JDDATE (tjd,idate,ihour)
*-----------------------------------------------------------------------
*
*     Object :
*     Conversion   Julian date ---> Calendar date    (Meeus formular).
*
*     Input :
*     tjd         julian date (real double precision).
*
*     Ouput :
*     idate       calendar date (integer).
*                 julian calendar before 1582 october 15
*                 gregorian calendar after.
*                 code: *yyyymmdd (* sign).
*     ihour       hour (integer).
*                 code: hhmmss.
*
*-----------------------------------------------------------------------
      implicit double precision (a-h,o-z)
      integer day,month,year
      idate=0
      ihour=0
      if (tjd.lt.0.d0) return
      t=tjd+0.5d0/86400.d0+0.5d0
      z=dint(t)
      f=t-z
      if (z.lt.2299161.d0) then
         a=z
      else
         x=dint((z-1867216.25d0)/36524.25d0)
         a=z+1.d0+x-dint(x/4.d0)
      endif
      b=a+1524.d0
      c=dint((b-122.1d0)/365.25d0)
      d=dint(365.25d0*c)
      e=dint((b-d)/30.6001d0)
      day=b-d-dint(30.6001d0*e)
      month=e-1.d0
      if (e.lt.13.5d0) then
         month=e-1.d0
      else
         month=e-13.d0
      endif
      if (month.lt.3) then
         year=c-4715.d0
      else
         year=c-4716.d0
      endif
      is=+1
      if (year.lt.0) is=-1
      idate=((iabs(year)*100+month)*100+day)*is
      f=f*24.d0
      ih=f
      f=(f-ih)*60.d0
      im=f
      f=(f-im)*60.d0
      is=f
      ihour=(ih*100+im)*100+is
      return
      end
*
*
*
      subroutine DATEJD (idate,ihour,tjd)
*-----------------------------------------------------------------------
*
*     Object :
*     Conversion   Calendar date -> Julian date    (Meeus formular).
*
*     Input :
*     idate       calendar date gregorian/julian (integer).
*                 julian calendar before 1582 october 15
*                 gregorian calendar after.
*                 code: *yyyymmdd (* sign).
*     ihour       hour (integer).
*                 code: hhmmss.
*
*     Output
*     tjd         julian date (real double precision).
*
*-----------------------------------------------------------------------
      implicit double precision (a-h,o-z)
      integer day,month,year
      dimension lm(12)
      data lm/31,28,31,30,31,30,31,31,30,31,30,31/
      tjd=0.d0
      year=idate/10000
      if (year.lt.-4713.or.year.gt.5000) return
      kdate=iabs(idate)-iabs(year)*10000
      month=kdate/100
      if (month.lt.1.or.month.gt.12) return
      day=kdate-month*100
      lm(2)=28
      if (mod(year,4).eq.0) then
         lm(2)=29
         if (year.gt.1582) then
            ncent=year/100
            if (mod(year,100).eq.0.and.mod(ncent,4).ne.0) lm(2)=28
         endif
      endif
      if (day.lt.1.or.day.gt.lm(month)) return
      is=ihour
      ih=ihour/10000
      if (ih.lt.0.or.ih.gt.24) return
      is=is-ih*10000
      im=is/100
      if (im.lt.0.or.im.gt.60) return
      is=is-im*100
      if (is.lt.0.or.is.gt.60) return
      a=0.d0
      b=0.d0
      c=0.d0
      if (month.gt.2) then
         y=year
         m=month
      else
         y=year-1
         m=month+12
      endif
      if (y.lt.0.d0) then
         c=-0.75d0
      else
         if (idate.ge.15821015) then
            a=dint(y/100.d0)
            b=2.d0-a+dint(a/4.d0)
         endif
      endif
      tjd=dint(365.25d0*y+c)+dint(30.6001d0*(m+1))+day+
     .    dfloat(ih)/24.d0+dfloat(im)/1440.d0+dfloat(is)/86400.d0+
     .    1720994.5d0+b
      return
      end
*
*
*
      subroutine CLRSCR
*-----------------------------------------------------------------------
*
*     ref : bdl-gf9412
*
*     Object :
*     Clear the screen.
*
*     Remark :
*     *DOS  for DOS system.
*     *UNX  for UNIX system.
*
*-----------------------------------------------------------------------
*
*DOS  character*7 escscr
*DOS  escscr=char(27)//char(91)//'2J'//char(27)//char(91)//'H'
*DOS  write (*,'(2x,a)') escscr
*
*UNX  call system ('clear')
*
      call system ('clear')
*
      return
      end
*
*
*
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
