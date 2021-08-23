import pandas as pd
import seaborn as sns

lista = ["cba_marzo2019","cba_abril2019","cba_may2019","cba_jun2019","cba_jul2019",
         "cba_ago2019","cba_sep2019","cba_oct2019","cba_nov2019","cba_dic2019","cba_feb2020"
         ,"cba_mar2020","cba_junio2020","cba_julio2020","cba_agosto2020","cba_sept2020"]
meses = ["03/01/2019","04/01/2019","05/01/2019","06/01/2019","07/01/2019",
         "08/01/2019","09/01/2019","10/01/2019","11/01/2019","12/01/2019","02/01/2020",
         "03/01/2020","06/01/2020","07/01/2020","08/01/2020","09/01/2020"]
# Importar csv 
for i in range(len(lista)):
    df= pd.read_csv(r'.\Datos CBA Original\\'+lista[i]+'.csv',
                    sep=',',
                    encoding ='mac_roman')
    
    # Asignar nombre de columnas
    df.loc[1,'Unnamed: 0'] = 'Producto' 
    df.loc[1,'Unnamed: 1'] = 'Unidad'
    # Tomar nombres de la fila con índice 1
    df.columns = df.iloc[1]
    
    # Tomar solo las filas con valores relevantes
    df=df[2:61]
    
    # Calcular promedio de solo columnas numéricas
    df2 = df.drop(df.columns[[0, 1]], axis=1)
    df2 = df2.apply(pd.to_numeric)
    df2['avg'] = df2.mean(axis=1)
    promedios = df2['avg']
    
    # Unir promedio a df original
    df = df.join(promedios)
    df=df.apply(pd.to_numeric, errors='ignore')
    
    # Rellenar valores vacíos con precio promedio
    df=df.where(df.notnull(), df.avg, axis=0)
    df = df.drop(df.columns[[-1]], axis=1)
    
    # Transformar matriz en tabla relacional
    df = df.set_index(['Producto','Unidad']).stack().reset_index(name='Precio').rename(columns={'level_3':'Supermercado'})
    
    # # Solución para transformar matriz
    # df = pd.melt(df,id_vars=['Producto','Unidad'],var_name ='Supermercado').sort_values(['Producto','Unidad','Supermercado'])
    
    # Asignar nombres finales de las columnas
    df.columns = ['Producto', 'Unidad', 'Supermercado', 'Precio']
    
    # Asignar productos al grupo de carnes
    df.loc[((df.Producto.str.contains('Babilla',na=False))|
                                (df.Producto.str.contains("Bistec de Cinta",na=False))|
                                (df.Producto.str.contains("Carne Molida de Primera",na=False))|
                                (df.Producto.str.contains("Costilla",na=False))|
                                (df.Producto.str.contains("Puerco Liso",na=False))|
                                (df.Producto.str.contains("Pulpa Negra",na=False))|
                                (df.Producto.str.contains("Muslo de Pollo con Piel",na=False))|
                                (df.Producto.str.contains("Pechuga de Pollo con Piel",na=False))|
                                (df.Producto.str.contains("Pollo Entero s/plumas",na=False))|
                                (df.Producto.str.contains("Pescado Corvina",na=False))|
                                (df.Producto.str.contains("Pescado Corvina",na=False))|
                                (df.Producto.str.contains("Pescado Corvina",na=False))|
                                (df.Producto.str.contains("Sardina en Salsa de Tomate sin Picante",na=False))|
                                (df.Producto.str.contains("Tuna en Agua",na=False))|
                                (df.Producto.str.contains("Jam¢n Cocido Empacado 4x4",na=False))|
                                (df.Producto.str.contains("Cocido Empacado",na=False))|
                                (df.Producto.str.contains("Mortadela",na=False))|
                                (df.Producto.str.contains("Salchichas Nac Empacadas tipo frankfurter",na=False))), 'Grupo'] = "Carnes"
    
    # Asignar productos al grupo de cereales
    df.loc[((df.Producto.str.contains('Arroz',na=False))|                 
                                (df.Producto.str.contains("Codito",na=False))|
                                (df.Producto.str.contains("Crema",na=False))|
                                (df.Producto.str.contains("Hojuelas",na=False))|
                                (df.Producto.str.contains("Macarrones",na=False))|
                                (df.Producto.str.contains("Michita",na=False))|
                                (df.Producto.str.contains("Molde",na=False))|
                                (df.Producto.str.contains("Tortilla",na=False))), 'Grupo'] = "Cereales"
    
    # Asignar productos al grupo de vegetales y verduras
    df.loc[((df.Producto.str.contains('Aj° Dulce',na=False))|                           
                                (df.Producto.str.contains("Cebolla",na=False))|
                                (df.Producto.str.contains("picoloro",na=False))|
                                (df.Producto.str.contains("Lechuga",na=False))|
                                (df.Producto.str.contains("•ame",na=False))|
                                (df.Producto.str.contains("ame Diamante",na=False))|
                                (df.Producto.str.contains("Papa",na=False))|
                                (df.Producto.str.contains("Pl†tano",na=False))|
                                (df.Producto.str.contains("tano Verde",na=False))|
                                (df.Producto.str.contains("Repollo",na=False))|
                                (df.Producto.str.contains("Tomate Nacional",na=False))|
                                (df.Producto.str.contains("Yuca",na=False))|
                                (df.Producto.str.contains("Zanahoria",na=False))|
                                (df.Producto.str.contains("Ajo",na=False))), 'Grupo'] = "Vegetales y Verduras"
    
    
    # Asignar productos al grupo de leguminosas
    df.loc[((df.Producto.str.contains('Frijoles Chiricanos',na=False))|               
                                (df.Producto.str.contains("Lentejas",na=False))|
                                (df.Producto.str.contains("Porotos",na=False))), 'Grupo'] = "Leguminosas/Menestra"
    
    
    # Asignar productos al grupo de frutas
    df.loc[((df.Producto.str.contains('Guineos',na=False))|                               
                                (df.Producto.str.contains("Manzana",na=False))|
                                (df.Producto.str.contains("Naranja de",na=False))|
                                (df.Producto.str.contains("PiÒa",na=False))|
                                (df.Producto.str.contains("Pi§a",na=False))), 'Grupo'] = "Frutas"
    
    # Asignar productos al grupo de grasas
    df.loc[((df.Producto.str.contains('Aceite',na=False))|
                                (df.Producto.str.contains("Margarina",na=False))), 'Grupo'] = "Grasas"
    
    # Asignar productos al grupo de lacteos
    df.loc[((df.Producto.str.contains('Leche',na=False))|                    
                                (df.Producto.str.contains("Queso",na=False))), 'Grupo'] = "Lacteos"
    
    # Asignar productos al grupo de otros
    df.loc[((df.Producto.str.contains('Huevos',na=False))|
                                (df.Producto.str.contains("Az£car",na=False))|
                                (df.Producto.str.contains("car Morena",na=False))|
                                (df.Producto.str.contains("CafÇ",na=False))|
                                (df.Producto.str.contains("Molido Tradicional",na=False))|
                                (df.Producto.str.contains("Jugo de",na=False))|
                                (df.Producto.str.contains("Mayonesa",na=False))|
                                (df.Producto.str.contains("Pasta de",na=False))|
                                (df.Producto.str.contains("Sal ",na=False))|
                                (df.Producto == 'Sal  ')|
                                (df.Producto.str.contains("Salsa de Tomate",na=False))|
                                (df.Producto.str.contains("Soda",na=False))|
                                (df.Producto.str.contains("Sopa Deshidratada",na=False))|
                                (df.Producto.str.contains("Te Negro",na=False))), 'Grupo'] = "Otros"
    
    # Asignar los supermercados de Betania
    df.loc[((df.Supermercado == "SUPER 99 EL DORADO") |
                  (df.Supermercado == "SUPER 99 CAMINO REAL") |
                  (df.Supermercado == "SUPER 99 TUMBA MUERTO") |
                  (df.Supermercado =="REY EL DORADO")|
                  (df.Supermercado == "XTRA TUMBA MUERTO")), "Area"] = "Betania"
    
    # Asignar los supermercados de Santa Ana y Calidonia
    df.loc[((df.Supermercado == "EL MACHETAZO SANTA ANA") |
                  (df.Supermercado == "EL MACHETAZO CALIDONIA") |
                  (df.Supermercado == "REY BOMBERO SANTA ANA") |
                  (df.Supermercado == "SUPER 99 LA CUCHILLA CALIDONIA")), "Area"] = "Santa Ana y Calidonia"
    
    # Asignar los supermercados de Bella Vista
    df.loc[((df.Supermercado == "CASA DE LA CARNE CANGREJO") |
                  (df.Supermercado == "REY DE VIA ESPA•A") |
                  (df.Supermercado == "REY DE VIA ESPA—A") |
                  (df.Supermercado == "RIBA SMITH BELLA VISTA") |
                  (df.Supermercado == "RIBA SMITH TRANSISTMICA")), "Area"] = "Bella Vista"
    
    # Asignar los supermercados de Juan Diaz
    df.loc[((df.Supermercado == "EL MACHETAZO COSTA SUR") |
                  (df.Supermercado == "EL MACHETAZO METRO MALL") |
                  (df.Supermercado == "SUPER 99 LOS PUEBLOS") |
                  (df.Supermercado == "SUPER 99 PEDREGAL") |
                  (df.Supermercado == "SUPER 99 PLAZA TOCUMEN") |
                  (df.Supermercado == "XTRA LAS ACACIAS") |
                  (df.Supermercado == "XTRA LOS PUEBLOS")), "Area"] = "Juan Diaz"
    
    # Asignar los supermercados de Parque Lefevre
    df.loc[((df.Supermercado == "REY CHANIS") |
                  (df.Supermercado == "SUPER 99 CHANIS") |
                  (df.Supermercado == "SUPER 99 PORTOBELO")), "Area"] = "Parque Lefevre"
    
    # Asignar los supermercados de Pueblo Nuevo
    df.loc[((df.Supermercado == "REY 12 DE OCTUBRE") |
                  (df.Supermercado == "SUPER 99 VISTA HERMOSA")), "Area"] = "Pueblo Nuevo"
    
    # Asignar los supermercados de San Francisco
    df.loc[((df.Supermercado == "CASA DE LA CARNE VIA PORRAS") |           
                  (df.Supermercado == "REY CALLE 50") |
                  (df.Supermercado == "SUPER 99 SAN FRANCISCO") |
                  (df.Supermercado == "SUPER 99 VÕA PORRAS") |
                  (df.Supermercado == "SUPER 99 V÷A PORRAS")), "Area"] = "San Francisco"
    
    # Asignar los supermercados de San Miguelito
    df.loc[((df.Supermercado == "EL FUERTE SAN MIGUELITO") |
                  (df.Supermercado == "EL MACHETAZO SAN MIGUELITO") |
                  (df.Supermercado == "REY BRISAS DEL GOLF") |
                  (df.Supermercado == "REY VILLA LUCRE") |
                  (df.Supermercado == "SUPER 99 BRISAS DEL GOLF") |
                  (df.Supermercado == "SUPER 99 LOS ANDES") |
                  (df.Supermercado == "SUPER 99 VILLA LUCRE") |
                  (df.Supermercado == "XTRA MARKET  VILLA LUCRE") |
                  (df.Supermercado == "XTRA OJO DE AGUA") |
                  (df.Supermercado == "XTRA PAN DE AZ⁄CAR") |                  
                  (df.Supermercado == "XTRA PAN DE AZÈCAR")), "Area"] = "San Miguelito"
    
    # Asignar los supermercados de Panama Este
    df.loc[((df.Supermercado == "EL MACHETAZO NVO. TOCUMEN") |
                  (df.Supermercado == "EL MACHETAZO PUNTA DEL ESTE") |
                  (df.Supermercado == "REY LAS AMERICAS") |
                  (df.Supermercado == "SUPER 99 24 DE DICIEMBRE") |
                  (df.Supermercado == "SUPER 99 MA•ANITAS") |                  
                  (df.Supermercado == "SUPER 99 MA—ANITAS") |
                  (df.Supermercado == "SUPER 99 MEGA MALL") |
                  (df.Supermercado == "XTRA  24 DICIEMBRE") |
                  (df.Supermercado == "XTRA CHEPO") |
                  (df.Supermercado =="EL FUERTE VILLA ZAITA")|
                  (df.Supermercado =="REY MILLA 8")|
                  (df.Supermercado =="SUPER 99 LA CABIMA")|
                  (df.Supermercado == "XTRA PACORA")), "Area"] = "Panama Este"
    
    # Asignar cadenas de Supermercado
    df.loc[df['Supermercado'].str.contains("REY",na=False), "Cadena"] = "Rey"
    df.loc[df['Supermercado'].str.contains("SUPER 99",na=False), "Cadena"] = "Super 99"
    df.loc[df['Supermercado'].str.contains("XTRA",na=False), "Cadena"] = "Xtra"
    df.loc[df['Supermercado'].str.contains("MACHETAZO",na=False), "Cadena"] = "Machetazo"
    df.loc[df['Supermercado'].str.contains("EL FUERTE",na=False), "Cadena"] = "El Fuerte"
    df.loc[df['Supermercado'].str.contains("CASA DE LA CARNE",na=False), "Cadena"] = "Casa de la Carne"
    df.loc[df['Supermercado'].str.contains("RIBA",na=False), "Cadena"] = "Riba Smith"
    
    df = df.loc[df['Cadena'].notnull()]
    df['Mes']=meses[i]
    if i==0:    
        df3=df
    elif i>=1:
        df3=df3.append(df)

df_pivot = df3.groupby(['Supermercado','Mes','Cadena']).sum().reset_index()
df_pivot2 = df3.groupby(['Supermercado','Mes','Area']).sum().reset_index()
df_cadena = df_pivot[['Cadena','Precio']]
df_mes = df_pivot[['Mes','Precio']]
df_area = df_pivot2[['Area','Precio']]
g = sns.catplot(x="Cadena", y="Precio", kind="box", data=df_cadena)
g.set_xticklabels(rotation=90)
g2 = sns.catplot(x="Mes", y="Precio", kind="box", data=df_mes)
g2.set_xticklabels(rotation=90)
g3 = sns.catplot(x="Area", y="Precio", kind="box", data=df_area)
g3.set_xticklabels(rotation=90)
df3.to_excel(r'.\Datos CBA Procesados\output.xlsx')  