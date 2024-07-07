# calendario_gimp
Creacion de calendario usando python y gimp


Hace tiempo me pidieron hacer un calendario para una compañía, estos calendarios se imprimen cada año y la compañía se los regala a sus socios. En lugar de usar un programa ya hecho para hacer calendarios como miscrosoft publisher o algo parecido, decidí hacer mi propio script utilizando Gimp y su implementacion de python-fu para automatizar el proceso. Python-fu solo puede usarse dentro de Gimp, asi que es necesario primero brir Gimp y despues ejecutar el script. para esto, escribí un script en bash que se encarga de ejecutar Gimp, correr python-fu y cerrarlo.

## Concepto

La idea del script es que genere cada una de las paginas de dos tipos de calendario, uno de escritorio y uno de pared. EN el script solo es necesario indicar el año del calendario y las fechas de los dias feriados, para que se marquen en otro color. El estilo del calendario, incluyendo los colores, las fuentes e imagenes utilizadas están predefinidas, aunque algunas cosas se van a editar en el mismo script. Las paginas generadas deben ser de alta calidad para que se vean bien en una impresion, por lo tanto, se generarán archivos pdf listos apra impresion de cada pagina.

## Codigo

El archivo que contiene todos los scripts es script_assets.py. En este script se generaran las fechas del calendario y algunos otros elementos, tambien se incluyen funiones que editan el calendario con las fechas de un año en especifico. Cada que se requiera un nuevo calendario, hay que ejecutar el script con el año indicado. Empezamos por importar las paqueterias necesarias, proveer una lista de los dias feriados en formato [mes, dia], y especificar la carpeta donde estaran las imagenes y otros assets necesarios apra generar el calendario.

```
import os, glob, sys, time, calendar
from gimpfu import *

carpeta = '/home/cesar/Documents/Proyectos/Calendario_GL/'
feriados = [[1,1],[2,5],[3,18],[5,1],[9,16],[11,18],[12,25]]
```

La primera funcion definida es `calendario_P(yyyy)`, donde el argumento es el año del calendario. Se empieza por definir la funcion y algunos colores que se usaran en los numeros del calendario, esto es cuestion de estilo.

```
def calendario_P(yyyy):
    yy = yyyy
    azul = gimpcolor.RGB(31,63,156)
    rojo = gimpcolor.RGB(255,0,0)
    verde = gimpcolor.RGB(67, 171, 59)
    gris = gimpcolor.RGB(233,233,233)
    gris2 = gimpcolor.RGB(101, 98, 99)
```

Despues se ccrea un objeto calendar de la paqueteria calendar. Por supuesto, este objeto es el que va a contener todas las fechas. El argumento 0 en el objeto calendario indica cual es el primer dia de la semana (en este caso, iniciamos en lunes). Tambin se definen algunas coordenas que son en donde se colocaran cada una de las fechas en la pagina del calendario. Estas coordenadas están dadas segun el estilo que se le quiera dar al calendario. Se definen dos listas `offX1` y `offX2` estas listas representan la posicion en la coordenada x de las fechas. Como hay fechas con un digito y fechas con dos digitos, deben colocarse en posiciones ligeramente distintas para que se vean centradas. La diferencia de posicion horizontal entre estos dos tipos de fechas esta representad apor la variable `Ct`. dependiendo de la fuente y tamao del texto en el calendario, estos valore svan a cambair. Tambien se tienen dos listas para la posicion vertical ya que algunos elementos tienen distinto tamaño. AL final, las variables `tama1` y `tama2` definen el tamaño de estos elementos.

```
 obj = calendar.Calendar(0)
    Px = [866, 1328, 1781, 2248, 2704, 3163, 3627]
    Ct = 66
    offX1 = [Px[0]-Ct, Px[1]-Ct, Px[2]-Ct, Px[3]-Ct, Px[4]-Ct, Px[5]-Ct, Px[6]-Ct] 
    offX2 = [Px[0], Px[1], Px[2], Px[3], Px[4], Px[5], Px[6]] 
    offX = offX1
    offy = [808, 1027, 1248, 1470, 1688, 1688]
    offy2 = [0, 836, 1056, 1276, 1496, 1716, 1716]
    wcount = 0 
    tama1 = 228
    tama2 = 172
```


Comenzamos con un ciclo para iterar en los meses del calendario, carga una imagen en gimp donde se creará esté calendario y se inicia un contador cuya funcion se detalla más adelante

```
    for m in range(1,13):
        image = pdb.gimp_image_new(5000, 3000, 0)
        ycount = 0
```

Despues, para cada uno de estos meses, se itera sobre todos los dias de dicho mes
```
for n in obj.itermonthdays(yy, m):
```

Primero se buscan los numeros que ser'am grises, es decir, los numeros que no corresponden al més en cuestion, sino al siguiente o al anterior. Se define su color con una funcion de Gimp y su posicion en x

```
            if n == 0:
                gimp.set_foreground(gris)
                offX = offX1 
```

