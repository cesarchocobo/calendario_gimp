yyyy=2024
flatpak run org.gimp.GIMP --batch-interpreter python-fu-eval -b "import sys; sys.path=['.']+sys.path; import script_assets; script_assets.calendario_P($yyyy)" -b "pdb.gimp_quit(1)"
flatpak run org.gimp.GIMP --batch-interpreter python-fu-eval -b "import sys; sys.path=['.']+sys.path; import script_assets; script_assets.calendario_E($yyyy)" -b "pdb.gimp_quit(1)"
flatpak run org.gimp.GIMP --batch-interpreter python-fu-eval -b "import sys; sys.path=['.']+sys.path; import script_assets; script_assets.numeros('Gold Logistic')" -b "pdb.gimp_quit(1)"
flatpak run org.gimp.GIMP -idf --batch-interpreter python-fu-eval -b "import sys; sys.path=['.']+sys.path; import script_assets; script_assets.label_meses()" -b "pdb.gimp_quit(1)"
flatpak run org.gimp.GIMP -idf --batch-interpreter python-fu-eval -b "import sys; sys.path=['.']+sys.path; import script_assets; script_assets.label_anios($yyyy)" -b "pdb.gimp_quit(1)"
flatpak run org.gimp.GIMP -idf --batch-interpreter python-fu-eval -b "import sys; sys.path=['.']+sys.path; import script_assets; script_assets.pared_all($yyyy)" -b "pdb.gimp_quit(1)"
flatpak run org.gimp.GIMP -idf --batch-interpreter python-fu-eval -b "import sys; sys.path=['.']+sys.path; import script_assets; script_assets.escritorio_all($yyyy)" -b "pdb.gimp_quit(1)"
flatpak run org.gimp.GIMP -idf --batch-interpreter python-fu-eval -b "import sys; sys.path=['.']+sys.path; import script_assets; script_assets.escritorio_full()" -b "pdb.gimp_quit(1)"
for (( i=1; i<=14; i++ ))
do
  convert Pared/$i.png -units pixelsperinch -density 300 -page 4145x2102 Pared/pdf/$i.pdf
done
convert Pared/portada.png -units pixelsperinch -density 300 -page 4287x2752 Pared/pdf/portada.pdf
for (( i=1; i<=12; i++ ))
do
  convert Escritorio/$i.png -units pixelsperinch -density 300 -page 2752x1630 Escritorio/pdf/$i.pdf
done
convert Escritorio/portada.png -units pixelsperinch -density 300 -page 2752x1630 Escritorio/pdf/portada.pdf
convert Escritorio/anual.png -units pixelsperinch -density 300 -page 2752x1630 Escritorio/pdf/anual.pdf
cd carpeta/Escritorio/pdf
for i in *.pdf
do
  gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH -sOutputFile=op/$i $i
done
cd carpeta/Pared/pdf
for i in *.pdf
do
  gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH -sOutputFile=op/$i $i
done
cd carpeta
convert Pared/portada.png -quality 50% -resize 700x700 muestra_portada_pared.png
convert Pared/1.png -quality 50% -resize 700x700 muestra_pared.png
convert Escritorio/portada.png -quality 50% -resize 700x700 muestra_portada_escritorio.png
convert Escritorio/1.png -quality 50% -resize 700x700 muestra_escritorio.png
