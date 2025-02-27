# Mini jeu taquin
# Import
import random
import keyboard
import heapq
import copy


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
        if nombre_traiter != 0:
            x_position = nombre_traiter % self.taille
            if x_position == 0:
                return  self.taille
            else:
                return x_position - 1
        else:
            return self.taille - 1

    def position_chiffre_y(self, nombre_traiter):
        if nombre_traiter != 0: 
            y_position = nombre_traiter // self.taille
            return y_position
        else: 
            return self.taille - 1
        
    def position (self,nombre):
        for y in range(self.taille):
            for x in range(self.taille):
                if nombre == self.solution[y][x]:
                    return [x,y]

    def heuristique(self,plateau):
        distance = 0

        for x in range(self.taille):
            for y in range(self.taille):
                position_voulu = self.position(plateau[x][y])
                print("nombre : ",plateau[x][y],"position :",position_voulu)
                distance += abs(x - position_voulu[0]) + abs (y - position_voulu[1])
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
                        
    def teste_deplacement(self):
        position_zero = self.coord_zero()
        
        deplacements = {
            "bas": (-1, 0),
            "haut": (1, 0),
            "droite": (0, 1),
            "gauche": (0, -1)
        }

        resultats = []
        
        for direction, (dx, dy) in deplacements.items():
            new_x, new_y = position_zero[0] + dx, position_zero[1] + dy
            
            if 0 <= new_x < self.taille and 0 <= new_y < self.taille:
                plateau_teste = [row[:] for row in self.plateau]
                plateau_teste[position_zero[0]][position_zero[1]] = plateau_teste[new_x][new_y]
                plateau_teste[new_x][new_y] = 0
                heuristique = self.heuristique(plateau_teste)
                resultats.append((heuristique, plateau_teste, direction))
            resultat_trier = sorted(resultats, key=lambda x: x[0])
        return resultat_trier


    def astar_solution(self):
        print("Lancement du teste de la résolution astar")
        i = 0
        
        historique = []
        historique_plateau = []
        plateau = copy.deepcopy(self.plateau)
        h = self.heuristique(self.plateau)
        historique.append({"f" : h ,"g" : 0, "h" : h, "etat": copy.deepcopy(self.plateau)})
        
        historique_plateau.append(plateau)
        print(historique)

        while self.plateau != self.solution and i < 10:
            #Faire le teste des quatre commande : 
            liste = self.teste_deplacement()
            print(liste)

            for possibilite in liste:
                if possibilite[1] not in historique_plateau:
                    plateau = copy.deepcopy(possibilite[1])
                    self.nombreCout +=1
                    self.plateau = plateau
                    historique_plateau.append(plateau)
                    f = self.nombreCout + possibilite[0]
                    g = self.nombreCout
                    h = possibilite[0]
                    historique.append({"f" : f,"g" : g, "h" : h, "etat": plateau})
            i += 1
        print("Terminé")



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
    plateau = Plateau(2)
    plateau.afficher()
    plateau.astar_solution()
    plateau.afficher()


if __name__ == "__main__":
    solve_astar()