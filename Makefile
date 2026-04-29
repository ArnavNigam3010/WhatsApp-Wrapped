.PHONY: all clean
all: ProjectReport.pdf
ProjectReport.pdf: ProjectReport.tex references.bib flowchart.png
	pdflatex ProjectReport.tex
	bibtex ProjectReport
	pdflatex ProjectReport.tex
	pdflatex ProjectReport.tex
clean: 
	rm -f *.aux *.bbl *.blg *.log *.out *.toc
