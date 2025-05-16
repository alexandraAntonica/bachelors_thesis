
import pandas as pd
import allel

rgi_df = pd.read_csv("/Users/alexandra/Desktop/thesis_programming/data/rgi_results_Ecoli/resistance_matrix.csv")
gene_df = pd.read_csv("/Users/alexandra/Desktop/thesis_programming/data/panaroo_output_Ecoli/gene_presence_absence.csv")
mlst_df = pd.read_csv("/Users/alexandra/Desktop/thesis_programming/mlst_results_Ecoli.csv")


# Clean the gene presence/absence matrix
# remove columns 2 and 3
gene_df.drop(gene_df.columns[[1, 2]], axis=1, inplace=True)

# Keep the first column unchanged then binarize columns
gene_df_binary = gene_df.copy()
gene_df_binary.iloc[:, 1:] = gene_df_binary.iloc[:, 1:].notnull().astype(int)

# Transpose the DataFrame so genes become columns, and samples become rows
transposed_df = gene_df_binary.set_index('Gene').T
transposed_df.index.name = 'sample_ID'
transposed_df = transposed_df.reset_index()



# Clean the resistance gene matrix
# Keep the columns corresponding to the TMP, CTX, and SUL drugs
new_df = rgi_df[["Unnamed: 0","diaminopyrimidine antibiotic", "cephalosporin", "sulfonamide antibiotic"]]
new_df = new_df.rename(columns={"Unnamed: 0": "sample_ID", "diaminopyrimidine antibiotic": "TMP", "cephalosporin": "CTX", "sulfonamide antibiotic": "SUL"})



# Create SNPs matrix and prepare for merging
callset = allel.read_vcf("/Users/alexandra/Desktop/thesis_programming/data/panaroo_output_Ecoli/core_gene_alignment.vcf")

# Get samples and genotypes
samples = callset['samples']
genotypes = callset['calldata/GT']

# Shape of genotypes: (variants, samples, ploidy)
print("Genotype shape:", genotypes.shape)

# Convert to haploid (first allele only)
snp_matrix = genotypes[:, :, 0]  # shape: (variants, samples)

# Transpose to make (samples, variants) for ML
binary_snp_matrix = (snp_matrix == 1).astype(int).T

# Confirm shape before DataFrame creation
print("Binary SNP matrix shape:", binary_snp_matrix.shape)
print("Number of samples:", len(samples))

# Now column names must match number of SNPs (variants)
num_snps = binary_snp_matrix.shape[1]
snp_columns = [f"SNP_{i}" for i in range(num_snps)]

# Create the DataFrame
df_snp = pd.DataFrame(binary_snp_matrix, index=samples, columns=snp_columns)

# Optional: Reset index to turn sample_ID into a column
df_snp.index.name = "sample_ID"
df_snp.reset_index(inplace=True)


# Merge SNPs matrix, resitance labels and gene presence/absence matrix on 'sample_ID'
final_df = pd.merge(new_df,transposed_df, on="sample_ID", how="inner")
final_df = pd.merge(final_df, df_snp, on="sample_ID", how="inner")



# Merge the MLST
mlst_df_reduced = mlst_df[['sample_ID', 'ST']]
final_df = pd.merge(final_df, mlst_df_reduced, on='sample_ID', how='inner')

# Save to CSV
final_df.to_csv("final_Ecoli.csv", index=False)


