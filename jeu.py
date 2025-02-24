# Mini jeu taquin
# Import
import random
import keyboard
import heapq


# Structure du jeu  :
class Plateau:
    def __init__(self, taille):
        self.taille = taille
        self.creer_grie_solution()
        self.creer_grie_random()
        self.nombreCout = 0

        if self.plateau == self.creer_grie_solution():
            self.creer_grie_random()


    def creer_grie_solution(self):
        self.solution = []
        liste_solution_temp = []
        for nombre_liste_solution in range(1,self.taille**2):
            liste_solution_temp.append(nombre_liste_solution)

            if self.taille**2 - 1 == nombre_liste_solution:
                liste_solution_temp.append(0)

            if len(liste_solution_temp) == self.taille:
                self.solution.append(liste_solution_temp)
                liste_solution_temp = []
        
    
    def creer_grie_random(self):
        self.plateau = []
        liste_nombre_plateau = []
        for i in range(self.taille**2):
            liste_nombre_plateau.append(i)

        for _ in range(self.taille):
            liste_temp = []
            for _ in range(self.taille):
                nombre_aléatoire = random.choice(liste_nombre_plateau)
                liste_nombre_plateau.remove(nombre_aléatoire)
                liste_temp.append(nombre_aléatoire)
            self.plateau.append(liste_temp)

    def afficher(self):
        print("Nombre de Cout :", self.nombreCout)
        for x in range(self.taille):
            print("| ", end=" ")
            for y in range(self.taille):
                print(self.plateau[x][y]," |", end=" ")
            print("\n")

    def verifier_validiter_commande(self, commande):
        position_zero = []
        for x in range(self.taille):
            if 0 in self.plateau[x]:
                position_zero.append(x)
                for y in range(self.taille):
                    if 0 == self.plateau[x][y]:
                        position_zero.append(y)

        if commande == "s":
            if position_zero[0] == 0:
                return False
            
            else:
                self.plateau[position_zero[0]][position_zero[1]] = self.plateau[position_zero[0] - 1][position_zero[1]]
                self.plateau[position_zero[0] - 1][position_zero[1]] = 0
                self.nombreCout +=1

        if commande == "z":
            if position_zero[0] == 2:
                return False
            
            else:
                self.plateau[position_zero[0]][position_zero[1]] = self.plateau[position_zero[0] + 1][position_zero[1]]
                self.plateau[position_zero[0] + 1][position_zero[1]] = 0
                self.nombreCout +=1

        if commande == "d":
            if position_zero[1] == 0:
                return False
            
            else:
                self.plateau[position_zero[0]][position_zero[1]] = self.plateau[position_zero[0]][position_zero[1] - 1]
                self.plateau[position_zero[0]][position_zero[1] - 1] = 0
                self.nombreCout +=1

        if commande == "q":
            if position_zero[1] == 2:
                return False
            
            else:
                self.plateau[position_zero[0]][position_zero[1]] = self.plateau[position_zero[0]][position_zero[1] + 1]
                self.plateau[position_zero[0]][position_zero[1] + 1] = 0
                self.nombreCout +=1 

    def position_chiffre_x(self, nombre_traiter):
        x = nombre_traiter // self.taille
        return x

    def position_chiffre_y(self, nombre_traiter):
        y = nombre_traiter % self.taille
        return y

    def heuristique(self,plateau):
        distance = 0

        for x in range(self.taille):
            for y in range(self.taille):
                distance += abs(x - self.position_chiffre_x(plateau[x][y])) + abs (y - self.position_chiffre_y(plateau[x][y]))
        return distance
    
    def coord_zero(self):
        position_zero = []
        for x in range(self.taille):
            if 0 in self.plateau[x]:
                position_zero.append(x)
                for y in range(self.taille):
                    if 0 == self.plateau[x][y]:
                        position_zero.append(y)
                        return [x, y]
                        
    def teste_bas(self):
        position_zero = self.coord_zero()
        # Teste Bas
        if not (position_zero[0] == 0):
            plateau_teste_b = [row[:] for row in self.plateau]
            plateau_teste_b[position_zero[0]][position_zero[1]] = plateau_teste_b[position_zero[0] - 1][position_zero[1]]
            plateau_teste_b[position_zero[0] - 1][position_zero[1]] = 0
            self.bas_heuristique = self.heuristique(plateau_teste_b)
            self.bas_plateau = plateau_teste_b
    
    def teste_haut(self):
        position_zero = self.coord_zero()
        # Teste Haut
        if not(position_zero[0] == 2):
            plateau_teste_h = [row[:] for row in self.plateau]
            plateau_teste_h[position_zero[0]][position_zero[1]] = plateau_teste_h[position_zero[0] + 1][position_zero[1]]
            plateau_teste_h[position_zero[0] + 1][position_zero[1]] = 0
            self.haut_heuristique = self.heuristique(plateau_teste_h)
            self.haut_plateau = plateau_teste_h

    def teste_droite(self):
        position_zero = self.coord_zero()
        # Teste Droite
        if not(position_zero[1] == 2):
            plateau_teste_d = [row[:] for row in self.plateau]
            plateau_teste_d[position_zero[0]][position_zero[1]] = plateau_teste_d[position_zero[0]][position_zero[1] + 1]
            plateau_teste_d[position_zero[0]][position_zero[1] + 1] = 0
            self.droite_heuristique = self.heuristique(plateau_teste_d)
            self.droite_plateau = plateau_teste_d

    def teste_gauche(self):
        position_zero = self.coord_zero()
        # Teste Gauche
        if not(position_zero[1] == 0): 
            plateau_teste_g = [row[:] for row in self.plateau]
            plateau_teste_g[position_zero[0]][position_zero[1]] = plateau_teste_g[position_zero[0]][position_zero[1] - 1]
            plateau_teste_g[position_zero[0]][position_zero[1] - 1] = 0
            self.gauche_heuristique = self.heuristique(plateau_teste_g)
            self.gauche_plateau = plateau_teste_g

    def astar_solution(self):
        print("Lancement du teste de la résolution astar")
        i = 0
        
        historique = []
        dico_historique = {"f","g", "h", "état"}

        while self.plateau != self.solution and i < 100:
            #Faire le teste des quatre commande : 
            dico_historique = {"f" = ,"g" = , "h" = self.teste_bas[0], "état" = self.teste_bas[1]}



def jeu():
    plateau = Plateau(3)
    plateau.afficher()
    liste_commande = ["z", "q", "s", "d"]
    print("Appuyez sur z : haut, q : gauche, s : bas, d : droite")

    def on_key_press(key):
        if key.name in liste_commande:
            plateau.verifier_validiter_commande(key.name)
            plateau.afficher()
            if plateau.plateau == plateau.solution:
                print("Bravo vous avez réussi à terminer")
                keyboard.unhook_all()

    keyboard.on_press(on_key_press)

    keyboard.wait('esc') 


def solve_astar():
    plateau = Plateau(3)
    plateau.afficher()
    plateau.astar_solution()


if __name__ == "__main__":
    solve_astar()