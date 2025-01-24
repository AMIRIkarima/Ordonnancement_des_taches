import streamlit as st
import matplotlib.pyplot as plt

def flowtime(tasks):
    """
    Calcule le flowtime total (temps de traitement) en utilisant la stratégie Shortest Processing Time (SPT).
    Affiche un diagramme de Gantt pour représenter l'ordre des tâches.

    Args:
        tasks (list of int): Liste des durées des tâches.

    Returns:
        int: Le flowtime total.
    """
    # Trier les tâches par ordre croissant de leur durée
    tasks_sorted = sorted(tasks)

    # Initialisation
    total_time = 0
    current_time = 0
    flow_times = []  # Stocker les temps de fin pour chaque tâche
    task_intervals = []  # Stocker les intervalles pour le diagramme de Gantt

    for i, task in enumerate(tasks_sorted):
        start_time = current_time
        current_time += task  # Mettre à jour le temps courant
        total_time += current_time  # Ajouter au flowtime total
        flow_times.append(current_time)
        task_intervals.append((start_time, task))  # Ajouter l'intervalle de la tâche

    # Diagramme de Gantt
    fig, ax = plt.subplots(figsize=(10, 3))
    for i, (start, duration) in enumerate(task_intervals):
        ax.barh("Tâches", duration, left=start, color="skyblue", edgecolor="black", alpha=0.8)
        ax.text(start + duration / 2, 0, f"T{i+1}", ha="center", va="center", color="black")

    ax.set_title("Diagramme de Gantt : Shortest Processing Time (SPT)")
    ax.set_xlabel("Temps")
    ax.set_ylabel("Tâches")
    ax.grid(axis="x", linestyle="--", alpha=0.7)
    st.pyplot(fig)

    return total_time


def minimize_lateness(tasks):
    """
    Minimise le retard total en planifiant les tâches selon la stratégie Earliest Due Date (EDD).
    Affiche un diagramme de Gantt pour représenter l'ordre des tâches.

    Args:
        tasks (list of tuple): Liste de tuples (durée, date de livraison).

    Returns:
        dict: Résultats incluant l'ordre optimal et le retard total.
    """
    # Trier les tâches par date de livraison croissante
    tasks_sorted = sorted(tasks, key=lambda x: x[1])

    # Initialisation
    current_time = 0
    total_lateness = 0
    task_intervals = []  # Stocker les intervalles pour le diagramme de Gantt

    for i, (duration, due_date) in enumerate(tasks_sorted):
        start_time = current_time
        current_time += duration  # Mettre à jour le temps courant
        lateness = max(0, current_time - due_date)  # Calculer le retard
        total_lateness += lateness  # Ajouter au retard total
        task_intervals.append((start_time, duration))  # Ajouter l'intervalle de la tâche

    # Diagramme de Gantt
    fig, ax = plt.subplots(figsize=(10, 3))
    for i, (start, duration) in enumerate(task_intervals):
        ax.barh("Tâches", duration, left=start, color="lightgreen", edgecolor="black", alpha=0.8)
        ax.text(start + duration / 2, 0, f"T{i+1}", ha="center", va="center", color="black")

    ax.set_title("Diagramme de Gantt : Earliest Due Date (EDD)")
    ax.set_xlabel("Temps")
    ax.set_ylabel("Tâches")
    ax.grid(axis="x", linestyle="--", alpha=0.7)
    st.pyplot(fig)

    return {
        'ordre': tasks_sorted,
        'retard_total': total_lateness
    }


# Interface Streamlit
st.title("Ordonnancement des Tâches")
st.write("Visualisation des algorithmes SPT (Shortest Processing Time) et EDD (Earliest Due Date).")

# Input pour SPT
st.header("SPT : Minimisation du Flowtime")
tasks_input = st.text_input("Entrez les durées des tâches séparées par des virgules :", "5, 2, 8, 3, 6")
if st.button("Calculer Flowtime"):
    try:
        tasks = [int(x.strip()) for x in tasks_input.split(",")]
        total_flowtime = flowtime(tasks)
        st.success(f"Flowtime total (SPT) : {total_flowtime}")
    except ValueError:
        st.error("Veuillez entrer des durées valides (nombres entiers).")

# Input pour EDD
st.header("EDD : Minimisation du Retard")
tasks_edd_input = st.text_area("Entrez les tâches au format (durée, date de livraison) ligne par ligne :", "3, 10\n2, 5\n1, 8\n4, 12")
if st.button("Calculer Retard Total"):
    try:
        tasks_edd = [tuple(map(int, line.split(","))) for line in tasks_edd_input.strip().split("\n")]
        resultat = minimize_lateness(tasks_edd)
        st.success(f"Retard total minimisé (EDD) : {resultat['retard_total']}")
    except ValueError:
        st.error("Veuillez entrer des tâches valides au format (durée, date de livraison).")


