import os
import subprocess
import pandas as pd
from glob import glob
from tqdm import tqdm

PROKKA_DIR = "/Users/alexandra/Desktop/thesis_programming/data/prokka_annotations_NM"
RGI_OUTPUT_DIR = "/Users/alexandra/Desktop/thesis_programming/data/rgi_results_NM"
DOCKER_IMAGE = "quay.io/biocontainers/rgi:6.0.3--pyha8f3691_0"
NUM_THREADS = 8

os.makedirs(RGI_OUTPUT_DIR, exist_ok=True)

def run_rgi_with_docker(faa_path, output_txt):
    faa_filename = os.path.basename(faa_path)
    output_name = os.path.splitext(faa_filename)[0]

    cmd = [
        "docker", "run", "--rm",
        "-v", f"{os.path.dirname(faa_path)}:/input",
        "-v", f"{RGI_OUTPUT_DIR}:/output",
        DOCKER_IMAGE,
        "rgi", "main",
        "--input_sequence", f"/input/{faa_filename}",
        "--output_file", f"/output/{output_name}",
        "--input_type", "protein",
        "--num_threads", str(NUM_THREADS)
    ]

    subprocess.run(cmd, check=True)

def parse_rgi_output(txt_file):
    df = pd.read_csv(txt_file, sep="\t")
    drug_classes = set()

    if "Drug Class" in df.columns:
        for drug_list in df["Drug Class"].dropna():
            for drug in drug_list.split(", "):
                drug_classes.add(drug.strip())
    
    return drug_classes

# Step 1: Run RGI on each .faa
print("[Step 1] Running RGI using Docker...")
faa_files = glob(os.path.join(PROKKA_DIR, "*", "*.faa"))
rgi_matrix = {}

for faa in tqdm(faa_files):
    genome_id = os.path.basename(os.path.dirname(faa))
    output_txt = os.path.join(RGI_OUTPUT_DIR, f"{genome_id}.txt")

    if not os.path.exists(output_txt):
        try:
            run_rgi_with_docker(faa, output_txt)
        except subprocess.CalledProcessError as e:
            print(f"Error processing {genome_id}: {e}")
            continue

    if os.path.exists(output_txt):
        rgi_matrix[genome_id] = parse_rgi_output(output_txt)


# Step 2: Build binary resistance matrix
print("[Step 2] Constructing resistance matrix...")
all_drugs = sorted(set().union(*rgi_matrix.values()))
df = pd.DataFrame(0, index=rgi_matrix.keys(), columns=all_drugs)

for genome, drugs in rgi_matrix.items():
    for drug in drugs:
        df.loc[genome, drug] = 1

# Step 3: Save matrix
output_file = os.path.join(RGI_OUTPUT_DIR, "resistance_matrix.csv")
df.to_csv(output_file)
print(f"[Done] Resistance matrix saved to {output_file}")
