
# ==============================================================
# PROJET : ANALYSE DES DONNEES DE SANTE MENTALE
# Auteur : MUHINDO KISUMBA Abdiel
# Bibliotheques : Pandas, NumPy, Matplotlib, OpenPyXL
# Objectif : Analyse statistique et epidemiologique
# ==============================================================


# 1. IMPORTATION DES BIBLIOTHEQUES

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter


# 2. IMPORTATION DU FICHIER EXCEL

# Remplacer le nom par celui de votre fichier Excel
df = pd.read_excel("donnees_sante_mentale.xlsx")

print("\n========== APERCU DES DONNEES ==========")
print(df.head())

# Afficher les dimensions du fichier
print("\nNombre de lignes et colonnes :", df.shape)

# Afficher les informations generales
print("\nInformations sur les variables :")
df.info()


# 3. NETTOYAGE DES DONNEES

# Uniformiser les noms des colonnes
df.columns = df.columns.str.strip().str.lower()

# Supprimer les espaces dans les colonnes textuelles
for colonne in df.select_dtypes(include="object").columns:
    df[colonne] = df[colonne].str.strip()

# Supprimer les doublons
df = df.drop_duplicates()

# Convertir l'age en variable numerique
df["age"] = pd.to_numeric(df["age"], errors="coerce")

# Convertir la date en format date
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Afficher les valeurs manquantes
print("\n========== VALEURS MANQUANTES ==========")
print(df.isnull().sum())

# Afficher le nombre de doublons restants
print("\nDoublons restants :", df.duplicated().sum())


# 4. ANALYSE STATISTIQUE DESCRIPTIVE

print("\n========== STATISTIQUES DESCRIPTIVES ==========")

# Nombre total de dossiers
print("Nombre total de dossiers :", len(df))

# Age moyen
print("Age moyen :", round(df["age"].mean(), 2))

# Age median
print("Age median :", df["age"].median())

# Age minimum
print("Age minimum :", df["age"].min())

# Age maximum
print("Age maximum :", df["age"].max())

# Ecart-type de l'age
print("Ecart-type :", round(df["age"].std(), 2))


# 5. CREATION DES TRANCHES D'AGE

# Classer les patients selon leur age
df["tranche_age"] = pd.cut(
    df["age"],
    bins=[0, 14, 24, 44, 59, 120],
    labels=[
        "0-14 ans",
        "15-24 ans",
        "25-44 ans",
        "45-59 ans",
        "60 ans et plus"
    ],
    include_lowest=True
)

# Afficher la repartition par tranche d'age
print("\n========== REPARTITION PAR AGE ==========")
print(df["tranche_age"].value_counts().sort_index())


# 6. ANALYSE DE LA REPARTITION PAR SEXE

print("\n========== REPARTITION PAR SEXE ==========")

sexe = df["sexe"].value_counts()

print(sexe)

# Calcul des pourcentages
pourcentage_sexe = df["sexe"].value_counts(normalize=True) * 100

print("\nPourcentages par sexe :")
print(pourcentage_sexe.round(2))


# 7. ANALYSE PAR ZONE DE SANTE

print("\n========== REPARTITION PAR ZONE DE SANTE ==========")

zone = df["zone_sante"].value_counts()

print(zone)

# Pourcentage par zone
print("\nPourcentage par zone :")
print((zone / len(df) * 100).round(2))


# 8. ANALYSE PAR TYPE DE TROUBLE MENTAL

print("\n========== TYPES DE TROUBLES MENTAUX ==========")

troubles = df["type_trouble"].value_counts()

print(troubles)

# Calcul des proportions
print("\nProportions des troubles :")
print((troubles / len(df) * 100).round(2))


# 9. ANALYSE DE LA PRISE EN CHARGE

print("\n========== STATUT DE PRISE EN CHARGE ==========")

prise_en_charge = df["statut_prise_en_charge"].value_counts()

print(prise_en_charge)

# Pourcentage de prise en charge
print("\nPourcentage :")
print((prise_en_charge / len(df) * 100).round(2))


# 10. ANALYSE CROISEE ENTRE SEXE ET TROUBLE

print("\n========== SEXE ET TYPE DE TROUBLE ==========")

croisement_sexe = pd.crosstab(
    df["sexe"],
    df["type_trouble"],
    margins=True
)

print(croisement_sexe)


# 11. ANALYSE CROISEE ENTRE ZONE ET TROUBLE

print("\n========== ZONE ET TYPE DE TROUBLE ==========")

croisement_zone = pd.crosstab(
    df["zone_sante"],
    df["type_trouble"],
    margins=True
)

print(croisement_zone)


# 12. ANALYSE TEMPORELLE DES CAS

print("\n========== EVOLUTION MENSUELLE ==========")

# Extraire le mois et l'annee
df["mois"] = df["date"].dt.to_period("M")

