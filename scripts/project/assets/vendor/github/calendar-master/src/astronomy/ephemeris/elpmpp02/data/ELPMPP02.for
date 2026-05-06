!-----------------------------------------------------------------------
!     SUBROUTINE ELPMPP02 TEST:
!     COMPUTATION OF GEOCENTRIC RECTANGULAR COORDINATES OF THE MOON
!-----------------------------------------------------------------------
!
      implicit        double precision (a-h,o-z)
      character*5     aa(0:1)
      dimension       r(6)
      parameter       (dj2000=2451545.0d0)
      data            aa/'LLR','DE405'/
!
      open (10,file='ELPMPP02.TXT')
!
!-----------------------------------------------------------------------
!     COMPUTE LUNAR COORDINATES (POSITIONS ANS VELOCITIES):
!     5 DATES FROM JD 2444239.5 TO 2452239.5,
!     TIME INTERVAL = 2000 DAYS,
!     CONSTANTS FITTED TO LLR OBSERVATIONS.
!-----------------------------------------------------------------------
!
      tj0=2444239.5d0
      dtj=2000.d0
      nda=5
      icor=0
!
      do n=1,nda
!
         t=tj0+(n-1)*dtj-dj2000
!
         call ELPMPP02 (t,11,icor,r,ierr)
!
         if (ierr.ne.0) then
             write (*,*) 'ERREUR ',ierr
             stop 
         endif
!
         tdj=t+dj2000
         write (*,1002)  tdj,r
         write (10,1002) tdj,r
!
      enddo
!
!-----------------------------------------------------------------------
!     COMPUTE LUNAR COORDINATES (POSITIONS ANS VELOCITIES):
!     5 DATES FROM JD 2500000.5 TO 1700000.5,
!     TIME INTERVAL = -200000 DAYS,
!     CONSTANTS FITTED TO JPL EPHEMERIS DE405.
!-----------------------------------------------------------------------
!
      tj0=2500000.5d0
      dtj=-200000.d0
      nda=5
      icor=1
!
      do n=1,nda
!
         t=tj0+(n-1)*dtj-dj2000
!
         call ELPMPP02 (t,11,icor,r,ierr)
!
         if (ierr.ne.0) then
             write (*,*) 'ERREUR ',ierr
             stop 
         endif
!
         tdj=t+dj2000
         write (*,1002)  tdj,r
         write (10,1002) tdj,r
!
      enddo
!
      stop
!
! --- Formats ----------------------------------------------------------
!
1001  format (/2x,'ELP/MPP02:'
     &        ,2x,'t0: ',f9.1,2x,'nda: ',i5,2x,'icor: ',a/)
1002  format (2x,'JD ',f9.1/
     &        2x,'X = ',f17.7,
     &        2x,'Y = ',f17.7,
     &        2x,'Z = ',f17.7,2x,'km'/
     &        2x,'X''= ',f17.7,
     &        2x,'Y''= ',f17.7,
     &        2x,'Z''= ',f17.7,2x,'km/day')
      end
!
!
!
      subroutine ELPMPP02 (tj,lu,icor,xyz,ierr)
