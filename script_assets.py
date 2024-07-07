import os, glob, sys, time, calendar
from gimpfu import *

carpeta = 'carpeta'
feriados = [[1,1],[2,5],[3,18],[5,1],[9,16],[11,18],[12,25]]

def calendario_P(yyyy):
    yy = yyyy
    azul = gimpcolor.RGB(31,63,156)
    rojo = gimpcolor.RGB(255,0,0)
    verde = gimpcolor.RGB(67, 171, 59)
    gris = gimpcolor.RGB(233,233,233)
    gris2 = gimpcolor.RGB(101, 98, 99)
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
    for m in range(1,13):
        image = pdb.gimp_image_new(5000, 3000, 0)
        ycount = 0
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
            #Poniendo numeros normales
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
                    pdb.gimp_layer_set_offsets(weekN, 376, offy2[ycount])
                Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)              
        #Poniendo numeros grises finales        
        if ycount < 5:
            gimp.set_foreground(gris2)
            weekN =  pdb.gimp_text_fontname(image, None, 0, 0, str(wcount+1), 1, True, tama2, PIXELS, "Myriad Pro Bold")
            pdb.gimp_layer_set_offsets(weekN, 376, offy2[ycount+1])
            gimp.set_foreground(gris)
            offX  = offX2   
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
        pdb.file_png_save(image, Vlayer, carpeta + 'Pared/fechas/'+ str(m+1) + '.png',  str(m+1) + '.png', 0, 0, 0, 1, 0,0,0)
        pdb.gimp_image_delete(image)


#Primera pagina
    image = pdb.gimp_image_new(5000, 3000, 0)
    ycount = 0
    m=12
    yy = yyyy-1
    wcount = 47
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
        #Poniendo numeros normales
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
                pdb.gimp_layer_set_offsets(weekN, 376, offy2[ycount])
            Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)              
    #Poniendo numeros grises finales        
    if ycount < 5:
        gimp.set_foreground(gris2)
        weekN =  pdb.gimp_text_fontname(image, None, 0, 0, str(wcount+1), 1, True, tama2, PIXELS, "Myriad Pro Bold")
        pdb.gimp_layer_set_offsets(weekN, 376, offy2[ycount+1])
        gimp.set_foreground(gris)
        offX  = offX2   
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
    pdb.file_png_save(image, Vlayer, carpeta + 'Pared/fechas/'+ str(1) + '.png',  str(1) + '.png', 0, 0, 0, 1, 0,0,0)
    pdb.gimp_image_delete(image)


#Ultima pagina
    image = pdb.gimp_image_new(5000, 3000, 0)
    ycount = 0
    m=1
    yy = yyyy+1
    wcount = 0
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
        #Poniendo numeros normales
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
                pdb.gimp_layer_set_offsets(weekN, 376, offy2[ycount])
            Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)              
    #Poniendo numeros grises finales        
    if ycount < 5:
        gimp.set_foreground(gris2)
        weekN =  pdb.gimp_text_fontname(image, None, 0, 0, str(wcount+1), 1, True, tama2, PIXELS, "Myriad Pro Bold")
        pdb.gimp_layer_set_offsets(weekN, 376, offy2[ycount+1])
        gimp.set_foreground(gris)
        offX  = offX2   
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
    pdb.file_png_save(image, Vlayer, carpeta + 'Pared/fechas/'+ str(14) + '.png',  str(14) + '.png', 0, 0, 0, 1, 0,0,0)
    pdb.gimp_image_delete(image)



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
    for m in range(1,13):
        image = pdb.gimp_image_new(1529, 1296, 0)
        gimp.set_foreground(gimpcolor.RGB(255,255,255))
        lsize = pdb.gimp_text_fontname(image, None, 0, 0, '.', 1, True, 1, PIXELS, "Myriad Pro Bold")
        pdb.gimp_layer_set_offsets(lsize, 0, 0)
        Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)
        ycount = 0
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
            #Poniendo numeros normales
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
        #Poniendo numeros grises finales        

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
           
        pdb.file_png_save(image, Vlayer, carpeta + 'Escritorio/fechas/'+ str(m) + '.png',  str(m+1) + '.png', 0, 0, 0, 1, 0,0,0)
        pdb.gimp_image_delete(image)


#Primera imagen
    m = 12
    yy = yyyy-1
    ycount = 0
    wcount = 47
    image = pdb.gimp_image_new(1529, 1296, 0)
    gimp.set_foreground(gimpcolor.RGB(255,255,255))
    lsize = pdb.gimp_text_fontname(image, None, 0, 0, '.', 1, True, 1, PIXELS, "Myriad Pro Bold")
    pdb.gimp_layer_set_offsets(lsize, 0, 0)
    Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)
    ycount = 0
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
        #Poniendo numeros normales
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
    #Poniendo numeros grises finales        

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
        
    pdb.file_png_save(image, Vlayer, carpeta + 'Escritorio/fechas/'+ str(0) + '.png',  str(m+1) + '.png', 0, 0, 0, 1, 0,0,0)
    pdb.gimp_image_delete(image)


