import subprocess
from pathlib import Path
import csv

# Define paths
prokka_dir_SA = Path("/Users/alexandra/Desktop/thesis_programming/data/prokka_annotations_SA")
prokka_dir_SP = Path("/Users/alexandra/Desktop/thesis_programming/data/prokka_annotations_SP")
prokka_dir_Ecoli = Path("/Users/alexandra/Desktop/thesis_programming/data/prokka_annotations_Ecoli")

output_file_SA = "mlst_results_SA.csv"
output_file_SP = "mlst_results_SP.csv"
output_file_Ecoli = "mlst_results_Ecoli.csv"

header_SA = header = ['sample_ID', 'scheme', 'ST', 
              'adhP', 'pheS', 'atr', 'glnA', 'sdhA', 'glcK', 'tkt']
header_SP = ['sample_ID', 'scheme', 'ST', 
          'aroE', 'gdh', 'gki', 'recP', 'spi', 'xpt', 'ddl']
header_Ecoli = ['sample_ID', 'scheme', 'ST', 
          'adk', 'fumC', 'gyrB', 'icd', 'mdh', 'purA', 'recA']


def mlst(prokka_dir, output_file, header):
    """
    Runs MLST on Prokka-annotated .fna files and saves the results directly to a CSV file,
    including genome ID as the first column (no file path column).
    
    Parameters:
    - prokka_dir: Path object pointing to the folder with Prokka output subfolders
    - output_file: Path or filename for the output CSV
    """

    # Open CSV file and write the header
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)

        # Loop through each sample folder
        for fna_path in prokka_dir.glob("*/*.fna"):
            genome_id = fna_path.parent.name  # Use folder name as genome ID

            docker_command = [
                "docker", "run", "--rm",
                "-v", f"{prokka_dir}:/data",
                "quay.io/biocontainers/mlst:2.9--h7b50bb2_6",
                "mlst", f"/data/{fna_path.parent.name}/{fna_path.name}"
            ]

            print(f"Running MLST on {fna_path.name} (Genome ID: {genome_id})...")

            try:
                # Run the Docker command and capture the output
                result = subprocess.run(docker_command, capture_output=True, text=True, check=True)
                line = result.stdout.strip().split("\t")
                # Remove the first column (filepath) from MLST output
                line_without_filepath = line[1:]  
                # Prepend genome ID
                writer.writerow([genome_id] + line_without_filepath)
            except subprocess.CalledProcessError as e:
                print(f"Error processing {fna_path.name}: {e.stderr}")
                # Write error row with genome_ID
                writer.writerow([genome_id, 'ERROR'] + [''] * (len(header) - 2))

    print(f"\n MLST results saved as CSV in: {output_file}")


if __name__ == "__main__":
    mlst(prokka_dir_SA, output_file_SA, header_SA)
    mlst(prokka_dir_SP, output_file_SP, header_SP)
    mlst(prokka_dir_Ecoli, output_file_Ecoli, header_Ecoli)