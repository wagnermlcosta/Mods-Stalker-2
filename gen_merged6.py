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

# Shotguns
content += "//------------------------------------------\n//----------------SHOTGUNS------------------\n//------------------------------------------\n\n"
shotguns = [
    ("GunObrez_SG", {"RecoilParams": {"RecoilRadius": "1750", "RecoilMaxPitch": "28", "RecoilPatternInterval": "0.15"}, "DispersionParams": {"FirstShotDispersionRadius": "280"}}),
    ("GunTOZ_SG", {"RecoilParams": {"RecoilRadius": "1600", "RecoilMaxPitch": "27", "RecoilPatternInterval": "0.18"}, "DispersionParams": {"FirstShotDispersionRadius": "220"}}),
    ("GunM860_SG", {"RecoilParams": {"RecoilRadius": "1550", "RecoilMaxPitch": "27", "RecoilPatternInterval": "0.6"}, "DispersionParams": {"FirstShotDispersionRadius": "200"}}),
    ("Gun_Predator_SG_GS", {"RecoilParams": {"RecoilRadius": "1450", "RecoilMaxPitch": "26", "RecoilPatternInterval": "0.6"}, "DispersionParams": {"FirstShotDispersionRadius": "190"}}),
    ("GunSPSA_SG", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "1400", "RecoilMaxPitch": "26", "RecoilPatternInterval": "0.08"}, "DispersionParams": {"FirstShotDispersionRadius": "195"}}),
    ("GunD12_SG", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "1350", "RecoilMaxPitch": "25.5", "RecoilPatternInterval": "0.08"}, "DispersionParams": {"FirstShotDispersionRadius": "185"}}),
    ("GunRam2_SG", {"RecoilParams": {"RecoilRadius": "1580", "RecoilMaxPitch": "27", "RecoilPatternInterval": "0.5"}, "DispersionParams": {"FirstShotDispersionRadius": "210"}}),
    ("Gun_Sledgehammer_SG_GS", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "1300", "RecoilMaxPitch": "25", "RecoilPatternInterval": "0.08"}, "DispersionParams": {"FirstShotDispersionRadius": "175"}}),
    ("Gun_Texas_SG_GS", {"RecoilParams": {"RecoilRadius": "1480", "RecoilMaxPitch": "26", "RecoilPatternInterval": "0.6"}, "DispersionParams": {"FirstShotDispersionRadius": "195"}}),
    ("Gun_Reyka_SG", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "1400", "RecoilMaxPitch": "25.5", "RecoilPatternInterval": "0.08"}, "DispersionParams": {"FirstShotDispersionRadius": "170"}}, False),
]
for s in shotguns:
    name = s[0]
    props = s[1]
    aim = s[2] if len(s) > 2 else True
    content += weapon(name, props, aim) + "\n\n"

with open(output_path, 'a', encoding='utf-8') as f:
    f.write(content)
print('Part 6 (Shotguns) appended successfully')