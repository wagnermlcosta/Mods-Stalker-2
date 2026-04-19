INPUT_FILE = "WeaponGeneralSetupPrototypes.cfg"
OUTPUT_FILE = "WeaponGeneralSetupPrototypes_patch_Sway.cfg"

# Modos disponíveis:
# "attach"             -> CanHoldBreath = false + Scope + AimingEffects
# "weapon"             -> Apenas AimingEffects
# "attach_true"        -> Apenas CanHoldBreath = true
# "attach_breath_true" -> CanHoldBreath = true + Scope + AimingEffects
MODE = "weapon"


def build_template(indent, name):
    if MODE == "attach":
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

    elif MODE == "attach_true":
        return [
            f"{indent}{name} struct.begin {{bpatch}}\n",
            f"{indent}   CanHoldBreath = true\n",
            f"{indent}struct.end\n",
        ]

    elif MODE == "attach_breath_true":
        return [
            f"{indent}{name} struct.begin {{bpatch}}\n",
            f"{indent}   CanHoldBreath = true\n",
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

    else:
        raise ValueError(
            "MODE inválido! Use 'attach', 'weapon', 'attach_true' ou 'attach_breath_true'."
        )


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

output = []
nesting_level = 0

for line in lines:
    stripped = line.strip()

    if "struct.begin" in stripped:
        nesting_level += 1

        if nesting_level == 1:
            begin_index = line.index("struct.begin")
            prefix = line[:begin_index]

            # Mantém a indentação original perfeita e o nome do struct
            indent = prefix[:len(prefix) - len(prefix.lstrip())]
            name = prefix[len(indent):]

            output.extend(build_template(indent, name))

        continue

    if "struct.end" in stripped:
        nesting_level -= 1
        continue

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.writelines(output)

print("Arquivo processado com sucesso!")
print(f"Modo utilizado: {MODE}")
print(f"Saída gerada em: {OUTPUT_FILE}")