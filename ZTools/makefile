# Unix C makefile for the Infocom tools

CC = cc
NROFF	= nroff

#Some systems declare getopt, others do not.  Pick whichever works
#CFLAGS = -O -DHAS_GETOPT
CFLAGS = -O
LDFLAGS =
LIBS =


.SUFFIXES: .c .h .1 .man

.1.man:
	$(NROFF) -man $*.1 | col -b > $*.man

MANPAGES = infodump.1 txd.1
FORMATTEDMAN = $(MANPAGES:.1=.man)


IINC = tx.h
IOBJS = infodump.o showhead.o showdict.o showobj.o showverb.o txio.o infinfo.o symbols.o

TINC = tx.h
TOBJS = txd.o txio.o showverb.o infinfo.o symbols.o showobj.o

all : infodump txd doc

infodump : $(IOBJS)
	$(CC) -o $@ $(LDFLAGS) $(IOBJS) $(LIBS)

$(IOBJS) : $(IINC)

txd : $(TOBJS)
	$(CC) -o $@ $(LDFLAGS) $(TOBJS) $(LIBS)

$(TOBJS) : $(TINC)

clean :
	-rm *.o infodump txd $(FORMATTEDMAN)

doc: $(FORMATTEDMAN)
