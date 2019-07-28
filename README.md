# Which CSS class are still in used

Little program in Python 3.6, which checks in each css file, the class still used in the html files according to the chosen paths.


# Options

 - Deep search for CSS

>  Search CSS file in every subdirectory

## To do

 - [ ] Rewrite CSS File
 - [ ] Show unused classes
 - [ ] Show in which HTML files the class is used

## Library needed

 - TKinter
 - CSSselect
 - CSSutils
 - LXML

## Compilation

You can use *cx_Freeze* for the compilation

    python3.6 setup.py build
