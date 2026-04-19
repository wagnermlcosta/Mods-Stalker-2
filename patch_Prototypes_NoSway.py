INPUT_FILE = "WeaponGeneralSetupPrototypes.cfg"
OUTPUT_FILE = "WeaponGeneralSetupPrototypes_patch_NoSway.cfg"

# Escolha o modo:
# "scope"  -> primeiro modelo (com CanHoldBreath + Scope)
# "weapon" -> segundo modelo (apenas AimingEffects)
MODE = "weapon"


def build_template(indent, name):
    if MODE == "scope":
        return [
            f"{indent}{name} struct.begin {{bpatch}}\n",
            f"{indent}   CanHoldBreath = false\n",
            f"{indent}   Scope : struct.begin {{bpatch}}\n",
            f"{indent}      AimingEffects : struct.begin {{bpatch}}\n",
            f"{indent}         PlayerOnlyEffects : struct.begin {{bpatch}}\n",
            f"{indent}            [*] = LessSwayX\n",
            f"{indent}            [*] = LessSwayY\n",
            f"{indent}            [*] = LessSwayTime\n",
            f"{indent}         struct.end\n",
            f"{indent}      struct.end\n",
            f"{indent}   struct.end\n",
            f"{indent}struct.end\n",
        ]

    elif MODE == "weapon":
        return [
            f"{indent}{name} struct.begin {{bpatch}}\n",
            f"{indent}   AimingEffects : struct.begin {{bpatch}}\n",
            f"{indent}      PlayerOnlyEffects : struct.begin {{bpatch}}\n",
            f"{indent}         [*] = LessSwayX\n",
            f"{indent}         [*] = LessSwayY\n",
            f"{indent}         [*] = LessSwayTime\n",
            f"{indent}      struct.end\n",
            f"{indent}   struct.end\n",
            f"{indent}struct.end\n",
        ]

    else:
        raise ValueError("MODE inválido! Use 'scope' ou 'weapon'.")


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

output = []
nesting_level = 0

for line in lines:
    stripped = line.strip()

    # Início de struct
    if "struct.begin" in stripped:
        nesting_level += 1

        if nesting_level == 1:
            begin_index = line.index("struct.begin")
            prefix = line[:begin_index]

            # Preserva indentação real (tabs/espaços)
            indent = prefix[:len(prefix) - len(prefix.lstrip())]
            name = prefix.strip()

            output.extend(build_template(indent, name))

        continue

    # Fim de struct
    if stripped.endswith("struct.end"):
        nesting_level -= 1
        continue

# Salva saída
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.writelines(output)

print("Arquivo processado com sucesso!")
print(f"Modo utilizado: {MODE}")
print(f"Saída: {OUTPUT_FILE}")