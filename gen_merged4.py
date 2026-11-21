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

# DMRs / Snipers
content += "//------------------------------------------\n//--------------DMRs / SNIPERS--------------\n// Semi-auto = same as pistols (0.08)\n// Bolt-action = no FireInterval\n//------------------------------------------\n\n"
dmrs = [
    ("GunThreeLine_SP_GS", {"RecoilParams": {"RecoilRadius": "780", "RecoilMaxPitch": "20", "RecoilPatternInterval": "0.6"}}),
    ("GunGonta_SP_GS", {"RecoilParams": {"RecoilRadius": "750", "RecoilMaxPitch": "19.5", "RecoilPatternInterval": "0.6"}}),
    ("GunSVDM_SP", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "620", "RecoilMaxPitch": "18", "RecoilPatternInterval": "0.08"}}),
    ("Gun_Lynx_SR_GS", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "590", "RecoilMaxPitch": "17.5", "RecoilPatternInterval": "0.08"}}),
    ("GunSVU_SP", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "640", "RecoilMaxPitch": "18.5", "RecoilPatternInterval": "0.08"}}),
    ("Gun_Whip_SR_GS", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "600", "RecoilMaxPitch": "18", "RecoilPatternInterval": "0.08"}}),
    ("GunMark_SP", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "480", "RecoilMaxPitch": "17", "RecoilPatternInterval": "0.08"}}),
    ("Gun_Partner_SR_GS", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "460", "RecoilMaxPitch": "16.5", "RecoilPatternInterval": "0.08"}}),
    ("GunM701_SP", {"RecoilParams": {"RecoilRadius": "720", "RecoilMaxPitch": "19", "RecoilPatternInterval": "0.6"}}),
    ("Gun_Cavalier_SR_GS", {"RecoilParams": {"RecoilRadius": "690", "RecoilMaxPitch": "18.5", "RecoilPatternInterval": "0.6"}}),
    ("GunGP3A_DMR_GS", {"FireInterval": "0.1", "RecoilParams": {"RecoilRadius": "500", "RecoilMaxPitch": "17", "RecoilPatternInterval": "0.1"}}),
    ("GunSKP_DMR_GS", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "520", "RecoilMaxPitch": "17.2", "RecoilPatternInterval": "0.08"}}),
]
for d in dmrs:
    name = d[0]
    props = d[1]
    content += weapon(name, props) + "\n\n"

# NoSway only
nosway_dmrs = ["GunGauss_SP", "GunGauss_Scar_SP"]
content += "// Exclusive to NoSway\n"
for n in nosway_dmrs:
    content += nosway_only(n) + "\n\n"

with open(output_path, 'a', encoding='utf-8') as f:
    f.write(content)
print('Part 4 (DMRs/Snipers) appended successfully')