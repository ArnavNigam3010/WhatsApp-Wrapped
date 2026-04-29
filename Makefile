.PHONY: all clean
all: ProjectReport.pdf
ProjectReport.pdf: ProjectReport.tex references.bib
	pdflatex ProjectReport.tex
	bibtex ProjectReport.aux
	pdflatex ProjectReport.tex
	pdflatex ProjectReport.tex
ProjectReport.tex: flowchart.png references.bib
clean: 
	rm -f *.aux *.bbl *.blg *.log *.out *.toc
