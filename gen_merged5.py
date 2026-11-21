output_path = r'c:\Users\wagne\Documents\Criacao de Mods Stalker 2\Mods Stalker 2\Merged_Mod\Stalker2\Content\GameLite\GameData\WeaponData\WeaponGeneralSetupPrototypes.cfg'

def weapon(name, props, aim=True):
    lines = [f"{name} : struct.begin {{bpatch}}"]
    for k, v in props.items():
        if isinstance(v, dict):
            lines.append(f"   {k} : struct.begin {{bpatch}}")
            for k2, v2 in v.items():
                if isinstance(v2, dict):
                    lines.append(f"      {k2} : struct.begin {{bpatch}}")
                    for k3, v3 in v2.items():
                        lines.append(f"         {k3} = {v3}")
                    lines.append(f"      struct.end")
                else:
                    lines.append(f"      {k2} = {v2}")
            lines.append(f"   struct.end")
        elif isinstance(v, list):
            lines.append(f"   {k} : struct.begin {{bpatch}}")
            for i, item in enumerate(v):
                lines.append(f"      [{i}] = {item}")
            lines.append(f"   struct.end")
        else:
            lines.append(f"   {k} = {v}")
    if aim:
        lines.append(f"   AimingEffects : struct.begin {{bpatch}}")
        lines.append(f"      PlayerOnlyEffects : struct.begin {{bpatch}}")
        lines.append(f"         [*] = LessSwayX")
        lines.append(f"         [*] = LessSwayY")
        lines.append(f"         [*] = LessSwayTime")
        lines.append(f"      struct.end")
        lines.append(f"   struct.end")
    lines.append(f"struct.end")
    return "\n".join(lines)

content = ""

# LMGs
content += "//------------------------------------------\n//-----------------LMGS---------------------\n//------------------------------------------\n\n"
lmgs = [
    ("GunPKP_MG", {"FireInterval": "0.0923", "RecoilParams": {"RecoilRadius": "320", "RecoilMaxPitch": "15", "RecoilPatternInterval": "0.0923"}}),
    ("Gun_Tank_MG_GS", {"FireInterval": "0.0833", "RecoilParams": {"RecoilRadius": "290", "RecoilMaxPitch": "14", "RecoilPatternInterval": "0.0833"}}),
    ("GunPKP_Korshunov_MG_GS", {"FireInterval": "0.0882", "RecoilParams": {"RecoilRadius": "310", "RecoilMaxPitch": "14.5", "RecoilPatternInterval": "0.0882"}}),
]
for l in lmgs:
    name = l[0]
    props = l[1]
    content += weapon(name, props) + "\n\n"

with open(output_path, 'a', encoding='utf-8') as f:
    f.write(content)
print('Part 5 (LMGs) appended successfully')