!-----------------------------------------------------------------------
!
!     Ref: JCGF0206
!
! --- OBJECT -----------------------------------------------------------
!
!     Computation of the Moon coordinates with ELP/MPP02 lunar theory.
!     Frame: dynamical mean ecliptic and equinox of J2000.
!
! --- INPUT ------------------------------------------------------------
!
!     tj       : Time in days from J2000 (real*8).
!
!     lu       : Logical unit of Moon files (integer).
!
!     icor     : Index of the corrections to the constants (integer).
!
! --- OUTPUT -----------------------------------------------------------
!
!     xyz(6)   : Geocentric rectangular coordinates (real*8).
!                xyz(1) : Position X (km)
!                xyz(2) : Position Y (km)
!                xyz(3) : Position Z (km)
!                xyz(4) : Velocity X' (km/day)
!                xyz(5) : Velocity Y' (km/day)
!                xyz(6) : Velocity Z' (km/day)
!
!     ierr     : Error file index (integer).
!                ierr=0 : no error.
!                ierr=1 : error file.
!
! --- HOW TO USE IT ----------------------------------------------------
!
!     The subroutine ELPMPP02 calls 3 subroutines:
!     INITIAL  : Initialization of the constants of the solution,
!     READFILE : Reading the 6 files containing the ELP/MPP02 series,
!     EVALUATE : Computation of the geocentric coordinates of the Moon.
!
!     The subroutines INITIAL and READFILE are used after the first call 
!     to the subroutine ELPMPP02. They are also called each time the 
!     index of the corrections is modified. Hence, it is not advisable 
!     to change the index during a same run.    
!
!     The subroutine ELPMPP02 uses 2 commons:
!     ELPCST : Constants of the solution ELP/MPP02, 
!     ELPSER : Series of the solution ELP/MPP02.
!
!     The constants are initialized by INITIAL and used in READFILE and 
!     EVALUATE. The series are read by READFILE and used in EVALUATE.
!
!     The subroutine ELPMPP02 sets the names of the 6 files that  
!     contain the ELP/MPP02 series (parameter 'filename').
!     These names include the directory where the files are stored.
!     By default, the files are supposed to be stored in the current
!     directory.
!
!     The nominal values of some constants have to be corrected.
!     There are 2 sets of corrections. The corresponding choice is 
!     marked by the parameter 'icor' (used in INITIAL).
!     icor=0, the constants are fitted to LLR observations provided 
!             from 1970 to 2001; it is the default value;
!     icor=1, the constants are fitted to DE405 ephemeris over one 
!             century (1950-1960); the lunar angles W1, W2, W3 receive 
!             also additive corrections to the secular coefficients.
!
! --- Declarations -----------------------------------------------------
!
      implicit double precision (a-h,o-z),integer(i-n)
!
      character*40   filename(6)
      dimension      xyz(6)
!
      data           kinit/999/
      save           kinit
!
! --- Names of the ELPMPP02 files --------------------------------------
!
      filename(1)='ELP_MAIN.S1'
      filename(2)='ELP_MAIN.S2'
      filename(3)='ELP_MAIN.S3'
      filename(4)='ELP_PERT.S1'
      filename(5)='ELP_PERT.S2'
      filename(6)='ELP_PERT.S3'
!
! --- Initializing of constants and Reading the files-------------------
!
      if (icor.ne.kinit) then
         call INITIAL (icor) 
         call READFILE (lu,filename,ierr)
         if (ierr.ne.0) return
         kinit=icor
      endif 
!
! --- Computation of the geocentric coordinates of the Moon ------------
!
      call EVALUATE (tj,xyz)
!
      return
      end
!
!
!
      subroutine INITIAL (icor)
