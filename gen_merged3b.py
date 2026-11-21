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

def nosway_only(name):
    return f"""{name} :  struct.begin {{bpatch}}
   AimingEffects : struct.begin {{bpatch}}
      PlayerOnlyEffects : struct.begin {{bpatch}}
         [*] = LessSwayX
         [*] = LessSwayY
         [*] = LessSwayTime
      struct.end
   struct.end
struct.end"""

content = ""

# Assault Rifles - Part 2
ars2 = [
    ("GunG37_ST", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "92", "RecoilMaxPitch": "10.2", "RecoilPatternInterval": "0.08"}}),
    ("GunG37V2_ST", {"FireInterval": "0.08", "FireTypes": ["EFireType::SemiAutomatic", "EFireType::Queue", "EFireType::Automatic"], "DefaultFireType": "EFireType::Automatic", "FireQueueCount": "3", "RecoilParams": {"RecoilRadius": "90", "RecoilMaxPitch": "10", "RecoilPatternInterval": "0.08"}}),
    ("GunKharod_ST", {"FireInterval": "0.0706", "RecoilParams": {"RecoilRadius": "100", "RecoilMaxPitch": "10.5", "RecoilPatternInterval": "0.0706"}}),
    ("Gun_Sharpshooter_AR_GS", {"FireInterval": "0.092", "RecoilParams": {"RecoilRadius": "380", "RecoilMaxPitch": "16", "RecoilPatternInterval": "0.092"}}),
    ("GunLavina_ST", {"FireInterval": "0.0667", "RecoilParams": {"RecoilRadius": "105", "RecoilMaxPitch": "9.5", "RecoilPatternInterval": "0.0667"}}),
    ("GunGrim_ST", {"FireInterval": "0.0857", "RecoilParams": {"RecoilRadius": "130", "RecoilMaxPitch": "11", "RecoilPatternInterval": "0.0857"}}),
    ("GunGvintar_ST", {"FireInterval": "0.075", "RecoilParams": {"RecoilRadius": "95", "RecoilMaxPitch": "9", "RecoilPatternInterval": "0.075"}}),
    ("Gun_Trophy_AR_GS", {"FireInterval": "0.0652", "RecoilParams": {"RecoilRadius": "98", "RecoilMaxPitch": "9", "RecoilPatternInterval": "0.0652"}}),
    ("Gun_Merc_AR_GS", {"FireInterval": "0.0732", "RecoilParams": {"RecoilRadius": "100", "RecoilMaxPitch": "9.2", "RecoilPatternInterval": "0.0732"}}),
    ("Gun_Decider_AR_GS", {"FireInterval": "0.0769", "RecoilParams": {"RecoilRadius": "115", "RecoilMaxPitch": "11", "RecoilPatternInterval": "0.0769"}}),
    ("GunArev_ST_GS", {"FireInterval": "0.0732", "RecoilParams": {"RecoilRadius": "90", "RecoilMaxPitch": "10", "RecoilPatternInterval": "0.0732"}}),
    ("GunArevPrecise_AR_GS", {"FireInterval": "0.067", "FireTypes": ["EFireType::SemiAutomatic", "EFireType::Queue", "EFireType::Automatic"], "DefaultFireType": "EFireType::Automatic", "FireQueueCount": "3", "RecoilParams": {"RecoilRadius": "85", "RecoilMaxPitch": "9.5", "RecoilPatternInterval": "0.067"}}),
]
for a in ars2:
    name = a[0]
    props = a[1]
    content += weapon(name, props) + "\n\n"

# NoSway only ARs
nosway_ars = ["GunAK74_Phantom_ST", "GunAK74_Strelok_ST"]
content += "// Exclusive to NoSway\n"
for n in nosway_ars:
    content += nosway_only(n) + "\n\n"

with open(output_path, 'a', encoding='utf-8') as f:
    f.write(content)
print('Part 3b (Assault Rifles 2) appended successfully')