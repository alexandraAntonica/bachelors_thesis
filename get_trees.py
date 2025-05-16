import subprocess
from pathlib import Path

SP_DIR = Path("/Users/alexandra/Desktop/thesis_programming/data/panaroo_output_SP")
SA_DIR = Path("/Users/alexandra/Desktop/thesis_programming/data/panaroo_output_SA")
NM_DIR = Path("/Users/alexandra/Desktop/thesis_programming/data/panaroo_output_NM")
Ecoli_DIR = Path("/Users/alexandra/Desktop/thesis_programming/data/panaroo_output_Ecoli")

ALIGNMENT_FILE_SP = SP_DIR / "snps_only.fasta"
ALIGNMENT_FILE_SA = SA_DIR / "snps_only.fasta"
ALIGNMENT_FILE_NM = NM_DIR / "snps_only.fasta"
ALIGNMENT_FILE_Ecoli = Ecoli_DIR / "snps_only.fasta"


TREE_FILE_SP = SP_DIR / "snps_only.fasta.treefile"
TREE_FILE_SA = SA_DIR / "snps_only.fasta.treefile"
TREE_FILE_NM = NM_DIR / "snps_only.fasta.treefile"
TREE_FILE_Ecoli = Ecoli_DIR / "snps_only.fasta.treefile"

def run_iqtree(data_dir):
    print("[IQ-TREE] Building tree using Docker...")

    cmd = [
        "docker", "run", "--rm", "-it",
        "-v", f"{data_dir}:/data",
        "staphb/iqtree",
        "iqtree", "-s", "/data/snps_only.fasta",
        "-m", "GTR+G",
        "-nt", "AUTO"
    ]
    subprocess.run(cmd, check=True)
    print(f"Tree built")


if __name__ == "__main__":
    run_iqtree(SP_DIR)
    run_iqtree(SA_DIR)
    run_iqtree(NM_DIR)
    run_iqtree(Ecoli_DIR)
    print("All trees built successfully.")
