# Script em Python para processar um arquivo .cfg
# Regras:
# - Para TODOS os structs (superiores e aninhados):
# - Preservar o nome do struct (antes do :)
# - Adicionar {bpatch} ao struct.begin
# - Remover TODOS os parâmetros existentes
# - Para structs superiores (nível 1): adicionar DamagePlayer e DamageNPC com o maior valor
# - Para ExplosionM203, usar valores do ExplosionVOG25 (80 e 300)
# - PRESERVAR indentação original

INPUT_FILE = "ExplosionPrototypes.cfg"
OUTPUT_FILE = "ExplosionPrototypes_patch_GlassCannon.cfg"

# Valores específicos para o m203 (do vog25)
M203_DAMAGE_PLAYER = 300
M203_DAMAGE_NPC = 300

def extract_value(line):
    """Extrai o valor numérico de uma linha 'Parametro = valor.'"""
    if "=" in line:
        parts = line.split("=")
        if len(parts) >= 2:
            value_str = parts[1].strip().rstrip(".")
            try:
                return int(value_str)
            except:
                return None
    return None

def get_indent(line):
    """Extrai a indentação exata de uma linha."""
    return line[:len(line) - len(line.lstrip())]

def extract_struct_name(line):
    """Extrai o nome do struct da linha (parte antes do ':')"""
    if ":" in line and "struct.begin" in line:
        parts = line.split(":")
        return parts[0].strip()
    return None

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Primeiro, processamos tudo e armazenamos as informações
struct_info = {}  # Armazena informações de cada struct superior
current_struct = None
current_level = 0
struct_stack = []

for line in lines:
    stripped = line.rstrip()
    indent = get_indent(line)
    
    # Detecta início de um struct
    if "struct.begin" in stripped:
        struct_name = extract_struct_name(stripped)
        
        if current_level == 0 and struct_name:
            current_struct = struct_name
            struct_info[struct_name] = {
                'indent': indent,
                'damage_player': None,
                'damage_npc': None,
                'has_params': False
            }
        
        struct_stack.append(struct_name)
        current_level += 1
        continue
    
    # Detecta fim de um struct
    if stripped.endswith("struct.end"):
        if struct_stack:
            struct_stack.pop()
            current_level -= 1
            if current_level == 0:
                current_struct = None
        continue
    
    # Dentro de struct superior - extrair valores
    if current_level == 1 and current_struct:
        if "DamagePlayer" in stripped and "=" in stripped:
            struct_info[current_struct]['damage_player'] = extract_value(stripped)
            struct_info[current_struct]['has_params'] = True
            continue
        
        if "DamageNPC" in stripped and "=" in stripped:
            struct_info[current_struct]['damage_npc'] = extract_value(stripped)
            struct_info[current_struct]['has_params'] = True
            continue
        
        # Ignora outros parâmetros
        continue
    
    # Dentro de structs aninhados - ignora tudo
    if current_level > 1:
        continue

# Agora processamos novamente para gerar o output correto
output = []
struct_stack = []
current_level = 0
current_struct = None

for line in lines:
    stripped = line.rstrip()
    indent = get_indent(line)
    
    # Detecta início de um struct
    if "struct.begin" in stripped:
        struct_name = extract_struct_name(stripped)
        
        if current_level == 0 and struct_name:
            current_struct = struct_name
        
        struct_stack.append(struct_name)
        current_level += 1
        
        # Adiciona struct.begin com {bpatch}
        if struct_name:
            output.append(f"{indent}{struct_name} : struct.begin {{bpatch}}\n")
        else:
            output.append(f"{indent}struct.begin {{bpatch}}\n")
        
        # Se for struct superior, adiciona parâmetros imediatamente
        if current_level == 1 and struct_name:
            if struct_name == "ExplosionM203":
                output.append(f"{indent}   DamagePlayer = {M203_DAMAGE_PLAYER}.\n")
                output.append(f"{indent}   DamageNPC = {M203_DAMAGE_NPC}.\n")
            elif struct_name in struct_info and struct_info[struct_name]['has_params']:
                damage_value = max(
                    struct_info[struct_name]['damage_player'] if struct_info[struct_name]['damage_player'] is not None else 0,
                    struct_info[struct_name]['damage_npc'] if struct_info[struct_name]['damage_npc'] is not None else 0
                )
                output.append(f"{indent}   DamagePlayer = {damage_value}.\n")
                output.append(f"{indent}   DamageNPC = {damage_value}.\n")
        
        continue
    
    # Detecta fim de um struct
    if stripped.endswith("struct.end"):
        if struct_stack:
            struct_stack.pop()
            current_level -= 1
            if current_level == 0:
                current_struct = None
        
        output.append(f"{indent}struct.end\n")
        continue
    
    # Dentro de structs superiores - ignora parâmetros originais
    if current_level == 1 and struct_stack and struct_stack[-1] in struct_info:
        if "DamagePlayer" in stripped or "DamageNPC" in stripped:
            continue  # Ignora parâmetros originais
        # Ignora outros parâmetros também
        if "=" in stripped:
            continue
    
    # Dentro de structs aninhados - ignora tudo
    if current_level > 1:
        continue
    
    # Fora de structs - mantém linhas vazias ou comentários
    if current_level == 0:
        if stripped.strip() == "" or stripped.strip().startswith("#"):
            output.append(line)

# Escreve o arquivo de saída
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.writelines(output)

print("Arquivo processado com sucesso!")
print(f"Saída gerada em: {OUTPUT_FILE}")