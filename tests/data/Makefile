MP3S = null-noid3.mp3 null-v1.mp3 null-v2.mp3

LAME_OPTS = --ta "Null Artist" \
	    --tl "Null Album" \
	    --tt "Null Title"
LAME_V1_OPTS = $(LAME_OPTS) --id3v1-only
LAME_V2_OPTS = $(LAME_OPTS) --id3v2-only

all: $(MP3S)

null-noid3.mp3: null
	lame -r $< $@

null-v1.mp3: null
	lame -r $(LAME_V1_OPTS) $< $@

null-v2.mp3: null
	lame -r $(LAME_V2_OPTS) $< $@

clean:
	rm -f $(MP3S)
