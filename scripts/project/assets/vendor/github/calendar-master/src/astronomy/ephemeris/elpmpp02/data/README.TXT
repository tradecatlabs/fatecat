
 ==================== SYRTE - PARIS OBSERVATORY - FRANCE ====================

                           LUNAR SOLUTION ELP/MPP02

                                 December 2002

 ==================== SYRTE - PARIS OBSERVATORY - FRANCE ====================


 Jean Chapront      jean.chapront@obspm.fr
 Michelle Chapront  michelle.chapront@obspm.fr
 Gerard Francou     gerard.francou@obspm.fr

 Observatoire de Paris - SYRTE (UMR 8630/CNRS)
 61, avenue de l'Observatoire
 75014 Paris - France


 ELP/MPP02 (Chapront, Francou, 2003) is a semi-analytical solution for the 
 orbital motion of the Moon. 
 
 It is built on the basis of the lunar theories:
 - ELP 2000-82 (Chapront-Touze, Chapront, 1983), 
 - ELP 2000-85 (Chapront-Touze, Chapront, 1988),
 - ELP 2000-96, version used for analysing Lunar Laser Ranging (LLR).
 
 The main differences from the previous solution 'ELP 2000-82B' is the use 
 of the new planetary perturbations MPP01 (Bidart, 2000) and the contribution 
 of the LLR observations provided since 1970.

 Like the previous versions, ELP/MPP02 includes:
 - the solution of the Main Problem 'Earth, Moon, Sun' with a keplerian orbit 
   for the Earth-Moon barycenter (EMB) including partials with respect to 
   various constants and parameters;
 - the direct and indirect planetary perturbations that contain in particular 
   the effects of the secular motions in eccentricity and perihelion of the 
   Earth-Moon barycenter EMB and the secular motion of the ecliptic; 
 - the Earth's figure perturbations, and the Moon's figure perturbations
   coupling with libration; 
 - the relativistic effects and the tidal perturbations;
 
 Some parameters or constants used in ELP/MPP02 have 'nominal values' which 
 are corrected with adjustments resulting from the fit of the solution to 
 observations. The partial derivatives given together with the series of the 
 Main Problem allow to do these corrections. 
 
 ELP/MPP02, proposes two ways for computing the lunar coordinates:  
 - to use corrections obtained by the fit to Laser Lunar Ranging data (LLR);
 - to use corrections obtained by the fit to the numerical integration DE405 
   of the Jet Propulsion Laboratory (Standish, 1998)) used as an observing 
   model; in that case some additive corrections are also applied to secular 
   values of the lunar angles for approaching closer the JPL Ephemeris over 
   6000 years.
   
 The construction of ELP/MPP02 is explained in the note 'elpmpp02.pdf'. 
 Explanatory comments about the original ELP2000-82 series are also given in 
 the technical note concerning the Lunar solution ELP 2000-82B. 
 
 The series of the lunar solution ELP/MPP02 are separated in 2 parts,  
 the Main Problem and the perturbations listed above and brought together, 
 for the each geocentric coordinate: Longitude, Latitude and Distance. 
 At all, there are 6 data files containing the ELP/MPP02 Series.
 
 The FORTRAN subroutine 'ELPMPP02' (in file 'elpmpp02.for') allows to compute 
 rectangular geocentric lunar coordinates (X,Y,Z)  referred to the inertial 
 mean ecliptic and equinox of J2000.  
 
 
 Files list:
 README.TXT    : This file
 elpmpp02.pdf  : Explanatory Note about ELP/MPP02 solution
 elpmpp02.for  : Fortran subroutine for using ELP/MPP02 Series
 ELP-MAIN.S1   : Series 'Main problem  - Longitude' 
 ELP-MAIN.S2   : Series 'Main problem  - Latitude' 
 ELP-MAIN.S3   : Series 'Main problem  - Distance' 
 ELP-PERT.S1   : Series 'Perturbations - Longitude' 
 ELP-PERT.S2   : Series 'Perturbations - Latitude' 
 ELP-PERT.S3   : Series 'Perturbations - Distance' 


 References:

 Chapront-Touze M., Chapront J., 1983:
 The lunar Ephemeris ELP 2000,
 Astronomy and Astrophysics, 124, 50.
 
 Chapront-Touze M., Chapront J., 1988:
 ELP 2000-85: a semi-analytical lunar ephemeris adequate for historial times, 
 Astronomy and Astrophysics, 190, 342.
 
 Standish E.M., 1998:
 JPL Planetary and Lunar ephemerides, DE405/LE405,
 Jet Propulsion Laboratory, InterOffice Memorandum, IOM, 321.F-98-048.
 
 Bidart P., 2001:
 MPP01, a new solution for planetary perturbations in the orbital motion 
 of the Moon,
 Astronomy and Astrophysics, 366, 351.
 
 Chapront J., Francou G., 2003: 
 The lunar theory ELP revisited. Introduction of new planetary perturbations, 
 Astronomy and Astrophysics, 404, 735.
 
 (end of document)
 
 