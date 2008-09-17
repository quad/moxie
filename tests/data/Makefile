LAME=/usr/bin/lame
LAME_TAGS=--ta "Null Artist" --tl "Null Album" --tt "Null Title"

all: null-v1.mp3 null-v2.mp3 null-noid3.mp3

null:
	touch null

null-v1.mp3: null
	$(LAME) $(LAME_TAGS) --id3v1-only $? $@

null-v2.mp3: null
	$(LAME) $(LAME_TAGS) --id3v2-only $? $@

null-noid3.mp3: null
	$(LAME) $? $@

clean:
	-rm null *.mp3
