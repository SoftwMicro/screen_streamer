import os
import glob

# Caminho para a pasta changes
CHANGES_DIR = os.path.join(os.path.dirname(__file__), '..', 'changes')

# Padrão para arquivos proposal*.md
pattern = os.path.join(CHANGES_DIR, 'proposta*.md')

# Lista todos os arquivos que correspondem ao padrão
files = glob.glob(pattern)

for file_path in files:
    try:
        os.remove(file_path)
        print(f"Removido: {file_path}")
    except Exception as e:
        print(f"Erro ao remover {file_path}: {e}")
