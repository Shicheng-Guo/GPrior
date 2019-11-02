from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import pandas as pd
import numpy as np

DO_NOT_NEED = ['ld_snp_rsID',
               'chrom',
               'pos',
               'GRCh38_chrom',
               'gwas_size',
               'GRCh38_pos',
               'GRCh38_gene_chrom',
               'gene_chrom',
               'gene_tss',
               'GRCh38_gene_pos',
               'disease_name',
               'disease_efo_id',
               'cluster_id',
               'gwas_source',
               'gwas_snp',
               'gwas_pvalue_description',
               'gwas_odds_ratio',
               'gwas_odds_ratio_ci_start',
               'gwas_odds_ratio_ci_end',
               'gwas_size',
               'gwas_pmid',
               'gwas_study',
               'gwas_reported_trait',
               'vep_terms',
               'gnomad',
               'gnomad_sas',
               'gnomad_oth',
               'gnomad_asj',
               'gnomad_nfe',
               'gnomad_afr',
               'gnomad_amr',
               'gnomad_fin',
               'gnomad_eas',
               'afr',
               'amr',
               'eas',
               'eur',
               'sas',
               'gwas_beta',
               'gwas_pvalue',
               'ls_snp_is_gwas_snp',
               'r2']

GTEX_COLUMNS = {'Adipose - Subcutaneous': None,
                'Adipose - Visceral (Omentum)': None,
                'Adrenal Gland': None,
                'Artery - Aorta': None,
                'Artery - Coronary': None,
                'Artery - Tibial': None,
                'Bladder': None,
                'Brain - Amygdala': None,
                'Brain - Anterior cingulate cortex (BA24)': None,
                'Brain - Caudate (basal ganglia)': None,
                'Brain - Cerebellar Hemisphere': None,
                'Brain - Cerebellum': None,
                'Brain - Cortex': None,
                'Brain - Frontal Cortex (BA9)': None,
                'Brain - Hippocampus': None,
                'Brain - Hypothalamus': None,
                'Brain - Nucleus accumbens (basal ganglia)': None,
                'Brain - Putamen (basal ganglia)': None,
                'Brain - Spinal cord (cervical c-1)': None,
                'Brain - Substantia nigra': None,
                'Breast - Mammary Tissue': None,
                'Cells - EBV-transformed lymphocytes': None,
                'Cells - Transformed fibroblasts': None,
                'Cervix - Ectocervix': None,
                'Cervix - Endocervix': None,
                'Colon - Sigmoid': None,
                'Colon - Transverse': None,
                'Esophagus - Gastroesophageal Junction': None,
                'Esophagus - Mucosa': None,
                'Esophagus - Muscularis': None,
                'Fallopian Tube': None,
                'Heart - Atrial Appendage': None,
                'Heart - Left Ventricle': None,
                'Kidney - Cortex': None,
                'Liver': None,
                'Lung': None,
                'Minor Salivary Gland': None,
                'Muscle - Skeletal': None,
                'Nerve - Tibial': None,
                'Ovary': None,
                'Pancreas': None,
                'Pituitary': None,
                'Prostate': None,
                'Skin - Not Sun Exposed (Suprapubic)': None,
                'Skin - Sun Exposed (Lower leg)': None,
                'Small Intestine - Terminal Ileum': None,
                'Spleen': None,
                'Stomach': None,
                'Testis': None,
                'Thyroid': None,
                'Uterus': None,
                'Vagina': None,
                'Whole Blood': None}

GTEX_DB = pd.read_csv(
    'databases/GTEx_Analysis_2016-01-15_v7_RNASeQCv1.1.8_gene_median_tpm.tsv', sep='\t')

GTEX_SIMILARITY_DB = pd.read_csv(
    'databases/UCSC_gtex_db.tsv', sep='\t', index_col=0)

BLASTP_SIMILARITY_DB = pd.read_csv(
    'databases/UCSC_blastp_db.tsv', sep='\t', index_col=0)

ATLAS_SIMILARITY_DB = pd.read_csv(
    'databases/UCSC_atlas_db.tsv', sep='\t', index_col=0)

GENE_INTERACTIONS_DB = pd.read_csv(
    'databases/UCSC_gene_interactions.tsv', sep='\t', index_col=0)