#ultima imagen
    m = 1
    yy = yyyy+1
    ycount = 0
    wcount = 0
    image = pdb.gimp_image_new(1529, 1296, 0)
    gimp.set_foreground(gimpcolor.RGB(255,255,255))
    lsize = pdb.gimp_text_fontname(image, None, 0, 0, '.', 1, True, 1, PIXELS, "Myriad Pro Bold")
    pdb.gimp_layer_set_offsets(lsize, 0, 0)
    Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)
    ycount = 0
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
        #Poniendo numeros normales
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
    #Poniendo numeros grises finales        

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
        
    pdb.file_png_save(image, Vlayer, carpeta + 'Escritorio/fechas/'+ str(13) + '.png',  str(m+1) + '.png', 0, 0, 0, 1, 0,0,0)
    pdb.gimp_image_delete(image)




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
    #Cambiar anios
    if mes == 1:
        anio1 = yyyy-1
        anio2 = yyyy
    elif mes == 12:
        anio1 = yyyy
        anio2 = yyyy+1
    else:
        anio1 = yyyy
        anio2 = yyyy
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
    #Cambiar header
    layer_header_2 = pdb.gimp_file_load_layer(image, carpeta + 'common/header.png')
    pdb.gimp_image_insert_layer(image, layer_header_2, None , 9)
    pdb.gimp_item_set_name(layer_header_2, 'Header')
    pdb.gimp_layer_scale(layer_header_2, 755, 245, 0)
    pdb.gimp_layer_set_offsets(layer_header_2, 1007, 540)
    #Cambiar fechas
    layer_dates1_2 = pdb.gimp_file_load_layer(image, carpeta + 'Escritorio/fechas/' + str(mes-1) +'.png')
    layer_dates2_2 = pdb.gimp_file_load_layer(image, carpeta + 'Escritorio/fechas/' + str(mes) +'.png')
    layer_dates3_2 = pdb.gimp_file_load_layer(image, carpeta + 'Escritorio/fechas/' + str(mes+1) +'.png')
    pdb.gimp_image_insert_layer(image, layer_dates1_2, None , 20)
    pdb.gimp_image_insert_layer(image, layer_dates2_2, None , 20)
    pdb.gimp_image_insert_layer(image, layer_dates3_2, None , 20)
    pdb.gimp_item_set_name(layer_dates1_2, 'Dates1')
    pdb.gimp_item_set_name(layer_dates2_2, 'Dates2')
    pdb.gimp_item_set_name(layer_dates3_2, 'Dates3')
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
    pdb.gimp_layer_set_offsets(layer_dates1_2, 240, 760)
    pdb.gimp_layer_set_offsets(layer_dates2_2, 1020, 770)
    pdb.gimp_layer_set_offsets(layer_dates3_2, 1805, 760)   
    #Guardar
    pdb.gimp_xcf_save(1, image, layer_header_2, carpeta + 'Escritorio/' + str(mes) + '.xcf', str(mes) + '.xcf')
    Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)
    pdb.file_png_save(image, Vlayer, carpeta + 'Escritorio/' + str(mes) + '.png', str(mes) + '.png', 0, 0, 0, 1, 0, 0, 0)
    pdb.gimp_image_delete(image)


def escritorio_full():
    image = pdb.gimp_file_load(carpeta + 'Escritorio/anual.xcf', 'anual.xcf')
    for n in range(1,13):
        layerm = pdb.gimp_image_get_layer_by_name(image, str(n)+'.png')
        pdb.gimp_image_remove_layer(image, layerm)
        layer_replace = pdb.gimp_file_load_layer(image, carpeta + 'Pared/' + str(n+1) +'.png')
        pdb.gimp_image_insert_layer(image, layer_replace, None , 0)
        pdb.gimp_item_set_name(layer_replace, str(n)+'.png')
        pdb.gimp_layer_scale(layer_replace, 611, 371, 0)
        if n == 1:
            pdb.gimp_layer_set_offsets(layer_replace, 181, 282)
        elif n== 2:
            pdb.gimp_layer_set_offsets(layer_replace, 771, 282)
        elif n== 3:
            pdb.gimp_layer_set_offsets(layer_replace, 1377, 282)
        elif n== 4:
            pdb.gimp_layer_set_offsets(layer_replace, 1975, 282)
        elif n== 5:
            pdb.gimp_layer_set_offsets(layer_replace, 181, 666)
        elif n== 6:
            pdb.gimp_layer_set_offsets(layer_replace, 771, 666)
        elif n== 7:
            pdb.gimp_layer_set_offsets(layer_replace, 1377, 666)
        elif n== 8:
            pdb.gimp_layer_set_offsets(layer_replace, 1975, 666)
        elif n== 9:
            pdb.gimp_layer_set_offsets(layer_replace, 181, 1038)
        elif n== 10:
            pdb.gimp_layer_set_offsets(layer_replace, 771, 1038)
        elif n== 11:
            pdb.gimp_layer_set_offsets(layer_replace, 1377, 1038)
        else:
            pdb.gimp_layer_set_offsets(layer_replace, 1975, 1038)
    pdb.gimp_xcf_save(1, image, layer_replace, carpeta +'Escritorio/anual.xcf', 'anual.xcf')
    Vlayer = pdb.gimp_image_merge_visible_layers(image, 1)
    pdb.file_png_save(image, Vlayer, carpeta + 'Escritorio/anual.png', 'anual.png', 0, 0, 0, 1, 0, 0, 0)
    pdb.gimp_image_delete(image)
                                                        




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

def pared_all(yyyy):
    for n in range(2,14):
        archivo_n = str(n)
        cambio_pared(archivo_n, yyyy, n-1)
    cambio_pared('1', yyyy-1, 12)
    cambio_pared('14', yyyy+1, 1)

def escritorio_all(yyyy):
    for n in range(1,13):
        cambio_escritorio(yyyy,n)
