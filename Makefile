all: midas CRdiff

clean:
	rm -f *.aux *.bbl *.blg *.fdb_latexmk *.fls *.log *.out *.synctex.gz *.dvi
	rm Midas.pdf latexdiff.pdf

.PHONY: all clean midas

midas:
	rubber --pdf Midas.tex

# CRdiff:
# 	latexdiff TikTok_usenix22.tex --exclude-textcmd="tocttou" --exclude-textcmd="midas" Midas.tex  > latexdiff.tex 
# 	-rubber --pdf latexdiff.tex

CRdiff:
	git show 972d1a40e787faf33bdf1d0a036af0cd4e8099eb:TikTok_usenix21.tex > diff.tex
	sed -i 's/\\newcommand\\tiktok/%/g' diff.tex
	sed -i 's/\\tiktok/TikTok/g' diff.tex
	sed 's/\\newcommand\\midas/\%/g' Midas.tex > midas.tex
	sed -i 's/\\midas/Midas/g' midas.tex
	latexdiff diff.tex midas.tex --disable-citation-markup --config="PICTUREENV=(?:picture|DIFnomarkup|align|tabular)[\w\d*@]*" > sec22CR_diff.tex
	-rubber --unsafe --pdf sec22CR_diff.tex
	rm diff.tex midas.tex sec22CR_diff.tex

.PHONY: revision
revision: *.md
	pandoc oakland21-fall.md -o oakland21-fall.pdf
	pandoc oakland21-response.md -o oakland21-response.pdf
	latexdiff TikTok_oakland21.tex Midas.tex --exclude-textcmd="section,subsection,table,table*" --config="PICTUREENV=(?:picture|DIFnomarkup|align|tabular)[\w\d*@]*" > latexdiff.tex
	-rubber --pdf latexdiff.tex
	pdftk oakland21-response.pdf oakland21-fall.pdf TikTok_oakland21.pdf latexdiff.pdf cat output previous_submission.pdf
