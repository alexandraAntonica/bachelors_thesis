import subprocess
from pathlib import Path

# Input/output paths
PANAROO_DIR_SP = Path("/Users/alexandra/Desktop/thesis_programming/data/panaroo_output_SP")
PANAROO_DIR_NM = Path("/Users/alexandra/Desktop/thesis_programming/data/panaroo_output_NM")
PANAROO_DIR_SA = Path("/Users/alexandra/Desktop/thesis_programming/data/panaroo_output_SA")
PANAROO_DIR_ecoli = Path("/Users/alexandra/Desktop/thesis_programming/data/panaroo_output_Ecoli")

CORE_ALIGNMENT_SP = PANAROO_DIR_SP / "core_gene_alignment.aln"
SNP_OUTPUT_VCF_SP = PANAROO_DIR_SP / "core_gene_alignment.vcf"

CORE_ALIGNMENT_SA = PANAROO_DIR_SA / "core_gene_alignment.aln"
SNP_OUTPUT_VCF_SA = PANAROO_DIR_SA / "core_gene_alignment.vcf"

CORE_ALIGNMENT_NM = PANAROO_DIR_NM / "core_gene_alignment.aln"
SNP_OUTPUT_VCF_NM = PANAROO_DIR_NM / "core_gene_alignment.vcf"

CORE_ALIGNMENT_ecoli = PANAROO_DIR_ecoli / "core_gene_alignment.aln"
SNP_OUTPUT_VCF_ecoli = PANAROO_DIR_ecoli / "core_gene_alignment.vcf"


def run_snp_sites_vcf(core_alignment, snp_output_vcf):
    """
    Run SNP-sites to extract SNPs from the core alignment file and save them in VCF format.

    Parameters:
    - core_alignment (Path): Path to the core alignment file.
    - snp_output_vcf (Path): Path where the output VCF file will be saved.
    """
    cmd = [
            "docker", "run", "--rm", "-it",
            "-v", f"{core_alignment.parent}:/data",
            "staphb/snp-sites",
            "snp-sites",
            "-v",  # VCF output
            "-o", f"/data/{snp_output_vcf.name}",
            f"/data/{core_alignment.name}"
        ]

    subprocess.run(cmd, check=True)


def run_snp_sites_fasta(panaroo_dir):
    """
    Run SNP-sites to extract SNPs from the core alignment file and save them in FASTA format.

    Parameters:
    - panaroo_dir (Path): Path to the directory containing the core alignment file.
    """
    print("[SNP-sites] Extracting SNPs only as FASTA...")

    cmd = [
        "docker", "run", "--rm", "-it",
        "-v", f"{panaroo_dir}:/data",
        "staphb/snp-sites",
        "snp-sites", "-c", "-o", "/data/snps_only.fasta", "/data/core_gene_alignment.aln"
    ]

    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    run_snp_sites_vcf(CORE_ALIGNMENT_SP, SNP_OUTPUT_VCF_SP)
    run_snp_sites_fasta(PANAROO_DIR_SP)
    print("SNPs extracted as FASTA for SP.")

    run_snp_sites_vcf(CORE_ALIGNMENT_SA, SNP_OUTPUT_VCF_SA)
    run_snp_sites_fasta(PANAROO_DIR_SA)
    print("SNPs extracted as FASTA for SA.")

    run_snp_sites_vcf(CORE_ALIGNMENT_NM, SNP_OUTPUT_VCF_NM)
    run_snp_sites_fasta(PANAROO_DIR_NM)
    print("SNPs extracted as FASTA for NM.")

    run_snp_sites_vcf(CORE_ALIGNMENT_ecoli, SNP_OUTPUT_VCF_ecoli)
    run_snp_sites_fasta(PANAROO_DIR_ecoli)
    print("SNPs extracted as FASTA for Ecoli.")
