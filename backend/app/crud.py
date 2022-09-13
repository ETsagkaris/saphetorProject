import io
import pandas as pd

from . import settings


def get_vcf_data():
    path = settings.vcf_file
    with open(path, 'r') as f:
        lines = [line for line in f if not line.startswith('##')]
    return pd.read_csv(
        io.StringIO(''.join(lines)),
        usecols=["#CHROM", "ID", "REF", "POS", "ALT"],
        dtype={'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str},
        sep='\t'
    ).rename(columns={'#CHROM': 'CHROM'})


def save_data(data):
    header = """##fileformat=VCFv4.2
##source=myImputationProgramV3.1
##reference=file:///seq/references/
#CHROM	POS	ID	REF	ALT
    """
    with open(settings.vcf_file, 'w') as vcf_file:
        vcf_file.write(header)
    data.to_csv(settings.vcf_file, sep="\t", mode='a', index=False, header=False)


def create_record(variant):
    data = variant.dict()
    return pd.DataFrame({
        'CHROM': [data['CHROM']],
        'ID': [data['ID']],
        'REF': [data['REF']],
        'POS': [data['POS']],
        'ALT': [data['ALT']],
    })
