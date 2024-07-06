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
cd /home/cesar/Documents/Proyectos/Calendario_GL_2023/Escritorio/pdf
for i in *.pdf
do
  gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH -sOutputFile=op/$i $i
done
cd /home/cesar/Documents/Proyectos/Calendario_GL_2023/Pared/pdf
for i in *.pdf
do
  gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH -sOutputFile=op/$i $i
done
cd /home/cesar/Documents/Proyectos/Calendario_GL_2023

