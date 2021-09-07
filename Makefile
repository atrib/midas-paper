all: tiktok CRdiff

clean:
	rm -f *.aux *.bbl *.blg *.fdb_latexmk *.fls *.log *.out *.synctex.gz *.dvi
	rm TikTok.pdf latexdiff.pdf

.PHONY: all clean tiktok

tiktok:
	rubber --pdf TikTok.tex

CRdiff:
	latexdiff TikTok_usenix22.tex TikTok.tex  --exclude-textcmd="section,subsection,table,table*" --config="PICTUREENV=(?:picture|DIFnomarkup|align|tabular)[\w\d*@]*" > latexdiff.tex
	-rubber --pdf latexdiff.tex

.PHONY: revision
revision: *.md
	pandoc oakland21-fall.md -o oakland21-fall.pdf
	pandoc oakland21-response.md -o oakland21-response.pdf
	latexdiff TikTok_oakland21.tex TikTok.tex --exclude-textcmd="section,subsection,table,table*" --config="PICTUREENV=(?:picture|DIFnomarkup|align|tabular)[\w\d*@]*" > latexdiff.tex
	-rubber --pdf latexdiff.tex
	pdftk oakland21-response.pdf oakland21-fall.pdf TikTok_oakland21.pdf latexdiff.pdf cat output previous_submission.pdf
