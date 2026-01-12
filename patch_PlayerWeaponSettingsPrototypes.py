# Script em Python para processar um arquivo .cfg
# Regras:
# - Para TODOS os structs (nível superior e aninhados):
# - Adicionar {bpatch} ao struct.begin
# - Remover todos os parâmetros existentes
# - Remover todo conteúdo fora dos nodes (structs)
# - PRESERVAR indentação original
# - Para nodes de NÍVEL SUPERIOR: adicionar ArmorPiercing e CoverPiercing com valor igual a 4

INPUT_FILE = "PlayerWeaponSettingsPrototypes.cfg"
OUTPUT_FILE = "PlayerWeaponSettingsPrototypes_patch_GlassCannon.cfg"

# ========== PRIMEIRA PASSAGEM: COLETAR NOMES DE NODES DE NÍVEL SUPERIOR ==========
top_level_nodes = []  # Lista para armazenar nomes de nodes de nível superior

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lines_first_pass = f.readlines()

nesting_level_first = 0

for i, line in enumerate(lines_first_pass):
    stripped = line.rstrip()
    
    if "struct.begin" in stripped:
        if nesting_level_first == 0:
            # Extrair nome do node da linha atual (antes do ':')
            if ':' in line:
                node_name = line.split(':')[0].strip()
                top_level_nodes.append(node_name)
        nesting_level_first += 1
        continue
    
    if stripped.endswith("struct.end"):
        nesting_level_first -= 1
        continue

# ========== SEGUNDA PASSAGEM: PROCESSAR E ADICIONAR PARÂMETROS ==========
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

output = []
nesting_level = 0  # Contador de níveis de aninhamento
inside_struct = False  # Flag para saber se estamos dentro de qualquer struct
current_node_name_pass2 = None  # Nome do node atual
params_added = False  # Flag para garantir que parâmetros sejam adicionados apenas uma vez

for line in lines:
    # Preserva espaços/tabs iniciais, remove apenas espaços do final
    stripped = line.rstrip()
    
    # Detecta início do node
    if "struct.begin" in stripped:
        is_top_level = (nesting_level == 0)
        nesting_level += 1
        inside_struct = True
        
        # Se for nível superior, extrair nome do node
        if is_top_level and ':' in line:
            current_node_name_pass2 = line.split(':')[0].strip()
            params_added = False
        
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
            
            # Se for nível superior e temos nome do node, adicionar parâmetros agora
            if is_top_level and current_node_name_pass2:
                # Detectar indentação padrão (3 espaços baseado no arquivo original)
                param_indent = "   "
                
                # Usar valor fixo 4.0 para ambos os parâmetros
                armor_piercing = 4.0
                cover_piercing = 4.0
                
                # Adicionar os parâmetros com indentação correta
                output.append(f"{param_indent}ArmorPiercing = {armor_piercing}\n")
                output.append(f"{param_indent}CoverPiercing = {cover_piercing}\n")
                params_added = True
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
        
        # Reset quando sair de um node de nível superior
        if nesting_level == 0:
            current_node_name_pass2 = None
            params_added = False
        
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
print(f"\nValores de ArmorPiercing e CoverPiercing adicionados aos nodes de nível superior:")
print(f"  Todos os {len(top_level_nodes)} nodes de nível superior receberam:")
print(f"  ArmorPiercing = 4.0")
print(f"  CoverPiercing = 4.0")