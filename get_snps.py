import subprocess
from pathlib import Path

# Input/output paths
PANAROO_DIR = Path("/Users/alexandra/Desktop/thesis_programming/data/panaroo_output_SP")
CORE_ALIGNMENT = PANAROO_DIR / "core_gene_alignment.aln"
SNP_OUTPUT_VCF = PANAROO_DIR / "core_gene_alignment.vcf"
SNP_OUTPUT_FASTA = PANAROO_DIR / "snps_only.fasta"

def run_snp_sites_vcf():
   
    cmd = [
        "docker", "run", "--rm", "-it",
        "-v", f"{CORE_ALIGNMENT.parent}:/data",
        "staphb/snp-sites",
        "snp-sites",
        "-v",  # VCF output
        "-o", f"/data/{SNP_OUTPUT_VCF.name}",
        f"/data/{CORE_ALIGNMENT.name}"
    ]

    subprocess.run(cmd, check=True)


def run_snp_sites_fasta():
    print("[SNP-sites] Extracting SNPs only as FASTA...")

    cmd = [
        "docker", "run", "--rm", "-it",
        "-v", f"{PANAROO_DIR}:/data",
        "staphb/snp-sites",
        "snp-sites", "-c", "-o", "/data/snps_only.fasta", "/data/core_gene_alignment.aln"
    ]

    subprocess.run(cmd, check=True)
    print(f"SNP FASTA saved to: {SNP_OUTPUT_FASTA}")

if __name__ == "__main__":
    run_snp_sites_vcf()
    run_snp_sites_fasta()
