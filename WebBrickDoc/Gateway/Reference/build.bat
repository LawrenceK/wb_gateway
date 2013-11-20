lore.py --config template=../../template.tpl --inputext=.lore

REM PROBLEMS. Lore converts png to eps for latex to use. this causes issues for miktex.

lore.py --config template=../../template.tpl --inputext=.lore --output=latex --config section

texify --language=LaTeX --pdf --clean Reference.tex
