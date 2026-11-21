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

# SMGs
content += "//------------------------------------------\n//-----------------SMGs---------------------\n//------------------------------------------\n\n"
smgs = [
    ("GunBucket_PP", {"FireInterval": "0.0706", "RecoilParams": {"RecoilRadius": "105", "RecoilMaxPitch": "8", "RecoilPatternInterval": "0.0706"}}),
    ("GunViper_PP", {"FireInterval": "0.075", "RecoilParams": {"RecoilRadius": "85", "RecoilMaxPitch": "7.5", "RecoilPatternInterval": "0.075"}}),
    ("GunZubr_PP", {"FireInterval": "0.0857", "RecoilParams": {"RecoilRadius": "95", "RecoilMaxPitch": "8", "RecoilPatternInterval": "0.0857"}}),
    ("GunIntegral_PP", {"FireInterval": "0.05", "RecoilParams": {"RecoilRadius": "75", "RecoilMaxPitch": "7", "RecoilPatternInterval": "0.05"}}),
    ("Gun_Shakh_SMG_GS", {"FireInterval": "0.0706", "RecoilParams": {"RecoilRadius": "80", "RecoilMaxPitch": "7.2", "RecoilPatternInterval": "0.0706"}}),
    ("Gun_Logarithm_SMG_GS", {"FireInterval": "0.05", "RecoilParams": {"RecoilRadius": "70", "RecoilMaxPitch": "6.8", "RecoilPatternInterval": "0.05"}}, False),
    ("Gun_Spitter_SMG_GS", {"FireInterval": "0.0632", "RecoilParams": {"RecoilRadius": "100", "RecoilMaxPitch": "8.2", "RecoilPatternInterval": "0.0632"}}),
    ("Gun_RatKiller_SMG_GS", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "88", "RecoilMaxPitch": "7.5", "RecoilPatternInterval": "0.08"}}),
    ("Gun_GStreet_HG_GS", {"FireInterval": "0.052", "RecoilParams": {"RecoilRadius": "135", "RecoilMaxPitch": "9.0", "RecoilPatternInterval": "0.052"}}),
    ("GunM10_HG", {"FireInterval": "0.0571", "RecoilParams": {"RecoilRadius": "190", "RecoilMaxPitch": "11", "RecoilPatternInterval": "0.0571"}}),
    ("GunFora230_PP_GS", {"FireInterval": "0.075", "RecoilParams": {"RecoilRadius": "78", "RecoilMaxPitch": "7", "RecoilPatternInterval": "0.075"}}),
]
for s in smgs:
    name = s[0]
    props = s[1]
    aim = s[2] if len(s) > 2 else True
    content += weapon(name, props, aim) + "\n\n"

# NoSway only SMGs
nosway_smgs = ["GunAKU_PP", "Gun_Silence_SMG_GS", "Gun_Spitfire_SMG_GS"]
content += "// Exclusive to NoSway\n"
for n in nosway_smgs:
    content += nosway_only(n) + "\n\n"

with open(output_path, 'a', encoding='utf-8') as f:
    f.write(content)
print('Part 2 (SMGs) appended successfully')