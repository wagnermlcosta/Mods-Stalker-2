# Script em Python para processar um arquivo .cfg
# Regras:
# - Para TODOS os structs (nível superior e aninhados):
# - Adicionar {bpatch} ao struct.begin
# - Remover todos os parâmetros existentes
# - Remover todo conteúdo fora dos nodes (structs)
# - PRESERVAR indentação original
# - Para nodes de NÍVEL SUPERIOR: adicionar ArmorPenetrationPlayer e ArmorPenetrationNPC com valor 6

INPUT_FILE = "ExplosionPrototypes.cfg"
OUTPUT_FILE = "ExplosionPrototypes_patch_GlassCannon.cfg"

# ========== PRIMEIRA PASSAGEM: EXTRAIR VALORES ORIGINAIS ==========
armor_values = {}  # Dicionário para armazenar valores originais de ArmorPenetration por nome de node

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lines_first_pass = f.readlines()

current_node_name = None
current_armor_player = 4  # valor padrão
current_armor_npc = 4     # valor padrão
nesting_level_first = 0

for i, line in enumerate(lines_first_pass):
    stripped = line.rstrip()
    
    if "struct.begin" in stripped:
        if nesting_level_first == 0:
            # Extrair nome do node da linha atual (antes do ':')
            if ':' in line:
                node_name = line.split(':')[0].strip()
                current_node_name = node_name
                current_armor_player = 4  # reset para padrão
                current_armor_npc = 4
        nesting_level_first += 1
        continue
    
    if stripped.endswith("struct.end"):
        nesting_level_first -= 1
        if nesting_level_first == 0 and current_node_name:
            # Salvar valores para este node
            armor_values[current_node_name] = {
                'player': current_armor_player,
                'npc': current_armor_npc
            }
            current_node_name = None
        continue
    
    if current_node_name and nesting_level_first == 1:
        # Procurar pelos valores de ArmorPenetration
        if "ArmorPenetrationPlayer =" in stripped:
            current_armor_player = int(stripped.split("=")[1].strip().rstrip('.'))
        elif "ArmorPenetrationNPC =" in stripped:
            current_armor_npc = int(stripped.split("=")[1].strip().rstrip('.'))

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
            if is_top_level and current_node_name_pass2 and current_node_name_pass2 in armor_values:
                # Detectar indentação padrão (3 espaços baseado no arquivo original)
                param_indent = "   "
                
                # Definir valores fixos como 6
                armor_player = 6
                armor_npc = 6
                
                # Adicionar os parâmetros com indentação correta
                output.append(f"{param_indent}ArmorPenetrationPlayer = {armor_player}.\n")
                output.append(f"{param_indent}ArmorPenetrationNPC = {armor_npc}.\n")
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
print(f"\nValores de ArmorPenetration definidos como 6 para todos os nodes de nível superior:")
for sid in armor_values.keys():
    print(f"  {sid}: Player=6, NPC=6")