Despues definimos que pasá si estamos en el primer mes. La variable j guarda el dia del mes. notese que se define como los dias del mes de diciembre del año pasado menos los dias del mes del año actual + la variable de iteracion i + 1. Esto nos va a dar los del mes anterior que quedan en la misma semana que la semana inicial del mes actual. Posteriormente se pone el texto del numero de dia en la imagen, definiendo la fuente que se va a utilziar para estas fechas, la cual en este caso es "Myriad Pro Bold" Finalmente se. Despues se crea la capa yfinalmente se une la capa a la imagen para poder exportarla.

```
               if m == 1:
                    for i in range(calendar.weekday(yy, m, 1)):
                        j = calendar.monthrange(yy-1, 12)[1]-calendar.weekday(yy, m, 1)+i +1
                        dayB = pdb.gimp_text_fontname(image, None, 0, 0, str(j), 1, True, tama1, PIXELS, "Myriad Pro Bold")
                        pdb.gimp_layer_set_offsets(dayB, offX[calendar.weekday(yy-1, 12, j)], offy[0])
                        Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)
```

Para los demas meses del calendario, el codigo es similar, solo que ya no se necesita considerar el año anterior, solo el ems anterior del mismo año, por eso se toma como un caso aparte

```
                else:
                    for i in range(calendar.weekday(yy, m, 1)):
                        j = calendar.monthrange(yy, m-1)[1]-calendar.weekday(yy, m, 1)+ i +1
                        dayB = pdb.gimp_text_fontname(image, None, 0, 0, str(j), 1, True, tama1, PIXELS, "Myriad Pro Bold")
                        pdb.gimp_layer_set_offsets(dayB, offX[calendar.weekday(yy, m-1, j)], offy[0])                   
                        Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)
```

Ahora sí, empezamos a poner los dias del mes actual. Primero ponemos una serie de ifs para distinguir los dias normales, de los domingfos y los feriados, dependiendo de que tipo de dia sea, su color será distinto. Tambien se distingue si la fecha tiene un digito mas  con el primer if.

```
            else:
                if n < 10:
                    offX = offX2
                else:
                    offX = offX1 
                if [m,n] in feriados:
                    gimp.set_foreground(verde)
                elif calendar.weekday(yy, m, n) == 6:
                    gimp.set_foreground(rojo)
                else:
                    gimp.set_foreground(azul)
```
Con estas ditinciones hechas, se scribe el numero y se pone la capa en la imagen

```
                dayT = pdb.gimp_text_fontname(image, None, 0, 0, str(n), 1, True, tama1, PIXELS, "Myriad Pro Bold")
                pdb.gimp_layer_set_offsets(dayT, offX[calendar.weekday(yy, m, n)], offy[ycount])
```

Finalmente, se pone una columna extra para indicar el numero de semana. El primer if se utiliza para contar cuantas semanas tiene el mes, cada que el dia es domingo, aumenta en uno el contador local ycount y el contador global wcount. Se cambia el color del texto y se escribe el numero de semana (es decir, wcount), se agrega la capa y al final se fusionan todas las capas con la imagen.
```
                if calendar.weekday(yy, m, n) == 6:
                    ycount = ycount + 1
                    wcount = wcount + 1
                    gimp.set_foreground(gris2)
                    weekN =  pdb.gimp_text_fontname(image, None, 0, 0, str(wcount), 1, True, tama2, PIXELS, "Myriad Pro Bold")
                    pdb.gimp_layer_set_offsets(weekN, 376, offy2[ycount])
                Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)              
```

El siguiente codigo pone fechas del sieguente mes en la ultima semana (de manera similar a como se pusieron dias del mes anterior en la primer semana). Esto solo se va a hacer cuando sobre lugares en el calendario, es decir, cuando ycount sea menor que 5. Empezamos definiendo los estilos y poniendo el numero de semana correspondiente

```
        if ycount < 5:
            gimp.set_foreground(gris2)
            weekN =  pdb.gimp_text_fontname(image, None, 0, 0, str(wcount+1), 1, True, tama2, PIXELS, "Myriad Pro Bold")
            pdb.gimp_layer_set_offsets(weekN, 376, offy2[ycount+1])
            gimp.set_foreground(gris)
            offX  = offX2   
```

Despues se ponen las fechas. Tambien debemos separar en dos casos ya que el ultimo mes incluita dias del siguiente año.

```
            if m == 12:
                for l in range(6-calendar.weekday(yy, m, calendar.monthrange(yy, m)[1])):
                    dayA = pdb.gimp_text_fontname(image, None, 0, 0, str(l+1), 1, True, tama1, PIXELS, "Myriad Pro Bold")
                    pdb.gimp_layer_set_offsets(dayA, offX[calendar.weekday(yy+1, 1, l+1)], offy[4])
                    Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)
            else:
                for l in range(6-calendar.weekday(yy, m, calendar.monthrange(yy, m)[1])):
                    dayA = pdb.gimp_text_fontname(image, None, 0, 0, str(l+1), 1, True, tama1, PIXELS, "Myriad Pro Bold")
                    pdb.gimp_layer_set_offsets(dayA, offX[calendar.weekday(yy, m+1, l+1)], offy[4])
                    Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)    
```

