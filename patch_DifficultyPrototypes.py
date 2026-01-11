# Script em Python para processar um arquivo .cfg
# Regras:
# - Para TODOS os structs (nível superior e aninhados):
# - Adicionar {bpatch} ao struct.begin
# - Remover todos os parâmetros existentes
# - Remover todo conteúdo fora dos nodes (structs)
# - PRESERVAR indentação original

INPUT_FILE = "DifficultyPrototypes.cfg"
OUTPUT_FILE = "DifficultyPrototypes_patch_Damage.cfg"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

output = []
nesting_level = 0  # Contador de níveis de aninhamento
inside_struct = False  # Flag para saber se estamos dentro de qualquer struct

for line in lines:
    # Preserva espaços/tabs iniciais, remove apenas espaços do final
    stripped = line.rstrip()
    
    # Detecta início do node
    if "struct.begin" in stripped:
        nesting_level += 1
        inside_struct = True
        
        # Para TODOS os structs, adicionar {bpatch}
        # Extrai indentação exata da linha original
        # Encontra a posição de "struct.begin" na linha
        begin_pos = line.find("struct.begin")
        if begin_pos != -1:
            # Pega a indentação (tudo antes de "struct.begin")
            indent = line[:begin_pos]
            # Reconstrói a linha com {bpatch} mantendo a indentação exata
            node_header = f"{indent}struct.begin {{bpatch}}\n"
            output.append(node_header)
        else:
            # Fallback: usa a linha original e adiciona {bpatch}
            output.append(line.rstrip() + " {bpatch}\n")
        
        continue

    # Detecta fim do node
    if stripped.endswith("struct.end"):
        if nesting_level > 0:
            # Mantém a linha exata como está (com indentação original)
            output.append(line)
            inside_struct = False
        
        nesting_level -= 1
        continue

    # Dentro de qualquer struct, ignora todos os parâmetros existentes
    if inside_struct:
        continue

    # Linhas fora de structs são IGNORADAS (removidas)
    # Não adicionamos nada ao output para conteúdo fora de structs

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.writelines(output)

print("Arquivo processado com sucesso!")
print(f"Saída gerada em: {OUTPUT_FILE}")