def creation_lst_modifie(lst_coords: list, piece: str) -> tuple :
    """Renvoie la liste modifié avec comme origine le deuxième ou troisième point de la liste."""
    lst_modifie = list()

    if piece in ["I", "Z", "L"] :
        for x, y in lst_coords :
            lst_modifie.append((x - lst_coords[1][0], y - lst_coords[1][1]))
            origine = lst_coords[1]

    elif piece in ["T", "S", "J"] :
        for x, y in lst_coords :
            lst_modifie.append((x - lst_coords[2][0], y - lst_coords[2][1]))
            origine = lst_coords[2]
        
    return lst_modifie, origine


def rotation(lst_coords: list, piece: str, dir: str) -> list :
    """Renvoie la liste des coordonnées modifié avec la rotation dans le sens dir."""

    lst_modifie, origine = creation_lst_modifie(lst_coords, piece)
    lst_coords_modifie = list()
    lst_resultat = list()

    for x, y in lst_modifie :
        if dir == "Clockwise" :
            lst_coords_modifie.append((y, -x))
        else :
            lst_coords_modifie.append((-y, x))
    
    for x, y in lst_coords_modifie :
        lst_resultat.append([x + origine[0], y + origine[1]])

    return lst_resultat
