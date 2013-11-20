echo ==========================================================
echo  Linux version of Egg Build
echo ==========================================================
echo Check and build HTML from Lore files
lore --config template=template.tpl --inputext=.lore
lore --config template=template.tpl --inputext=.lore --output=latex --config section
cd Gateway
cd User
echo Building User.tex
#latex --language=LaTeX --output=pdf --clean User.tex
echo  ==================================================
echo   HTML and LATEX may have built, ToDo Egg creation
echo  ==================================================