COL_DTYPES = {'afr': 'float16',
              'amr': 'float16',
              'eas': 'float16',
              'eur': 'float16',
              'sas': 'float16',
              'gnomad': 'float16',
              'gnomad_sas': 'float16',
              'gnomad_oth': 'float16',
              'gnomad_asj': 'float16',
              'gnomad_nfe': 'float16',
              'gnomad_afr': 'float16',
              'gnomad_amr': 'float16',
              'gnomad_fin': 'float16',
              'gnomad_eas': 'float16',
              'GTEx_Thyroid': 'float32',
              'GTEx_Testis': 'float32',
              'GTEx_Small_Intestine_Terminal_Ileum': 'float32',
              'GTEx_Nerve_Tibial': 'float32',
              'GTEx_Brain_Frontal_Cortex_BA9': 'float32',
              'GTEx_Skin_Not_Sun_Exposed_Suprapubic': 'float32',
              'GTEx_Vagina': 'float32',
              'GTEx_Whole_Blood': 'float32',
              'GTEx_Breast_Mammary_Tissue': 'float32',
              'GTEx_Ovary': 'float32',
              'GTEx_Adipose_Subcutaneous': 'float32',
              'GTEx_Adrenal_Gland': 'float32',
              'GTEx_Heart_Atrial_Appendage': 'float32',
              'GTEx_Stomach': 'float32',
              'GTEx_Brain_Caudate_basal_ganglia': 'float32',
              'GTEx_Colon_Transverse': 'float32',
              'GTEx_Brain_Cerebellum': 'float32',
              'GTEx_Cells_Transformed_fibroblasts': 'float32',
              'GTEx_Esophagus_Muscularis': 'float32',
              'GTEx_Liver': 'float32',
              'GTEx_Muscle_Skeletal': 'float32',
              'GTEx_Prostate': 'float32',
              'GTEx_Pancreas': 'float32',
              'GTEx_Brain_Hypothalamus': 'float32',
              'GTEx_Spleen': 'float32',
              'GTEx_Colon_Sigmoid': 'float32',
              'GTEx_Brain_Anterior_cingulate_cortex_BA24': 'float32',
              'GTEx_Esophagus_Gastroesophageal_Junction': 'float32',
              'GTEx_Brain_Hippocampus': 'float32',
              'GTEx_Brain_Cortex': 'float32',
              'GTEx_Heart_Left_Ventricle': 'float32',
              'GTEx_Artery_Tibial': 'float32',
              'GTEx_Uterus': 'float32',
              'GTEx_Pituitary': 'float32',
              'GTEx_Cells_EBV-transformed_lymphocytes': 'float32',
              'GTEx_Artery_Coronary': 'float32',
              'GTEx_Adipose_Visceral_Omentum': 'float32',
              'GTEx_Brain_Nucleus_accumbens_basal_ganglia': 'float32',
              'GTEx_Brain_Cerebellar_Hemisphere': 'float32',
              'GTEx_Esophagus_Mucosa': 'float32',
              'GTEx_Artery_Aorta': 'float32',
              'GTEx_Brain_Putamen_basal_ganglia': 'float32',
              'GTEx_Lung': 'float32',
              'GTEx_Skin_Sun_Exposed_Lower_leg': 'float32',
              'GTEx': 'float32',
              'VEP': 'uint8',
              'Nearest': 'uint8'}

PARAM_DIST_RF = {'max_depth': [5, 10, 30, 50, 100],
                 'max_features': ['auto', 'sqrt', 'log2', None],
                 'min_samples_split': [2, 5, 10],
                 'min_samples_leaf': [2, 3, 4]}


PARAM_DIST_SVC = {'gamma': [1, 0.1, 0.001, 0.0001],
                  'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000],
                  'kernel': ['linear', 'rbf']}

PARAM_DIST_LR = {"C": np.logspace(-5, 3, 50),
                 "penalty": ["l1", "l2"]}

PARAM_DIST_DT = {'max_depth': [5, 10, 15, 50, 100],
                 'min_samples_leaf': [1, 2, 3, 4],
                 'min_samples_split': [2, 3, 5, 10]}

PARAM_DIST_ADA = {"learning_rate": np.logspace(-6, 0, 15),
                  "algorithm": ['SAMME', 'SAMME.R']}

WEIGHTS = {1:90, 0:10}

UNDER_SAMPLE_COEF = 0.8 # Roughly balancing 

ADA_BASE = DecisionTreeClassifier(criterion='gini', class_weight=WEIGHTS)

MODELS = {
    
    'ADABoosting': [AdaBoostClassifier(base_estimator = ADA_BASE), PARAM_DIST_ADA],
    'Random Forest': [RandomForestClassifier(bootstrap=True, n_estimators=10, class_weight=WEIGHTS, oob_score=False), PARAM_DIST_RF],
    'Support Vector Machine': [SVC(probability=True, kernel ='rbf', C= 0.01, class_weight=WEIGHTS), PARAM_DIST_SVC],
    'Logistic regression': [LogisticRegression(solver='liblinear', C= 0.01, class_weight=WEIGHTS), PARAM_DIST_LR],
    'Decision Tree': [DecisionTreeClassifier(criterion='gini', class_weight=WEIGHTS), PARAM_DIST_DT]
}

