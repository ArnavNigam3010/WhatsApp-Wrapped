# WhatsApp-Wrapped SSL Project

This is a project done for the SSL course at IITB. It involves a WhatsApp Chat generator, parser (analyzer) and web dev in form of a wrapped experience.

## Description

The project consists of 3 main parts:
1. Chat Generator:
   This generates a WhatsApp like chat, with 10 people and different personalities implemented. The code probabistically chooses which person will message, the length of the message and the kind of message based on each personality. These probabilities are also skewed on basis of factors like time of the day, previous message, etc.
   The goal is to create a realistic and randomized chat, but with clear personalities at the same time.
2. Chat Parser:
   Analyzes the chat and stores various properties in a JSON file. Identifies personalities of the chat members based on various factors.
3. Web Development:
   This involves HTML, CSS, and JS files to create a website which will show the data accumulated by parser in visually appealing way, in the form of a Wrapped Experience.
   The JS file uses the JSON file to obtain data to use for the website. Global statistics and member profiles and personalities are shown in the website.

The speciality is that these components are completely independent; the chat generator works on any vocabulary, the parser works on any chat, and the JS is only dependent on the JSON file.
## Getting Started

### Dependencies
Following libraries were used
1. numpy: For array handling in chat generator and analyser.
2. random: to generate random probability distributions required for chat generation.
3. datetime: to work efficiently with dates and time while generating and analysing chat.
4. re: to identify emojis using unicode.
5. json: to use json file for data from chat to analyse it.
6. chart.js: to make various charts and graphs to represent data in final wrapped website.
7. sys: To include command line arguments in the python scripts

### Installing

Download the Git Repository as is.

### Executing program
All execution will happen in the the main WhatsApp-Wrapped SSL Project directory. (Which contains generator and parser directories.)
Use python in Windows Powershell and python3 in Linux terminal.
1. Generating chat. Run
```
python3 generator/chat.py vocabulary.txt

```
2. Parsing chat. Run
```
python3 parser/analyze.py chat.txt

```
3. Seeing website. Run
```
python3 -m http.server 8000

```
Then go to following URL
```
http://localhost:8000/web/index.html

```

## Authors
Parth Vartak

Arnav Nigam
