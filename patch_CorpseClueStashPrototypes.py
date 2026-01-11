# Script em Python para processar um arquivo .cfg
# Regras:
# - Para cada node (struct.begin ... struct.end) de NÍVEL SUPERIOR:
# - Remover todos os parâmetros existentes
# - Manter apenas BaseSpawnChance = 1.0
# - Se não existir, inserir
# - Garantir que struct.begin contenha a chave {bpatch}
# - Remover todo conteúdo fora dos nodes (structs de nível superior)

import re

INPUT_FILE = "CorpseClueStashPrototypes.cfg"
OUTPUT_FILE = "CorpseClueStashPrototypes_patch_BaseSpawnChance.cfg"

MARKER_LINE = "\tBaseSpawnChance = 1.0"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

output = []
nesting_level = 0  # Contador de níveis de aninhamento
inside_top_level_struct = False  # Flag para saber se estamos dentro de um struct de nível superior

for line in lines:
    stripped = line.strip()

    # Detecta início do node
    if "struct.begin" in stripped:
        nesting_level += 1

        if nesting_level == 1:  # Apenas structs de nível superior
            inside_top_level_struct = True
            # Extrai índice do node (ex: [0] : struct.begin)
            prefix = line.split("struct.begin")[0]
            node_header = f"{prefix}struct.begin {{bpatch}}\n"
            output.append(node_header)
            continue
        # Para structs aninhadas, não adiciona nada (remove completamente)
        continue

    # Detecta fim do node
    if stripped == "struct.end":
        nesting_level -= 1

        if nesting_level == 0:  # Fim de struct de nível superior
            output.append(f"{MARKER_LINE}\n")
            output.append("struct.end\n")
            inside_top_level_struct = False
            continue
        # Para structs aninhadas, não adiciona nada (remove completamente)
        continue

    # Dentro de structs de nível superior, ignora todos os parâmetros
    if nesting_level > 0:
        continue

    # Linhas fora de nodes são IGNORADAS (removidas)
    # Não adicionamos nada ao output para conteúdo fora de structs

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.writelines(output)

print("Arquivo processado com sucesso!")
print(f"Saída gerada em: {OUTPUT_FILE}")