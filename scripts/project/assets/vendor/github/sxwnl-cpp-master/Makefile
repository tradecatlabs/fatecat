BUILD_PATH	:= build
VPATH	:= eph : lunar : draw : test : mylib

OBJ0	:= eph0.o eph.o eph_msc.o eph_rsgs.o eph_rspl.o eph_yspl.o \
eph_szj.o eph_show.o lunar.o lunar_ob.o lunar_ssq.o tool.o lat_lon_data.o

OBJ1	:= test1.o $(OBJ0)
OBJ2	:= test.o $(OBJ0)
LIBS	:= -lm
FLAG    := -fexceptions -std=c++11
ifdef CXXFLAGS
    CXXFLAGS := $(CXXFLAGS) $(FLAG)
else
    CXXFLAGS := -Os $(FLAG)
endif



TARGET  = mytest

all: test1 test0
test1: $(OBJ1)
	$(CXX) $(CXXFLAGS) $(LIBS) $^ -o $@
test0: $(OBJ2)
	$(CXX) $(CXXFLAGS) $(LIBS) $^ -o $@
.PHONY: test1 test0 clean cleanw
clean:
	rm -rf *.o test1 test0
cleanw:
	del *.o test1 test0