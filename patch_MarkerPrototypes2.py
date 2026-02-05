# Script em Python para processar um arquivo .cfg
# Regras:
# - Para cada node (struct.begin ... struct.end) de NÍVEL SUPERIOR:
# - Remover todos os parâmetros existentes
# - Inserir MarkerRevealDistance = 0.0
# - Inserir MarkerExploreDistance = 0.0
# - Inserir InitDiscoverState = EMarkerState::Hidden
# - Inserir MarkType = EMarkerType::None
# - Garantir que struct.begin contenha a chave {bpatch}
# - Remover todo conteúdo fora dos nodes (structs de nível superior)
# - PRESERVAR indentação original

import re

INPUT_FILE = "MarkerPrototypes.cfg"
OUTPUT_FILE = "MarkerPrototypes_patch_ImmersiveMap.cfg"

MARKER_REVEAL_KEY = "MarkerRevealDistance = 0.0"
MARKER_EXPLORE_KEY = "MarkerExploreDistance = 0.0"
MARKER_INIT_STATE_KEY = "InitDiscoverState = EMarkerState::Hidden"
MARKER_TYPE_KEY = "MarkType = EMarkerType::None"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

output = []
nesting_level = 0  # Contador de níveis de aninhamento
inside_top_level_struct = False  # Flag para saber se estamos dentro de um struct de nível superior
top_level_indent = ""
struct_end_indent = ""
param_indent = ""
current_struct_name = ""

for line in lines:
    stripped = line.strip()

    # Detecta início do node
    if "struct.begin" in stripped:
        nesting_level += 1

        if nesting_level == 1:  # Apenas structs de nível superior
            inside_top_level_struct = True
            # Extrai índice do node (ex: [0] : struct.begin)
            prefix = line.split("struct.begin")[0]
            current_struct_name = prefix.split(":")[0].strip()
            node_header = f"{prefix}struct.begin {{bpatch}}\n"
            output.append(node_header)
            top_level_indent = prefix
            struct_end_indent = prefix[: len(prefix) - len(prefix.lstrip())]
            param_indent = ""
            continue
        # Para structs aninhadas, não adiciona nada (remove completamente)
        continue

    # Detecta fim do node
    if stripped == "struct.end":
        nesting_level -= 1

        if nesting_level == 0:  # Fim de struct de nível superior
            marker_indent = param_indent or f"{top_level_indent}\t"
            output.append(f"{marker_indent}{MARKER_REVEAL_KEY}\n")
            output.append(f"{marker_indent}{MARKER_EXPLORE_KEY}\n")
            output.append(f"{marker_indent}{MARKER_INIT_STATE_KEY}\n")
            output.append(f"{marker_indent}{MARKER_TYPE_KEY}\n")
            output.append(f"{struct_end_indent}struct.end\n")
            inside_top_level_struct = False
            continue
        # Para structs aninhadas, não adiciona nada (remove completamente)
        continue

    # Dentro de structs de nível superior, ignora todos os parâmetros
    if nesting_level > 0:
        if nesting_level == 1 and not param_indent and stripped and stripped != "struct.end":
            param_indent = line[: len(line) - len(line.lstrip())]
        continue

    # Linhas fora de nodes são IGNORADAS (removidas)
    # Não adicionamos nada ao output para conteúdo fora de structs

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.writelines(output)

print("Arquivo processado com sucesso!")
print(f"Saída gerada em: {OUTPUT_FILE}")