import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import pdist

# load gene presence-absence matrices
SP_matrix = pd.read_csv("/Users/alexandra/Desktop/thesis_programming/data/panaroo_output_SP/gene_presence_absence.csv")
NM_matrix = pd.read_csv("/Users/alexandra/Desktop/thesis_programming/data/panaroo_output_NM/gene_presence_absence.csv")
ecoli_matrix = pd.read_csv("/Users/alexandra/Desktop/thesis_programming/data/panaroo_output_Ecoli/gene_presence_absence.csv")
SA_matrix = pd.read_csv("/Users/alexandra/Desktop/thesis_programming/data/panaroo_output_SA/gene_presence_absence.csv")

def get_binary_matrix(matrix, keep_annotation_cols=3):
    """
    Loads a Panaroo gene_presence_absence.csv and converts it to a binary matrix
    indicating gene presence (1) or absence (0) per genome.

    Parameters:
    - matrix in which the gene presence/absence data was loaded
    - keep_annotation_cols (int): Number of annotation/meta columns before genome columns start (usually 3).

    Returns:
    - binary_matrix, the gene presence/absence matrix with genome names as index and 1 if gene is present, 0 if absent.
    """

    # indeces will be the gene names
    matrix.index = matrix.iloc[:, 0]  # usually "Gene" column
    matrix = matrix.iloc[:, keep_annotation_cols:]  # drop annotation cols

    # convert to binary presence/absence matrix
    binary_matrix = matrix.notnull().astype(int)

    return binary_matrix

presence_absence_SP = get_binary_matrix(SP_matrix)
presence_absence_NM = get_binary_matrix(NM_matrix)
presence_absence_ecoli = get_binary_matrix(ecoli_matrix)
presence_absence_SA = get_binary_matrix(SA_matrix)

matrices = {
    "SP": presence_absence_SP,
    "NM": presence_absence_NM,
    "Ecoli": presence_absence_ecoli,
    "SA": presence_absence_SA
}

for name, matrix in matrices.items():
    row_linkage = linkage(pdist(matrix, metric="jaccard"), method="ward")

    sns.set_theme(style="white")
    g = sns.clustermap(
        matrix,
        row_linkage=row_linkage,
        col_cluster=False,
        cmap="Blues",
        xticklabels=False,  # the labels are not well visible because the matrix is too big, so we set to false
        yticklabels=False, # same here
        figsize=(24, 12)
    )

    g.ax_heatmap.set_xlabel(f"{matrix.shape[1]} gene clusters")
    g.ax_heatmap.set_ylabel(f"{matrix.shape[0]} strains")
    plt.title(f"Presence/Absence of Gene Clusters - {name}", y=1.05)
    plt.savefig(f"panaroo_matrix_clustermap_{name}.png", dpi=300)
    plt.show()
