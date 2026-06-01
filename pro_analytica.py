import os
from Bio import Entrez, SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import matplotlib.pyplot as plt

# Always provide your email when using NCBI Entrez database
Entrez.email = "your.email@example.com"

class ProAnalytica:
    def __init__(self, ncbi_id):
        self.ncbi_id = ncbi_id
        self.raw_seq_record = None
        self.protein_seq = "" 
        self.analysis_results = {}

    def fetch_sequence(self):
        """Fetches a Nucleotide or Protein sequence from NCBI."""
        print(f"📡 Fetching sequence data for ID: {self.ncbi_id} from NCBI...")
        try:
            # Fetching from nucleotide database as an example
            handle = Entrez.efetch(db="nucleotide", id=self.ncbi_id, rettype="fasta", retmode="text")
            self.raw_seq_record = SeqIO.read(handle, "fasta")
            handle.close()
            print(" Successfully downloaded sequence!")
        except Exception as e:
            print(f" Error fetching from NCBI: {e}")

    def process_and_translate(self):
        """Checks sequence type and translates to protein if it's DNA/RNA."""
        if not self.raw_seq_record:
            return
        
        sequence = self.raw_seq_record.seq
        
        # Simple check to differentiate nucleotide from amino acid sequence
        if set(sequence.upper()).issubset({"A", "T", "C", "G", "N", "U"}):
            print(" Nucleotide sequence detected. Translating to Protein sequence...")
            # Translate up to the first stop codon to avoid trailing characters
            self.protein_seq = str(sequence.translate(to_stop=True))
        else:
            print(" Protein sequence detected. Proceeding directly...")
            self.protein_seq = str(sequence)
            
        # Strip out any unexpected non-standard amino acid characters for stability
        self.protein_seq = "".join([amino for amino in self.protein_seq if amino in "ACDEFGHIKLMNPQRSTVWY"])
        print(f" Processed Protein Length: {len(self.protein_seq)} amino acids.")

    def run_protein_profiling(self):
        """Calculates advanced structural and chemical metrics of the protein."""
        if not self.protein_seq:
            print(" No valid protein sequence available for analysis.")
            return

        print("Calculating structural parameters and composition maps...")
        analyser = ProteinAnalysis(self.protein_seq)
        
        self.analysis_results['molecular_weight'] = analyser.molecular_weight()
        self.analysis_results['aromaticity'] = analyser.aromaticity()
        self.analysis_results['instability_index'] = analyser.instability_index()
        self.analysis_results['isoelectric_point'] = analyser.isoelectric_point()
        self.analysis_results['amino_acid_count'] = analyser.count_amino_acids()
        self.analysis_results['secondary_structure_fraction'] = analyser.secondary_structure_fraction() # (Helix, Turn, Sheet)

    def generate_report(self):
        """Prints a scannable summary report and flags protein stability."""
        if not self.analysis_results:
            return

        print("\n" + "="*45)
        print(f" BIOINFORMATICS REPORT FOR: {self.ncbi_id}")
        print("="*45)
        print(f"• Molecular Weight:    {self.analysis_results['molecular_weight']:.2f} Da")
        print(f"• Isoelectric Point:   {self.analysis_results['isoelectric_point']:.2f}")
        print(f"• Aromaticity Score:   {self.analysis_results['aromaticity']:.4f}")
        print(f"• Instability Index:   {self.analysis_results['instability_index']:.2f}")
        
        # Check structural stability based on the threshold (40)
        status = " Unstable in test tube" if self.analysis_results['instability_index'] > 40 else " Stable in test tube"
        print(f"• Structural Status:   {status}")
        
        sec_struct = self.analysis_results['secondary_structure_fraction']
        print(f"• Helix Fraction:      {sec_struct[0]*100:.1f}%")
        print(f"• Turn Fraction:       {sec_struct[1]*100:.1f}%")
        print(f"• Sheet Fraction:      {sec_struct[2]*100:.1f}%")
        print("="*45)

    def plot_amino_acid_distribution(self):
        """Generates a clean visual frequency plot of the amino acids."""
        if not self.analysis_results:
            return
        
        counts = self.analysis_results['amino_acid_count']
        
        plt.figure(figsize=(10, 5))
        plt.bar(counts.keys(), counts.values(), color='teal', edgecolor='black')
        plt.title(f"Amino Acid Frequency Mapping ({self.ncbi_id})", fontsize=14, fontweight='bold')
        plt.xlabel("Amino Acid Residues", fontsize=12)
        plt.ylabel("Occurrences Count", fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Save visualization to local workspace
        output_file = f"{self.ncbi_id}_aa_distribution.png"
        plt.savefig(output_file)
        plt.close()
        print(f" Visual graph generated and saved safely as '{output_file}'!")

# --- Execution Entry Point ---
if __name__ == "__main__":
    # Example NCBI Accession ID: NM_000558 (Human Hemoglobin Subunit Alpha mRNA)
    TARGET_ID = "NM_000558"
    
    pipeline = ProAnalytica(ncbi_id=TARGET_ID)
    pipeline.fetch_sequence()
    pipeline.process_and_translate()
    pipeline.run_protein_profiling()
    pipeline.generate_report()
    pipeline.plot_amino_acid_distribution()
