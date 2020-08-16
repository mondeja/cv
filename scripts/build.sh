#!/bin/bash

EXTENSIONS_TO_CLEAN=(
  "lua"
  "timestamp"
  "aux"
  "bcf"
  "log"
  "out"
  "xml"
  "xmpi"
)

function cleanSrcDirectory {
  for filepath in src/*; do
    filename=$(printf "%s" "$filepath" | cut -d'/' -f2)
    extension=${filename##*.}

    if [[ ! " ${EXTENSIONS_TO_CLEAN[@]} " =~ " ${extension} " ]]; then
      continue
    fi;

    rm $filepath
  done
}


function main {
  # Iterate over language files
  find i18n -maxdepth 1 -type f -name '*.yml' | while read -r lang_filepath; do
    lang=$(basename "$lang_filepath" | cut -d'.' -f1)

    if [ -f "main.$lang.tex" ]; then
      rm main.$lang.tex
    fi;

    # Render `main.template.tex` file using the language
    python scripts/render_template.py "$lang" > src/main.$lang.tex

    cd src

    pdflatex main.$lang.tex
    pdflatex main.$lang.tex

    rm main.$lang.tex
    cd ..

    cleanSrcDirectory

    mv src/main.$lang.pdf dist/$lang.pdf

  done;
}

main