!-----------------------------------------------------------------------
!
!     Ref: JCGF0206
!
! --- OBJECT -----------------------------------------------------------
!
!     Initialization of the constants and parameters used for the 
!     evaluation of the ELP/MPP02 series.
!
! --- INPUT ------------------------------------------------------------
!
!     icor     : Index of the corrections to the constants (integer).
!
! --- OUTPUT -----------------------------------------------------------
!
!     elpcst   : Set of the constants of ELPMPP02 solution (common).
!
! --- REMARKS ----------------------------------------------------------
!
!     The nominal values of some constants have to be corrected.
!     There are 2 sets of corrections. The corresponding choice is 
!     marked by the parameter 'icor' (used in INITIAL).
!     icor=0, the constants are fitted to LLR observations provided 
!             from 1970 to 2001; it is the default value;
!     icor=1, the constants are fitted to DE405 ephemeris over one 
!             century (1950-1960); the lunar angles W1, W2, W3 receive 
!             also additive corrections to the secular coefficients.
! 
! --- NOTATIONS --------------------------------------------------------
!
!     Moon elements (polynomials coefficients until order 4):
!     w(1,0:4)  : mean longitude of the Moon                        (W1)
!     w(2,0:4)  : mean longitude of the lunar perigee               (W2)
!     w(3,0:4)  : mean longitude of the lunar ascending node        (W3)
!     zeta(0:4) : mean longitude of the Moon + precession        (W1+pt)
!                 p is the precession rate and t is the time
!
!     Earth-Moon (EMB) elements (polynomials coefficients until order 4):
!     eart(0:4) : mean longitude of EMB                             (Te)
!     peri(0:4) : mean longitude of the perihelion of EMB          (Pip)
!
!     Delaunay arguments (polynomials coefficients until order 4):
!     del(1,0:4): D  =  W1 - Te + 180 degrees                        (D)
!     del(2,0:4): F  =  W1 - W3                                      (F)
!     del(3,0:4): l  =  W1 - W2   mean anomaly of the Moon           (l)
!     del(4,0:4): l' =  Te - Pip  mean anomaly of EMB               (l')
!
!     Planetary arguments (mean longitudes at J2000 and mean motions):
!     p(1,0:1)  : mean longitude of Mercury
!     p(2,0:1)  : mean longitude of Venus
!     p(3,0:1)  : mean longitude of EMB (eart(0:1))
!     p(4,0:1)  : mean longitude of Mars 
!     p(5,0:1)  : mean longitude of Jupiter
!     p(6,0:1)  : mean longitude of Saturn
!     p(7,0:1)  : mean longitude of Uranus
!     p(8,0:1)  : mean longitude of Neptune
!
!     Moon constants:
!     nu        : mean motion of the Moon (W1(1,1))                 (Nu)
!     g         : half coefficient of sin(F) in latitude         (Gamma)
!     e         : half coefficient of sin(l) in longitude            (E)
!     np        : mean motion of EMB (eart(1))                      (n')
!     ep        : eccentricity of EMB                               (e')
!     alpha     : Ratio of the semi-major axis (Moon / EMB)
!     am        : Ratio of the mean motions (EMB / Moon)
!     dtasm     : (2*alpha) / (3*am)     
!
!     Corrections to the constants Nu, Gamma, E, n', e':
!     delnu     : to the mean motion of the Moon 
!     delg      : to the half coefficient of sin(F) in latitude
!     dele      : to the half coefficient of sin(l) in longitude
!     delnp     : to the mean motion of EMB 
!     delep     : to the eccentricity of EMB
!
!     Precession of the longitude of the ascending node of the mean 
!     ecliptic of date on fixed ecliptic J2000:
!     pi(i=1,5) : sine coefficients
!     qi(i=1,5) : cosine coefficients
!
! --- Declarations -----------------------------------------------------
!
      implicit double precision (a-h,o-z),integer(i-n)
!
      parameter       (cpi=3.141592653589793d0)
      parameter       (rad=648000.d0/cpi,deg=cpi/180.d0)
!
      common/elpcst/  w(3,0:4),eart(0:4),peri(0:4),zeta(0:4),del(4,0:4),
     &                p(8,0:4),delnu,dele,delg,delnp,delep,dtasm,am,
     &                p1,p2,p3,p4,p5,q1,q2,q3,q4,q5
!
      dimension       bp(5,2)
      data bp/        +0.311079095d00, -0.4482398d-2,
     &                -0.110248500d-2, +0.1056062d-2, +0.50928d-4,
     &                -0.103837907d00, +0.6682870d-3,
     &                -0.129807200d-2, -0.1780280d-3, -0.37342d-4/
!
! --- Function for the conversion : sexagesimal degrees -> radians -----
!
      DMS(ideg,imin,sec)=(ideg+imin/60.d0+sec/3600.d0)*deg
!
! --- Value of the correction to the constant of precession ------------
!
      Dprec=-0.29965d0                                  !***** IAU 2000A
!
! --- Constants for the evaluation of the partial derivatives ----------
!
      am     =  0.074801329d0
      alpha  =  0.002571881d0
      dtasm  =  (2.d0*alpha)/(3.d0*am)
      xa     =  (2.d0*alpha)/3.d0
!
! --- Corrections to constants -----------------------------------------
!
      k=icor
      if (k.ne.1) k=0
!
!     Values of the corrections to the constants fitted to LLR.
!     Fit 13-05-02 (2 iterations) except Phi and eps w2_1 et w3_1
!
      if (k.eq.0) then
!
         Dw1_0   = -0.10525d0
         Dw2_0   =  0.16826d0
         Dw3_0   = -0.10760d0
         Deart_0 = -0.04012d0
         Dperi   = -0.04854d0
         Dw1_1   = -0.32311d0
         Dgam    =  0.00069d0
         De      = +0.00005d0
         Deart_1 =  0.01442d0
         Dep     =  0.00226d0
         Dw2_1   =  0.08017d0
         Dw3_1   = -0.04317d0
         Dw1_2   = -0.03794d0
!
      else
!
!     Values of the corrections to the constants fitted to DE405
!     over the time interval (1950-2060)
!
         Dw1_0   = -0.07008d0
         Dw2_0   =  0.20794d0
         Dw3_0   = -0.07215d0
         Deart_0 = -0.00033d0
         Dperi   = -0.00749d0
         Dw1_1   = -0.35106d0
         Dgam    =  0.00085d0
         De      = -0.00006d0
         Deart_1 =  0.00732d0
         Dep     =  0.00224d0
         Dw2_1   =  0.08017d0
         Dw3_1   = -0.04317d0
         Dw1_2   = -0.03743d0
!
      endif
!
! --- Fundamental arguments (Moon and EMB) -----------------------------
!
      w(1,0) = DMS(218,18,59.95571d0+Dw1_0)              !***** ELP
      w(1,1) = (1732559343.73604d0+Dw1_1)/rad            !***** ELP
      w(1,2) = (        -6.8084d0 +Dw1_2)/rad            !***** DE405
      w(1,3) =          0.66040d-2/rad                   !***** ELP
      w(1,4) =         -0.31690d-4/rad                   !***** ELP
!
      w(2,0) = DMS( 83,21,11.67475d0+Dw2_0)              !***** ELP
      w(2,1) = (  14643420.3171d0 +Dw2_1)/rad            !***** DE405
      w(2,2) = (       -38.2631d0)/rad                   !***** DE405
      w(2,3) =         -0.45047d-1/rad                   !***** ELP
      w(2,4) =          0.21301d-3/rad                   !***** ELP
!
      w(3,0) = DMS(125, 2,40.39816d0+Dw3_0)              !***** ELP
      w(3,1) = (  -6967919.5383d0 +Dw3_1)/rad            !***** DE405
      w(3,2) = (         6.3590d0)/rad                   !***** DE405
      w(3,3) =          0.76250d-2/rad                   !***** ELP
      w(3,4) =         -0.35860d-4/rad                   !***** ELP
!
      eart(0)= DMS(100,27,59.13885d0+Deart_0)            !***** VSOP2000
      eart(1)= (129597742.29300d0 +Deart_1)/rad          !***** VSOP2000
      eart(2)=         -0.020200d0/rad                   !***** ELP
      eart(3)=          0.90000d-5/rad                   !***** ELP
      eart(4)=          0.15000d-6/rad                   !***** ELP

      peri(0)= DMS(102,56,14.45766d0+Dperi)              !***** VSOP2000
      peri(1)=       1161.24342d0/rad                    !***** VSOP2000
      peri(2)=          0.529265d0/rad                   !***** VSOP2000
      peri(3)=         -0.11814d-3/rad                   !***** VSOP2000
      peri(4)=          0.11379d-4/rad                   !***** VSOP2000
!
! --- Corrections to the secular terms of Moon angles ------------------
!
      if (icor.eq.1) then
         w(1,3) = w(1,3) -0.00018865d0/rad
         w(1,4) = w(1,4) -0.00001024d0/rad
         w(2,2) = w(2,2) +0.00470602d0/rad
         w(2,3) = w(2,3) -0.00025213d0/rad
         w(3,2) = w(3,2) -0.00261070d0/rad
         w(3,3) = w(3,3) -0.00010712d0/rad
      endif
!
! --- Corrections to the mean motions of the Moon angles W2 and W3 -----
!     infered from the modifications of the constants
!
      x2     =   w(2,1)/w(1,1)
      x3     =   w(3,1)/w(1,1)
      y2     =   am*bp(1,1)+xa*bp(5,1)
      y3     =   am*bp(1,2)+xa*bp(5,2)
!
      d21    =   x2-y2
      d22    =   w(1,1)*bp(2,1)
      d23    =   w(1,1)*bp(3,1)
      d24    =   w(1,1)*bp(4,1)
      d25    =   y2/am
!
      d31    =   x3-y3
      d32    =   w(1,1)*bp(2,2)
      d33    =   w(1,1)*bp(3,2)
      d34    =   w(1,1)*bp(4,2)
      d35    =   y3/am
!
      Cw2_1  =  d21*Dw1_1+d25*Deart_1+d22*Dgam+d23*De+d24*Dep
      Cw3_1  =  d31*Dw1_1+d35*Deart_1+d32*Dgam+d33*De+d34*Dep
!
      w(2,1) =  w(2,1)+Cw2_1/rad
      w(3,1) =  w(3,1)+Cw3_1/rad
!
! --- Arguments of Delaunay --------------------------------------------
!
      do i=0,4
         del(1,i) = w(1,i)-eart(i)                             !***** D 
         del(2,i) = w(1,i)-w(3,i)                              !***** F 
         del(3,i) = w(1,i)-w(2,i)                              !***** l 
         del(4,i) = eart(i)-peri(i)                            !***** l'
      end do
      del(1,0) = del(1,0) + cpi
!
! --- Planetary arguments (mean longitudes and mean motions) -----------
!
      p(1,0) = DMS(252,15, 3.216919d0)                   !***** VSOP2000
      p(2,0) = DMS(181,58,44.758419d0)                   !***** VSOP2000
      p(3,0) = DMS(100,27,59.138850d0)                   !***** VSOP2000
      p(4,0) = DMS(355,26, 3.642778d0)                   !***** VSOP2000
      p(5,0) = DMS( 34,21, 5.379392d0)                   !***** VSOP2000
      p(6,0) = DMS( 50, 4,38.902495d0)                   !***** VSOP2000
      p(7,0) = DMS(314, 3, 4.354234d0)                   !***** VSOP2000
      p(8,0) = DMS(304,20,56.808371d0)                   !***** VSOP2000
!
      p(1,1) = 538101628.66888d0/rad                     !***** VSOP2000
      p(2,1) = 210664136.45777d0/rad                     !***** VSOP2000
      p(3,1) = 129597742.29300d0/rad                     !***** VSOP2000
      p(4,1) =  68905077.65936d0/rad                     !***** VSOP2000
      p(5,1) =  10925660.57335d0/rad                     !***** VSOP2000
      p(6,1) =   4399609.33632d0/rad                     !***** VSOP2000
      p(7,1) =   1542482.57845d0/rad                     !***** VSOP2000
      p(8,1) =    786547.89700d0/rad                     !***** VSOP2000
!
      do i=1,8
      do j=2,4
         p(i,j)=0.d0
      enddo
      enddo
!
! --- Zeta : Mean longitude W1 + Rate of the precession ----------------
!
      zeta(0)= w(1,0)
      zeta(1)= w(1,1) + (5029.0966d0+Dprec)/rad
      zeta(2)= w(1,2)
      zeta(3)= w(1,3)
      zeta(4)= w(1,4)
!
! --- Corrections to the parameters: Nu, E, Gamma, n' et e' ------------
!
      delnu  = (+0.55604d0+Dw1_1)/rad/w(1,1)                  !***** ELP
      dele   = (+0.01789d0+De)/rad                            !***** ELP
      delg   = (-0.08066d0+Dgam)/rad                          !***** ELP
      delnp  = (-0.06424d0+Deart_1)/rad/w(1,1)                !***** ELP
      delep  = (-0.12879d0+Dep)/rad                           !***** ELP
!
! --- Precession coefficients for P and Q (Laskar, 1986) ---------------
!
      p1 =  0.10180391d-04
      p2 =  0.47020439d-06
      p3 = -0.5417367d-09
      p4 = -0.2507948d-11
      p5 =  0.463486d-14
!
      q1 = -0.113469002d-03
      q2 =  0.12372674d-06
      q3 =  0.1265417d-08
      q4 = -0.1371808d-11
      q5 = -0.320334d-14
!
      end subroutine INITIAL
!
!
!
      subroutine READFILE (lu,filename,ierr)
!-----------------------------------------------------------------------
!
!     Ref: JCGF0206
!
! --- OBJECT -----------------------------------------------------------
!
!     Reading the 6 files containing the ELP/MPP02 series 
!
! --- INPUT ------------------------------------------------------------
!
!     lu       : Logical unit of the files ELP/MPP02 (integer).
!     filename : Names of the files ELP/MPP02 (character*40).
!     elpcst   : Set of the constants of ELP/MPP02 solution (common).
!
! --- OUTPUT -----------------------------------------------------------
!
!     elpser   : Series of the ELP/MPP02 solution (common).
!     ierr     : Error file index (integer).
!                ierr=0 : no error.
!                ierr=1 : error file.
!
! --- Declarations -----------------------------------------------------
!
      implicit double precision (a-h,o-z),integer(i-n)
!
      character*40    filename(6)
      logical         fexist
!
      parameter       (max1=2645,max2=33256)
      parameter       (cpi=3.141592653589793d0)
      parameter       (pis2=cpi/2.d0,dpi=2.d0*cpi)
!
      dimension       b(5),ilu(4),ipla(11),ifi(16)
!
      common/elpcst/  w(3,0:4),eart(0:4),peri(0:4),zeta(0:4),del(4,0:4),
     &                p(8,0:4),delnu,dele,delg,delnp,delep,dtasm,am,
     &                p1,p2,p3,p4,p5,q1,q2,q3,q4,q5
!
      common/elpser/  cmpb(max1),fmpb(0:4,max1),nmpb(3,3),
     &                cper(max2),fper(0:4,max2),nper(3,0:3,3)
!
! --- Check up the files -----------------------------------------------
!
      ierr=1
      do i=1,6
         inquire (file=filename(i),exist=fexist)
         if (.not.fexist) return
      enddo
!
! --- Reading Main Problem series --------------------------------------
!
      ir=0
      do iv=1,3
      do k=1,3
         nmpb(iv,k)=0
      enddo
      enddo
!
      do iv=1,3
         open (lu,file=filename(iv),status='old',iostat=nerr)
         if (nerr.ne.0) return
         read (lu,1001,iostat=nerr,end=100) nmpb(iv,1)
         if (nerr.ne.0) return
         nmpb(iv,2)=ir+1
         nmpb(iv,3)=nmpb(iv,1)+nmpb(iv,2)-1
         do n=1,nmpb(iv,1)
            read (lu,1002,iostat=nerr,end=100) ilu,a,b
            if (nerr.ne.0) return
            ir=ir+1
            tgv=b(1)+dtasm*b(5)
            if (iv.eq.3) a=a-2.d0*a*delnu/3.d0
            cmpb(ir) = a+tgv*(delnp-am*delnu)
     &               + b(2)*delg + b(3)*dele + b(4)*delep
            do k=0,4
               fmpb(k,ir)=0.d0
               do i=1,4
                  fmpb(k,ir)=fmpb(k,ir)+ilu(i)*del(i,k)
               enddo
            enddo
            if (iv.eq.3) fmpb(0,ir)=fmpb(0,ir)+pis2
         enddo
         close (lu)
      enddo
!
! --- Reading Perturbations series -------------------------------------
!
      ir=0
      do iv=1,3
      do it=0,3
      do k=1,3
         nper(iv,it,k)=0
      enddo
      enddo
      enddo
!
      do iv=1,3
         open (lu,file=filename(iv+3),status='old',iostat=nerr) 
         if (nerr.ne.0) return
         do it=0,3
            read (lu,1003,iostat=nerr,end=100) nper(iv,it,1),ipt
            if (nerr.ne.0) return
            nper(iv,it,2)=ir+1
            nper(iv,it,3)=nper(iv,it,1)+nper(iv,it,2)-1
            if (nper(iv,it,1).eq.0) cycle
            do n=1,nper(iv,it,1)
               read (lu,1004,iostat=nerr,end=100) icount,s,c,ifi
               if (nerr.ne.0) return
               ir=ir+1
               cper(ir)=sqrt(c*c+s*s)
               pha=atan2(c,s)
               if (pha.lt.0.d0) pha=pha+dpi
               do k=0,4
                  fper(k,ir)=0.d0
                  if (k.eq.0) fper(k,ir)=pha
                  do i=1,4
                     fper(k,ir)=fper(k,ir)+ifi(i)*del(i,k)
                  enddo
                  do i=5,12
                     fper(k,ir)=fper(k,ir)+ifi(i)*p(i-4,k)
                  enddo
                  fper(k,ir)=fper(k,ir)+ifi(13)*zeta(k)
               enddo
            enddo
         enddo
         close (lu)
      enddo
!
! --- Exit -------------------------------------------------------------
!
      ierr=0
      return
!
! --- File error -------------------------------------------------------
!
100   continue
      ierr=1
      return
!
! --- Formats ----------------------------------------------------------
!
1001  format (25x,i10)
1002  format (4i3,2x,f13.5,5f12.2)
1003  format (25x,2i10)
1004  format(i5,2d20.13,16i3)
!
      end
!
!
!
      subroutine EVALUATE (tj,xyz)
!-----------------------------------------------------------------------
!
!     Ref: JCGF0206
!
! --- OBJECT -----------------------------------------------------------
!
!     Evaluation of the series ELP/MPP02.
!     Computation of the geocentric rectangular coordinates of the Moon
!     Frame: dynamical mean ecliptic and equinox of J2000.
!
! --- INPUT ------------------------------------------------------------
!
!     tj       : Time in days from J2000 (real*8).
!     elpcst   : Set of the constants of ELP/MPP02 solution (common).
!     elpser   : Series of the ELP/MPP02 solution (common).
!
! --- OUTPUT -----------------------------------------------------------
!
!     xyz(6)   : Geocentric rectangular coordinates (real*8).
!                xyz(1) : Position X (km)
!                xyz(2) : Position Y (km)
!                xyz(3) : Position Z (km)
!                xyz(4) : Velocity X' (km/day)
!                xyz(5) : Velocity Y' (km/day)
!                xyz(6) : Velocity Z' (km/day)
!
! --- Declarations -----------------------------------------------------
!
      implicit double precision (a-h,o-z),integer(i-n)
!
      dimension       t(0:4),xyz(6),v(6)
!
      parameter       (max1=2645,max2=33256)
      parameter       (cpi=3.141592653589793d0)
      parameter       (a405=384747.9613701725d0)
      parameter       (aelp=384747.980674318d0)
      parameter       (rad=648000.d0/cpi,sc=36525.d0)
!
      common/elpcst/  w(3,0:4),eart(0:4),peri(0:4),zeta(0:4),del(4,0:4),
     &                p(8,0:4),delnu,dele,delg,delnp,delep,dtasm,am,
     &                p1,p2,p3,p4,p5,q1,q2,q3,q4,q5
!
      common/elpser/  cmpb(max1),fmpb(0:4,max1),nmpb(3,3),
     &                cper(max2),fper(0:4,max2),nper(3,0:3,3)
!
! --- Initialization of time powers ------------------------------------

      t(0)=1.d0
      t(1)=tj/sc
      t(2)=t(1)*t(1)
      t(3)=t(2)*t(1)
      t(4)=t(3)*t(1)
!
! --- Evaluation of the series: substitution of time in the series -----
!     Variable iv=1 : Longitude
!     Variable iv=2 : Latitude
!     Variable iv=3 : Distance
!
      do iv=1,3
!
         v(iv)=0.d0
         v(iv+3)=0.d0
!
! ------ Main Problem series -------------------------------------------
!
         do n=nmpb(iv,2),nmpb(iv,3)
            x=cmpb(n)
            y=fmpb(0,n)
            yp=0.d0
            do k=1,4
               y=y+fmpb(k,n)*t(k)
               yp=yp+k*fmpb(k,n)*t(k-1)
            enddo
            v(iv)=v(iv)+x*sin(y)
            v(iv+3)=v(iv+3)+x*yp*cos(y)
         enddo
!
! ------ Perturbations series  -----------------------------------------
!
         do it=0,3
            do n=nper(iv,it,2),nper(iv,it,3)
               x=cper(n)
               y=fper(0,n)
               xp=0.d0
               yp=0.d0
               if (it.ne.0) xp=it*x*t(it-1)
               do k=1,4
                  y=y+fper(k,n)*t(k)
                  yp=yp+k*fper(k,n)*t(k-1)
               enddo
               v(iv)=v(iv)+x*t(it)*sin(y)
               v(iv+3)=v(iv+3)+xp*sin(y)+x*t(it)*yp*cos(y)
            enddo
         enddo
!
      enddo
!
! --- Computation of the rectangular coordinates (Epoch J2000) ---------           
!
      v(1)   = v(1)/rad
     &       + w(1,0)+w(1,1)*t(1)+w(1,2)*t(2)+w(1,3)*t(3)+w(1,4)*t(4)
      v(2)   = v(2)/rad
      v(3)   = v(3)*a405/aelp
      v(4)   = v(4)/rad
     &       + w(1,1)+2.d0*w(1,2)*t(1)+3.d0*w(1,3)*t(2)+4.d0*w(1,4)*t(3)
      v(5)   = v(5)/rad
!
      clamb  = cos(v(1))
      slamb  = sin(v(1))
      cbeta  = cos(v(2))
      sbeta  = sin(v(2))
      cw     = v(3)*cbeta
      sw     = v(3)*sbeta
!
      x1     = cw*clamb
      x2     = cw*slamb
      x3     = sw
      xp1    = (v(6)*cbeta-v(5)*sw)*clamb-v(4)*x2
      xp2    = (v(6)*cbeta-v(5)*sw)*slamb+v(4)*x1
      xp3    = v(6)*sbeta+v(5)*cw
!
      pw     = (p1+p2*t(1)+p3*t(2)+p4*t(3)+p5*t(4))*t(1)
      qw     = (q1+q2*t(1)+q3*t(2)+q4*t(3)+q5*t(4))*t(1)
      ra     = 2.d0*sqrt(1-pw*pw-qw*qw)
      pwqw   = 2.d0*pw*qw
      pw2    = 1.d0-2.d0*pw*pw
      qw2    = 1.d0-2.d0*qw*qw
      pwra   = pw*ra
      qwra   = qw*ra
!
      xyz(1) = pw2*x1+pwqw*x2+pwra*x3
      xyz(2) = pwqw*x1+qw2*x2-qwra*x3
      xyz(3) = -pwra*x1+qwra*x2+(pw2+qw2-1)*x3
!
      ppw    = p1+(2.d0*p2+3.d0*p3*t(1)+4.d0*p4*t(2)+5.d0*p5*t(3))*t(1)
      qpw    = q1+(2.d0*q2+3.d0*q3*t(1)+4.d0*q4*t(2)+5.d0*q5*t(3))*t(1)
      ppw2   = -4.d0*pw*ppw
      qpw2   = -4.d0*qw*qpw
      ppwqpw = 2.d0*(ppw*qw+pw*qpw)
      rap    = (ppw2+qpw2)/ra
      ppwra  = ppw*ra+pw*rap
      qpwra  = qpw*ra+qw*rap
!
      xyz(4) = (pw2*xp1+pwqw*xp2+pwra*xp3
     &       + ppw2*x1+ppwqpw*x2+ppwra*x3)/sc
      xyz(5) = (pwqw*xp1+qw2*xp2-qwra*xp3
     &       + ppwqpw*x1+qpw2*x2-qpwra*x3)/sc
      xyz(6) = (-pwra*xp1+qwra*xp2+(pw2+qw2-1.d0)*xp3
     &       - ppwra*x1+qpwra*x2+(ppw2+qpw2)*x3)/sc
!
      return
      end
