# calendario_gimp
Creacion de calendario usando python y gimp


Hace tiempo me pidieron hacer un calendario para una compañía, estos calendarios se imprimen cada año y la compañía se los regala a sus socios. En lugar de usar un programa ya hecho para hacer calendarios como miscrosoft publisher o algo parecido, decidí hacer mi propio script utilizando Gimp y su implementacion de python-fu para automatizar el proceso. Python-fu solo puede usarse dentro de Gimp, asi que es necesario primero brir Gimp y despues ejecutar el script. para esto, escribí un script en bash que se encarga de ejecutar Gimp, correr python-fu y cerrarlo.

## Concepto

La idea del script es que genere cada una de las paginas de dos tipos de calendario, uno de escritorio y uno de pared. EN el script solo es necesario indicar el año del calendario y las fechas de los dias feriados, para que se marquen en otro color. El estilo del calendario, incluyendo los colores, las fuentes e imagenes utilizadas están predefinidas, aunque algunas cosas se van a editar en el mismo script. Las paginas generadas deben ser de alta calidad para que se vean bien en una impresion, por lo tanto, se generarán archivos pdf listos apra impresion de cada pagina.

## Codigo

### calendario_P

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

El resultado es una imagen que se ve asi para el mes de septiembre de 2024:

![example_10](https://github.com/cesarchocobo/calendario_gimp/assets/101080325/fdbfbe1c-2b0a-4dcf-9c5d-a9a0b08b0ece)


### Calendario_E

Se hace un codigo similar para el calendario de escritotio. La diferenia esta en el formato, incluyendo el tamaño y la organizacion del calendario. En este caso se pueden tener 5 filas de fechas, asi que no es necesario poner fechas en doble fila. De igual manera que con el calendario de apred, se comienza definiendo los tamaños y posiciones que tendran las fechas.

```
def calendario_E(yyyy):
    yy = yyyy
    azul = gimpcolor.RGB(31,63,156)
    rojo = gimpcolor.RGB(255,0,0)
    verde = gimpcolor.RGB(67, 171, 59)
    gris = gimpcolor.RGB(233,233,233)
    gris2 = gimpcolor.RGB(101, 98, 99)
    obj = calendar.Calendar(0)
    Px = [247, 436, 628, 817, 1008, 1197, 1388]
    Ct = 247-210
    offX1 = [Px[0]-Ct, Px[1]-Ct, Px[2]-Ct, Px[3]-Ct, Px[4]-Ct, Px[5]-Ct, Px[6]-Ct] 
    offX2 = [Px[0], Px[1], Px[2], Px[3], Px[4], Px[5], Px[6]] 
    offX = offX1
    offy = [41, 257, 471, 687, 902, 1116]
    offy2 = [0, 68, 283, 498, 712, 928, 1143]
    wcount = 0 
    tama1 = 133
    tama2 = 80
```
Despues se itera sobre los 12 meses del año. Dependiendo de cuantas semanas tenga el mes, el tamaño de los archivos será distinto, Para que todos tengan el mismo tamaño independientemente de la cantidad de semanas en el mes, se pone un punto en la esquina del archivo. este pinto es color blanco y en la impresion no se verá.

```
for m in range(1,13):
        image = pdb.gimp_image_new(1529, 1296, 0)
        gimp.set_foreground(gimpcolor.RGB(255,255,255))
        lsize = pdb.gimp_text_fontname(image, None, 0, 0, '.', 1, True, 1, PIXELS, "Myriad Pro Bold")
        pdb.gimp_layer_set_offsets(lsize, 0, 0)
        Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)
        ycount = 0
```
Despues se ponen los numeros grises (los que no pertenecen al mes en cuestion) siguiendo un codigo similar al caso del calendario de pared

```
        for n in obj.itermonthdays(yy, m):
            #Poniendo numeros grises
            if n == 0:
                gimp.set_foreground(gris)
                offX = offX1 
                if m == 1:
                    for i in range(calendar.weekday(yy, m, 1)):
                        j = calendar.monthrange(yy-1, 12)[1]-calendar.weekday(yy, m, 1)+i +1
                        dayB = pdb.gimp_text_fontname(image, None, 0, 0, str(j), 1, True, tama1, PIXELS, "Myriad Pro Bold")
                        pdb.gimp_layer_set_offsets(dayB, offX[calendar.weekday(yy-1, 12, j)], offy[0])
                        Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)
                else:
                     for i in range(calendar.weekday(yy, m, 1)):
                        j = calendar.monthrange(yy, m-1)[1]-calendar.weekday(yy, m, 1)+ i +1
                        dayB = pdb.gimp_text_fontname(image, None, 0, 0, str(j), 1, True, tama1, PIXELS, "Myriad Pro Bold")
                        pdb.gimp_layer_set_offsets(dayB, offX[calendar.weekday(yy, m-1, j)], offy[0])                   
                        Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)
```

Se ponen los numeros del mes, usando de nuevo un codigo similar al caso de pared

```
            else:
                #Centrando numeros
                if n < 10:
                    offX = offX2
                else:
                    offX = offX1 
                #Poniendo el color del domingo o entres emana
                if [m,n] in feriados:
                    gimp.set_foreground(verde)
                elif calendar.weekday(yy, m, n) == 6:
                    gimp.set_foreground(rojo)
                else:
                    gimp.set_foreground(azul)
                #Poniendo los numeros    
                dayT = pdb.gimp_text_fontname(image, None, 0, 0, str(n), 1, True, tama1, PIXELS, "Myriad Pro Bold")
                pdb.gimp_layer_set_offsets(dayT, offX[calendar.weekday(yy, m, n)], offy[ycount])
                #cambiando y poniendo el numero de semana
                if calendar.weekday(yy, m, n) == 6:
                    ycount = ycount + 1
                    wcount = wcount + 1
                    gimp.set_foreground(gris2)
                    weekN =  pdb.gimp_text_fontname(image, None, 0, 0, str(wcount), 1, True, tama2, PIXELS, "Myriad Pro Bold")
                    pdb.gimp_layer_set_offsets(weekN, 51, offy2[ycount])
                Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)
```

Se ponen los numeros de la ultima semana que no pertenecen al mes

```
        gimp.set_foreground(gris2)
        weekN =  pdb.gimp_text_fontname(image, None, 0, 0, str(wcount+1), 1, True, tama2, PIXELS, "Myriad Pro Bold")
        pdb.gimp_layer_set_offsets(weekN, 51, offy2[ycount+1])
        gimp.set_foreground(gris)
        offX  = offX2   
        if m == 12:
            for l in range(6-calendar.weekday(yy, m, calendar.monthrange(yy, m)[1])):
                dayA = pdb.gimp_text_fontname(image, None, 0, 0, str(l+1), 1, True, tama1, PIXELS, "Myriad Pro Bold")
                pdb.gimp_layer_set_offsets(dayA, offX[calendar.weekday(yy+1, 1, l+1)], offy[ycount])
                Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)
        else:
            for l in range(6-calendar.weekday(yy, m, calendar.monthrange(yy, m)[1])):
                dayA = pdb.gimp_text_fontname(image, None, 0, 0, str(l+1), 1, True, tama1, PIXELS, "Myriad Pro Bold")
                pdb.gimp_layer_set_offsets(dayA, offX[calendar.weekday(yy, m+1, l+1)], offy[ycount])
                Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)    
```

Finalmente se exporta el archivo en formato .png y se borra la imagen de gimp para ahorrar memoria.

```
        pdb.file_png_save(image, Vlayer, carpeta + 'Escritorio/fechas/'+ str(m) + '.png',  str(m+1) + '.png', 0, 0, 0, 1, 0,0,0)
        pdb.gimp_image_delete(image)
```

De igual forma que con el caso de pared, este codigo se repite para la primera pagina, que será el ultimo mes del año anterior y para la ultima pagina que será el primer mes del año siguiente. El resultado se ve asi:

![example_10](https://github.com/cesarchocobo/calendario_gimp/assets/101080325/14bf9364-fda5-4664-85bb-5688f1d2f067)


### Estilos

Por cuestiones de estilo, los numeros que etiquetan el mes de la pagina van a tener un cierto formato. Para darle mayor personalizacion, estos numeros no seran solo un texto sino una imagen. Hay que generar todos los digitos que se usrana, para esto es la funcion numeros(estilo). donde "estilo" es un patron de colores de Gimp. Se generan numeros del 0 al 9, con un cierto tamaño de imagen y se guardan en la carpeta /mold.

```
def numeros(estilo):
    for n in range(10):
        archivo = 'g'+str(n)
        image = pdb.gimp_image_new(295, 424, 0)
        layer = pdb.gimp_file_load_layer(image, carpeta + 'mold/' + archivo + '.png')
        pdb.gimp_image_insert_layer(image, layer, None , 0)
        border = pdb.gimp_layer_new(image, 295, 424, 1, 'border', 100, 0)
        pdb.gimp_image_insert_layer(image, border, None , 0)
        number = pdb.gimp_layer_new(image, 295, 424, 1, 'number', 100, 0)
        pdb.gimp_image_insert_layer(image, number, None , 0)
        pdb.gimp_context_set_gradient(estilo)
        pdb.gimp_image_select_item(image, 0, layer)
        non_empty, x1, y1, x2, y2 = pdb.gimp_selection_bounds(image)
        pdb.gimp_drawable_edit_gradient_fill(border, 0, 0, False, 1, 0, TRUE, x2, 0, x1, 0)
        pdb.gimp_selection_shrink(image, 5)
        non_empty, x1, y1, x2, y2 = pdb.gimp_selection_bounds(image)
        pdb.gimp_drawable_edit_gradient_fill(number, 0, 0, False, 1, 0, TRUE, 0, y1, 0, y2)
        pdb.gimp_image_remove_layer(image, layer)
        pdb.gimp_selection_none(image)
        Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)
        pdb.file_png_save(image, Vlayer, carpeta + 'common/' + archivo + '.png', archivo + '.png', 0, 0, 0, 1, 0,0,0)
        pdb.gimp_image_delete(image)

```

El resultado, con un cierto estilo se ve asi:

![g8](https://github.com/cesarchocobo/calendario_gimp/assets/101080325/3a39a990-c950-4526-b4bf-8c571611802e)

Los archivos son imagenes en formato .png, todos nombrados "gn.png" donde la n representa el digito que tiene esa imagen. por ejemplo "g8.png".

Despues se crea otra funcion que genere las etiquetas de los meses usando los numeros ya generados con la funcion anterior. No es necesario correr la funcion numeros para tener los numeros, se pueden proveer de forma externa si se quiere más personalizacion. por eso lo puse en funciones distintas

```
def label_meses():
    for mes in range(1,13):
        if mes <= 9:
            mes_1 = 0
            mes_2 = mes
        else:
            mes_1 = 1
            mes_2 = mes-10
        image = pdb.gimp_image_new(595, 424, 0)
        primer = pdb.gimp_file_load_layer(image, carpeta + 'common/g' + str(mes_1) + '.png')
        segundo = pdb.gimp_file_load_layer(image, carpeta + 'common/g' + str(mes_2) + '.png')
        pdb.gimp_image_insert_layer(image, primer, None , 0)
        pdb.gimp_layer_set_offsets(primer, 0, 0)
        pdb.gimp_image_insert_layer(image, segundo, None , 0)
        pdb.gimp_layer_set_offsets(segundo, 300, 0)
        Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)
        pdb.file_png_save(image, Vlayer, carpeta + 'common/mes' + str(mes) + '.png', 'mes' + str(mes) + '.png', 0, 0, 0, 1, 0, 0, 0)
        pdb.gimp_image_delete(image)
```
El resultado es juntar digitos para formar la etiqueta del mes que se ve de esta forma:

![mes9](https://github.com/cesarchocobo/calendario_gimp/assets/101080325/9ebb71eb-43ce-47e5-a4d9-a51ee622f336)


Se hace lo mismo para las etiquetas de los años

```
def label_anios(yyyy):
    for an in range(yyyy-2020-1, yyyy-2020+2):
        image = pdb.gimp_image_new(1200, 427, 0)
        primer = pdb.gimp_file_load_layer(image, carpeta +'common/g2.png')
        segundo = pdb.gimp_file_load_layer(image, carpeta +'common/g0.png')
        tercero = pdb.gimp_file_load_layer(image, carpeta +'common/g2.png')
        cuarto = pdb.gimp_file_load_layer(image, carpeta + 'common/g' + str(an) + '.png')
        pdb.gimp_image_insert_layer(image, primer, None , 0)
        pdb.gimp_image_insert_layer(image, segundo, None , 0)
        pdb.gimp_image_insert_layer(image, tercero, None , 0)
        pdb.gimp_image_insert_layer(image, cuarto, None , 0)
        pdb.gimp_layer_set_offsets(primer, 0, 0)
        pdb.gimp_layer_set_offsets(segundo, 300, 0)
        pdb.gimp_layer_set_offsets(tercero, 600, 0)
        pdb.gimp_layer_set_offsets(cuarto, 900, 0)
        Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)
        pdb.file_png_save(image, Vlayer, carpeta + 'common/202' + str(an) + '.png', '202' + str(an) + '.png', 0, 0, 0, 1, 0, 0, 0)
        pdb.gimp_image_delete(image)
```

El resultado, de nuevo, es combinar digitos para formar la etiqueta del año que se vede esta forma:
![2024](https://github.com/cesarchocobo/calendario_gimp/assets/101080325/94b6a6e3-0472-483f-9c18-9933371590bb)

### Calendarios

Ya generamos los assets dinamicos que se necesitarán para crear el calendario, solo queda general las paginas con el formato y estilo definido. Para esto necesitamos crear dicho formato, como este puede cambiar y depende de los gustos de cada quien, no hicé un script, mas bien, se tienen que crear las imagenes con el estilo que se quiera siguiendo ciertas convenciones como el nombre de las capas y el nombre del archivo.

La función cambio_escritorio(yyyy, mes) se encarga de sustituri las fechas y las etiquetas de losa archivos de escritorio. Lo primero que se hace es cargar el archivo de gmp y obtener las capas de la imagen y se borran, ya que serán sustituidas por nuevas capas cque contengan la imagen apropiada para el nuevo calendario.

```
def cambio_escritorio(yyyy, mes):
    image = pdb.gimp_file_load(carpeta + 'Escritorio/' + str(mes) + '.xcf', str(mes) + '.xcf')
    layer_year1 = pdb.gimp_image_get_layer_by_name(image, 'Year1')
    layer_year2 = pdb.gimp_image_get_layer_by_name(image, 'Year2')
    layer_header = pdb.gimp_image_get_layer_by_name(image, 'Header')
    layer_dates1 = pdb.gimp_image_get_layer_by_name(image, 'Dates1')
    layer_dates2 = pdb.gimp_image_get_layer_by_name(image, 'Dates2')
    layer_dates3 = pdb.gimp_image_get_layer_by_name(image, 'Dates3')
    pdb.gimp_image_remove_layer(image, layer_header)
    pdb.gimp_image_remove_layer(image, layer_year1)
    pdb.gimp_image_remove_layer(image, layer_year2)
    pdb.gimp_image_remove_layer(image, layer_dates1)
    pdb.gimp_image_remove_layer(image, layer_dates2)
    pdb.gimp_image_remove_layer(image, layer_dates3)
```

Despues se crean variables para definir que meses se van a poner

```
    if mes == 1:
        anio1 = yyyy-1
        anio2 = yyyy
    elif mes == 12:
        anio1 = yyyy
        anio2 = yyyy+1
    else:
        anio1 = yyyy
        anio2 = yyyy
```

Se cambian las capas que contienen las etiquetas de los años

```
    layer_year1_2 = pdb.gimp_file_load_layer(image, carpeta + 'common/' + str(anio1) +'.png')
    layer_year2_2 = pdb.gimp_file_load_layer(image, carpeta +'common/' + str(anio2) +'.png')
    pdb.gimp_image_insert_layer(image, layer_year1_2, None , 0)
    pdb.gimp_image_insert_layer(image, layer_year2_2, None , 0)
    pdb.gimp_item_set_name(layer_year1_2, 'Year1')
    pdb.gimp_item_set_name(layer_year2_2, 'Year2')
    pdb.gimp_layer_scale(layer_year1_2, 493, 175, 0)
    pdb.gimp_layer_scale(layer_year2_2, 493, 175, 0)
    pdb.gimp_layer_set_offsets(layer_year1_2, 332, 327)
    pdb.gimp_layer_set_offsets(layer_year2_2, 1944, 327)
```
Despues, se cambia la imagen del encabezado de la pagina del calendario, esta imagen esta predefinida y ya guardada en la carpeta /common. Si se queire cambiar este encabezxdo solo basta cambiar esa imagen

```
    layer_header_2 = pdb.gimp_file_load_layer(image, carpeta + 'common/header.png')
    pdb.gimp_image_insert_layer(image, layer_header_2, None , 9)
    pdb.gimp_item_set_name(layer_header_2, 'Header')
    pdb.gimp_layer_scale(layer_header_2, 755, 245, 0)
    pdb.gimp_layer_set_offsets(layer_header_2, 1007, 540)
```

Despues se cargan las capas con las nuevas fechas
```
    layer_dates1_2 = pdb.gimp_file_load_layer(image, carpeta + 'Escritorio/fechas/' + str(mes-1) +'.png')
    layer_dates2_2 = pdb.gimp_file_load_layer(image, carpeta + 'Escritorio/fechas/' + str(mes) +'.png')
    layer_dates3_2 = pdb.gimp_file_load_layer(image, carpeta + 'Escritorio/fechas/' + str(mes+1) +'.png')
    pdb.gimp_image_insert_layer(image, layer_dates1_2, None , 20)
    pdb.gimp_image_insert_layer(image, layer_dates2_2, None , 20)
    pdb.gimp_image_insert_layer(image, layer_dates3_2, None , 20)
    pdb.gimp_item_set_name(layer_dates1_2, 'Dates1')
    pdb.gimp_item_set_name(layer_dates2_2, 'Dates2')
    pdb.gimp_item_set_name(layer_dates3_2, 'Dates3')
```

y se les cambia el tamaño para que quepan en el formato de pagina. se utilizan ifs para detectar cuando hayq ue cambiarles el tamaño

```
    if layer_dates1_2.height < 1200:
        pdb.gimp_layer_scale(layer_dates1_2, 714, 505, 0)
    else:
        pdb.gimp_layer_scale(layer_dates1_2, 714, 606, 0)
    if layer_dates2_2.height < 1200:
        pdb.gimp_layer_scale(layer_dates2_2, 714, 505, 0)
    else:
        pdb.gimp_layer_scale(layer_dates2_2, 714, 606, 0) 
    if layer_dates3_2.height < 1200:
        pdb.gimp_layer_scale(layer_dates3_2, 714, 505, 0)
    else:
        pdb.gimp_layer_scale(layer_dates3_2, 714, 606, 0)
```

Se colocan las capas con las fechas

```
    pdb.gimp_layer_set_offsets(layer_dates1_2, 240, 760)
    pdb.gimp_layer_set_offsets(layer_dates2_2, 1020, 770)
    pdb.gimp_layer_set_offsets(layer_dates3_2, 1805, 760)   
```


Finalmente se exporta el archivo
```
    pdb.gimp_xcf_save(1, image, layer_header_2, carpeta + 'Escritorio/' + str(mes) + '.xcf', str(mes) + '.xcf')
    Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)
    pdb.file_png_save(image, Vlayer, carpeta + 'Escritorio/' + str(mes) + '.png', str(mes) + '.png', 0, 0, 0, 1, 0, 0, 0)
    pdb.gimp_image_delete(image)
```

El resultado es algo como esto:
![10](https://github.com/cesarchocobo/calendario_gimp/assets/101080325/8e4853ad-8b03-4bfd-8804-cb01620be756)

En la parte de enmedio puede tener mas cosas, como el logo de la empresa.


Se hace algo aprecido para el calendario de pared, esto con la función cambio_pared

```
def cambio_pared(archivo, anio, mes):    
    image = pdb.gimp_file_load(carpeta + 'Pared/' + archivo + '.xcf', archivo)
    #quitar lo  que se va a cambiar
    layer_year = pdb.gimp_image_get_layer_by_name(image, 'Year')
    layer_header = pdb.gimp_image_get_layer_by_name(image, 'Header')
    layer_month = pdb.gimp_image_get_layer_by_name(image, 'Month')
    layer_dates = pdb.gimp_image_get_layer_by_name(image, 'Dates')
    pdb.gimp_image_remove_layer(image, layer_year)
    pdb.gimp_image_remove_layer(image, layer_header)
    pdb.gimp_image_remove_layer(image, layer_month)
    pdb.gimp_image_remove_layer(image, layer_dates)
    #cambiar anio
    layer_year_2 = pdb.gimp_file_load_layer(image, carpeta + 'common/' + str(anio) +'.png')
    pdb.gimp_image_insert_layer(image, layer_year_2, None , 0)
    pdb.gimp_item_set_name(layer_year_2, 'Year')
    pdb.gimp_layer_scale(layer_year_2, 603, 220, 0)
    pdb.gimp_layer_set_offsets(layer_year_2, 3254, 296)
    #cambiar header
    layer_header_2 = pdb.gimp_file_load_layer(image, carpeta + 'common/header.png')
    pdb.gimp_image_insert_layer(image, layer_header_2, None , 5)
    pdb.gimp_item_set_name(layer_header_2, 'Header')
    pdb.gimp_layer_scale(layer_header_2, 4087, 813, 0)
    pdb.gimp_layer_set_offsets(layer_header_2, 50, 52)
    #cambiar mes
    layer_month_2 = pdb.gimp_file_load_layer(image, carpeta + 'common/mes'+ str(mes) + '.png')
    pdb.gimp_image_insert_layer(image, layer_month_2, None , 0)
    pdb.gimp_item_set_name(layer_month_2, 'Month')
    pdb.gimp_layer_scale(layer_month_2, 305, 217, 0)
    pdb.gimp_layer_set_offsets(layer_month_2, 338, 294)
    #cambiar fechas
    layer_dates_2 = pdb.gimp_file_load_layer(image, carpeta + 'Pared/fechas/'+ archivo + '.png')
    pdb.gimp_image_insert_layer(image, layer_dates_2, None , 0)
    pdb.gimp_item_set_name(layer_dates_2, 'Dates')
    pdb.gimp_layer_set_offsets(layer_dates_2, 376, 806)
    #guardar
    pdb.gimp_xcf_save(1, image, layer_year_2, carpeta + 'Pared/' + archivo + '.xcf', archivo + '.xcf')
    Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)
    pdb.file_png_save(image, Vlayer, carpeta + 'Pared/' + archivo + '.png', archivo + '.png', 0, 0, 0, 1, 0, 0, 0)
    pdb.gimp_image_delete(image)
```

El resultado es algo como esto:

![example_10](https://github.com/cesarchocobo/calendario_gimp/assets/101080325/e8c188c8-ec95-42fc-949c-4ef4d6a3a663)

Finalmente se crean dos funciones más para correr un loop con las funciones anteriores y obtener todas las paginas de los calendarios

```
def pared_all(yyyy):
    for n in range(2,14):
        archivo_n = str(n)
        cambio_pared(archivo_n, yyyy, n-1)
    cambio_pared('1', yyyy-1, 12)
    cambio_pared('14', yyyy+1, 1)

def escritorio_all(yyyy):
    for n in range(1,13):
        cambio_escritorio(yyyy,n)

```

### bash

Con esto ya se tiene todo el calendario, pero falta automatizar el proceso, para esto, escribí un archivo en bash que ejecuta gimp y las funciones necesarias para generar el calendario. Este es ela rchivo gimp_bash.sh.

Comenzamos por definir el año y ejectutar gimp junto con los scripts para generas los estilos y las paginas de los calendarios. En este caso, mi instalacion de gimp es usando flatpak, ya que esta version de gimp cuenta con python-fu instalado. En este ejemplo utilicé el estilo "Gold Logistic" para generar las etiquetas, pero se puede usar cualquier otro degradado que se tenga guardado en gimp o crear uno perzonalizado.

```
yyyy=2024
flatpak run org.gimp.GIMP --batch-interpreter python-fu-eval -b "import sys; sys.path=['.']+sys.path; import script_assets; script_assets.calendario_P($yyyy)" -b "pdb.gimp_quit(1)"
flatpak run org.gimp.GIMP --batch-interpreter python-fu-eval -b "import sys; sys.path=['.']+sys.path; import script_assets; script_assets.calendario_E($yyyy)" -b "pdb.gimp_quit(1)"
flatpak run org.gimp.GIMP --batch-interpreter python-fu-eval -b "import sys; sys.path=['.']+sys.path; import script_assets; script_assets.numeros('Gold Logistic')" -b "pdb.gimp_quit(1)"
flatpak run org.gimp.GIMP -idf --batch-interpreter python-fu-eval -b "import sys; sys.path=['.']+sys.path; import script_assets; script_assets.label_meses()" -b "pdb.gimp_quit(1)"
flatpak run org.gimp.GIMP -idf --batch-interpreter python-fu-eval -b "import sys; sys.path=['.']+sys.path; import script_assets; script_assets.label_anios($yyyy)" -b "pdb.gimp_quit(1)"
flatpak run org.gimp.GIMP -idf --batch-interpreter python-fu-eval -b "import sys; sys.path=['.']+sys.path; import script_assets; script_assets.pared_all($yyyy)" -b "pdb.gimp_quit(1)"
flatpak run org.gimp.GIMP -idf --batch-interpreter python-fu-eval -b "import sys; sys.path=['.']+sys.path; import script_assets; script_assets.escritorio_all($yyyy)" -b "pdb.gimp_quit(1)"
flatpak run org.gimp.GIMP -idf --batch-interpreter python-fu-eval -b "import sys; sys.path=['.']+sys.path; import script_assets; script_assets.escritorio_full()" -b "pdb.gimp_quit(1)"
```

Despues se convierten todas las imagenes a formato.pdf, paa que queden listas para imprimirse

```
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
```

Aqui se añaden las portadas de los calendarios que tambien deben hacerse aparte y contienen los logotipos e imagenes de la compañia. Despues, se optimizan losa rchivos para darles un tamaño menor y que puedan enviarse por correo electronico. Notese que esto disminuye la calidad de los archivos.

```
cd carpeta/Escritorio/pdf
for i in *.pdf
do
  gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH -sOutputFile=op/$i $i
done
cd /home/cesar/Documents/Proyectos/Calendario_GL/Pared/pdf
for i in *.pdf
do
  gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH -sOutputFile=op/$i $i
done
```

Finalmente, se generan archivos de muestra con mucho menor calidad para poder enviarlos a la compañia para su revision y aprovacion antes de enviar los archivos con mayor calidad.

```
cd carpeta
convert Pared/portada.png -quality 50% -resize 700x700 muestra_portada_pared.png
convert Pared/1.png -quality 50% -resize 700x700 muestra_pared.png
convert Escritorio/portada.png -quality 50% -resize 700x700 muestra_portada_escritorio.png
convert Escritorio/1.png -quality 50% -resize 700x700 muestra_escritorio.png
```

## Funcionamiento

Basta ejecutar el archivo gimp_bash.sh para generar calendarios con el año especificado en ese archivo. Sin embargo, es importante contar con todos los archivos necesarios para ejecutar esto, como lo son las portadas, las imagenes que necesita el script como el encabezado de los calendarios y los moldes de las paginas de los calendarios.