# Calculer le nombre de dossiers par mois
evolution = df.groupby("mois").size()

print(evolution)


# 13. VISUALISATION : REPARTITION PAR SEXE

plt.figure(figsize=(8, 5))

sexe.plot(kind="bar")

plt.title("Repartition des cas de sante mentale par sexe")
plt.xlabel("Sexe")
plt.ylabel("Nombre de dossiers")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("repartition_sexe.png", dpi=300)
plt.show()


# 14. VISUALISATION : REPARTITION PAR ZONE DE SANTE

plt.figure(figsize=(10, 6))

zone.sort_values().plot(kind="barh")

plt.title("Repartition des cas par zone de sante")
plt.xlabel("Nombre de dossiers")
plt.ylabel("Zone de sante")
plt.tight_layout()
plt.savefig("repartition_zone.png", dpi=300)
plt.show()


# 15. VISUALISATION : TYPES DE TROUBLES MENTAUX

plt.figure(figsize=(9, 6))

troubles.plot(kind="bar")

plt.title("Repartition des types de troubles mentaux")
plt.xlabel("Type de trouble")
plt.ylabel("Nombre de dossiers")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("types_troubles.png", dpi=300)
plt.show()


# 16. VISUALISATION : TRANCHES D'AGE

plt.figure(figsize=(9, 5))

df["tranche_age"].value_counts().sort_index().plot(kind="bar")

plt.title("Repartition des cas par tranche d'age")
plt.xlabel("Tranche d'age")
plt.ylabel("Nombre de dossiers")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("repartition_age.png", dpi=300)
plt.show()


# 17. VISUALISATION : EVOLUTION MENSUELLE

plt.figure(figsize=(12, 6))

evolution.plot(kind="line", marker="o")

plt.title("Evolution mensuelle des cas de sante mentale")
plt.xlabel("Mois")
plt.ylabel("Nombre de dossiers")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("evolution_mensuelle.png", dpi=300)
plt.show()


# 18. EXPORTATION DES RESULTATS VERS EXCEL

# Creer un rapport contenant plusieurs feuilles
with pd.ExcelWriter(
    "rapport_analyse_sante_mentale.xlsx",
    engine="openpyxl"
) as writer:

    # Donnees nettoyees
    df.to_excel(
        writer,
        sheet_name="Donnees",
        index=False
    )

    # Repartition par sexe
    sexe.rename("Effectif").to_excel(
        writer,
        sheet_name="Analyse_sexe"
    )

    # Repartition par zone
    zone.rename("Effectif").to_excel(
        writer,
        sheet_name="Analyse_zones"
    )

    # Types de troubles
    troubles.rename("Effectif").to_excel(
        writer,
        sheet_name="Analyse_troubles"
    )

    # Prise en charge
    prise_en_charge.rename("Effectif").to_excel(
        writer,
        sheet_name="Prise_en_charge"
    )

    # Analyse croisee
    croisement_sexe.to_excel(
        writer,
        sheet_name="Sexe_et_trouble"
    )

    croisement_zone.to_excel(
        writer,
        sheet_name="Zone_et_trouble"
    )

    # Evolution mensuelle
    evolution.to_frame("Nombre_de_cas").to_excel(
        writer,
        sheet_name="Evolution"
    )


# 19. MISE EN FORME DU RAPPORT EXCEL AVEC OPENPYXL

# Ouvrir le fichier Excel genere
classeur = load_workbook("rapport_analyse_sante_mentale.xlsx")

# Parcourir toutes les feuilles
for feuille in classeur.worksheets:

    # Mise en forme des en-tetes
    for cellule in feuille[1]:

        cellule.font = Font(
            bold=True,
            color="FFFFFF"
        )

        cellule.fill = PatternFill(
            start_color="1F4E78",
            end_color="1F4E78",
            fill_type="solid"
        )

        cellule.alignment = Alignment(
            horizontal="center"
        )

    # Ajustement automatique de la largeur des colonnes
    for colonne in feuille.columns:

        longueur_max = 0
        lettre = get_column_letter(colonne[0].column)

        for cellule in colonne:

            if cellule.value is not None:
                longueur_max = max(
                    longueur_max,
                    len(str(cellule.value))
                )

        feuille.column_dimensions[lettre].width = longueur_max + 3

# Enregistrer les modifications
classeur.save("rapport_analyse_sante_mentale.xlsx")


# 20. MESSAGE FINAL

print("\n==============================================")
print("ANALYSE DES DONNEES TERMINEE AVEC SUCCES !")
print("==============================================")

print("Nombre total de dossiers :", len(df))

print("Fichier Excel genere : rapport_analyse_sante_mentale.xlsx")

print("Graphiques generes :")
print("- repartition_sexe.png")
print("- repartition_zone.png")
print("- types_troubles.png")
print("- repartition_age.png")
print("- evolution_mensuelle.png")

print("\nMerci d'avoir utilise ce programme !")
