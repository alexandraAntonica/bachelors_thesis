# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import subprocess
from pathlib import Path
import requests
import webbrowser

DATA_DIR = Path("/Users/alexandra/Desktop/thesis_programming/data/panaroo_output_SP")
ALIGNMENT_FILE = DATA_DIR / "snps_only.fasta"
TREE_FILE = DATA_DIR / "snps_only.fasta.treefile"

ITOL_API_KEY = "r7i0nMpa6m7YxoxmtRzCXw"


def run_iqtree():
    print("[IQ-TREE] Building tree using Docker...")

    cmd = [
        "docker", "run", "--rm", "-it",
        "-v", f"{DATA_DIR}:/data",
        "staphb/iqtree",
        "iqtree", "-s", "/data/snps_only.fasta",
        "-m", "GTR+G",
        "-nt", "AUTO"
    ]
    subprocess.run(cmd, check=True)
    print(f"Tree built at: {TREE_FILE}")


def upload_to_itol():
    if not TREE_FILE.exists():
        raise FileNotFoundError(f"Tree file not found: {TREE_FILE}")

    print("[iTOL] Uploading tree to iTOL...")

    url = "https://itol.embl.de/batch_uploader.cgi"
    files = {'treeFile': TREE_FILE.open('rb')}
    payload = {
        "APIkey": ITOL_API_KEY,
        "treeName": "Panaroo SNP Tree",
        "treeFormat": "newick"
    }

    response = requests.post(url, files=files, data=payload)
    response.raise_for_status()

    if "upload_id" in response.text:
        upload_id = response.text.strip().split("upload_id:")[-1].strip()
        itol_url = f"https://itol.embl.de/tree/{upload_id}"
        print(f"Tree uploaded to iTOL: {itol_url}")
        webbrowser.open(itol_url)
    else:
        print("iTOL upload failed.")
        print(response.text)


if __name__ == "__main__":
    run_iqtree()
    #upload_to_itol() # NOT WORKING WITH API KEY, MODIFY THIS !!!!!!!!!!!!!!

    ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
