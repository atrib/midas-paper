all: tiktok

clean:
	rm -f *.aux *.bbl *.blg *.fdb_latexmk *.fls *.log *.out *.pdf *.synctex.gz *.dvi

.PHONY: all clean

tiktok:
	rubber --pdf TikTok.tex