Por cuestiones de estilo, se quiere que los calendarios solo tengan 4 semanas escritas, si algun mes llega a tener cinco semanas, los dias se colocan en una doble fila, asi que hay que poner un pedazo de codigo para distinguir estos casos y que formatee la imagen con el estilo adecuado.
```
       else:   #Poniendo filas dobles en la ultima semana
            if calendar.weekday(yy, m, calendar.monthrange(yy, m)[1]) < 6:
                for s in range(calendar.weekday(yy, m, calendar.monthrange(yy, m)[1]) + 1):
                    #Se borra el numero que se habia puesto antes
                    pdb.gimp_rect_select(image, offX1[s], offy[4], 250, 180, 0, False, 0)
                    floating_sel = pdb.gimp_selection_float(image.layers[0], offX1[s], offy[4])
                    pdb.gimp_edit_clear(floating_sel)
                    pdb.gimp_image_remove_layer(image, floating_sel)
                    #Se ponen los nuevos numeros pequenos y se acomodan en la doble fila
                    if [m,calendar.monthrange(yy, m)[1] - calendar.weekday(yy, m, calendar.monthrange(yy, m)[1]) + s -7] in feriados:
                        gimp.set_foreground(verde)
                    else: 
                        gimp.set_foreground(azul)
                    dayD1 = pdb.gimp_text_fontname(image, None, 0, 0, str(calendar.monthrange(yy, m)[1] - calendar.weekday(yy, m, calendar.monthrange(yy, m)[1]) + s -7), 1, True, 120, PIXELS, "Myriad Pro Bold")
                    if [m,calendar.monthrange(yy, m)[1] - calendar.weekday(yy, m, calendar.monthrange(yy, m)[1]) + s] in feriados:
                        gimp.set_foreground(verde)
                    else: 
                        gimp.set_foreground(azul)
                    dayD2 = pdb.gimp_text_fontname(image, None, 0, 0, str(calendar.monthrange(yy, m)[1] - calendar.weekday(yy, m, calendar.monthrange(yy, m)[1]) + s), 1, True, 120, PIXELS, "Myriad Pro Bold")
                    gimp.set_foreground(azul)
                    dayDs = pdb.gimp_text_fontname(image, None, 0, 0, '/', 1, True, 200, PIXELS, "Myriad Pro")
                    pdb.gimp_layer_set_offsets(dayD1, offX1[s]- 20, offy[4])
                    pdb.gimp_layer_set_offsets(dayD2, offX1[s] + 150, offy[4]+ 70)
                    pdb.gimp_layer_set_offsets(dayDs, offX1[s] + 100, offy[4])
                    Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)
```

Despues de definir el formato, se ponen los numeros de semana. Aqui revisamos si ya llegamos al final del año para reinicial el contador de semanas.

```
                #Se pone el numero de semana en la doble fila
                #Se borra el numero de fila
                gimp.set_foreground(gris2)
                pdb.gimp_rect_select(image, 370, offy2[5], 250, 180, 0, False, 0)
                floating_sel = pdb.gimp_selection_float(image.layers[0], 370, offy2[5])
                pdb.gimp_edit_clear(floating_sel)
                pdb.gimp_image_remove_layer(image, floating_sel)                   
                #Checamos si se sigue el contador o se reinicia por ser diciembre
                if m == 12:    
                    dayD1 = pdb.gimp_text_fontname(image, None, 0, 0, str(wcount), 1, True, 90, PIXELS, "Myriad Pro Bold")
                    dayD2 = pdb.gimp_text_fontname(image, None, 0, 0, str(1), 1, True, 90, PIXELS, "Myriad Pro Bold")
                else:
                    dayD1 = pdb.gimp_text_fontname(image, None, 0, 0, str(wcount), 1, True, 90, PIXELS, "Myriad Pro Bold")
                    dayD2 = pdb.gimp_text_fontname(image, None, 0, 0, str(wcount + 1), 1, True, 90, PIXELS, "Myriad Pro Bold")
                #Se ponen los numeros de semana pequenos en la doble fila
                dayDs = pdb.gimp_text_fontname(image, None, 0, 0, '/', 1, True, 150, PIXELS, "Myriad Pro")   
                pdb.gimp_layer_set_offsets(dayD1, 376 - 10, offy2[5])
                pdb.gimp_layer_set_offsets(dayD2, 376 + 90, offy2[5]+ 50)
                pdb.gimp_layer_set_offsets(dayDs, 376 + 65, offy2[5])
                Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)

```

Finalmente, se exportan las imagenes en formato png y se borra la imagen en gimp para ahorrar memoria
```
        pdb.file_png_save(image, Vlayer, carpeta + 'Pared/fechas/'+ str(m+1) + '.png',  str(m+1) + '.png', 0, 0, 0, 1, 0,0,0)
        pdb.gimp_image_delete(image)
```

posteriormente, se repite el codigo anterior dos veces para generar dos paginas mas, la primera que contiene el ultimo mes del año anterior y la ultima que contiene el primer mes del siguiente año. (se omiten esas lineas de codigo en este leeme).

El resultado es una imagen que se ve asi:

