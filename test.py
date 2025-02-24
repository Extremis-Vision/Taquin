taille  = 3

def position_chiffre_x( nombre_traiter):
        if nombre_traiter != 0:
            x_position = nombre_traiter % (taille)
            if x_position == 0:
                return  2
            else:
                return x_position - 1
        else:
            return taille - 1

def position_chiffre_y(nombre_traiter):
        if nombre_traiter != 0: 
            y_position = nombre_traiter // taille
            return y_position
        else: 
            return taille - 1
        
for nombre in range ((taille**2)):
    print("nombre :",nombre,"x : ", position_chiffre_x(nombre),", y : ", position_chiffre_y(nombre))