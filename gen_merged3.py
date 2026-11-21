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

# Assault Rifles - Part 1
content += "//------------------------------------------\n//-------------ASSAULT RIFLES---------------\n//------------------------------------------\n\n"
ars1 = [
    ("GunAK74_ST", {"FireInterval": "0.1", "RecoilParams": {"RecoilRadius": "125", "RecoilMaxPitch": "11.5", "RecoilPatternInterval": "0.1"}}),
    ("GunAKU_PP", {"FireInterval": "0.0923", "RecoilParams": {"RecoilRadius": "155", "RecoilMaxPitch": "13", "RecoilPatternInterval": "0.0923"}}),
    ("Gun_Silence_SMG_GS", {"FireInterval": "0.0857", "RecoilParams": {"RecoilRadius": "145", "RecoilMaxPitch": "12.5", "RecoilPatternInterval": "0.0857"}}),
    ("Gun_Spitfire_SMG_GS", {"FireInterval": "0.0833", "RecoilParams": {"RecoilRadius": "150", "RecoilMaxPitch": "12.8", "RecoilPatternInterval": "0.0833"}}),
    ("GunFora_ST", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "115", "RecoilMaxPitch": "11", "RecoilPatternInterval": "0.08"}}),
    ("GunDnipro_ST", {"FireInterval": "0.0909", "RecoilParams": {"RecoilRadius": "110", "RecoilMaxPitch": "10.8", "RecoilPatternInterval": "0.0909"}}),
    ("Gun_Combatant_AR_GS", {"FireInterval": "0.0968", "RecoilParams": {"RecoilRadius": "120", "RecoilMaxPitch": "11.2", "RecoilPatternInterval": "0.0968"}}),
    ("Gun_Drowned_AR_GS", {"FireInterval": "0.0952", "RecoilParams": {"RecoilRadius": "160", "RecoilMaxPitch": "13.2", "RecoilPatternInterval": "0.0952"}}),
    ("Gun_Sotnyk_AR_GS", {"FireInterval": "0.0882", "RecoilParams": {"RecoilRadius": "105", "RecoilMaxPitch": "10.5", "RecoilPatternInterval": "0.0882"}}),
    ("Gun_Lummox_AR_GS", {"FireInterval": "0.0923", "RecoilParams": {"RecoilRadius": "130", "RecoilMaxPitch": "11.8", "RecoilPatternInterval": "0.0923"}}),
    ("Gun_Stranger_AR", {"FireInterval": "0.0938", "RecoilParams": {"RecoilRadius": "112", "RecoilMaxPitch": "10.8", "RecoilPatternInterval": "0.0938"}}),
    ("Gun_S15_AR", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "115", "RecoilMaxPitch": "11", "RecoilPatternInterval": "0.08"}}),
    ("GunM16_ST", {"FireInterval": "0.071", "RecoilParams": {"RecoilRadius": "95", "RecoilMaxPitch": "10.5", "RecoilPatternInterval": "0.071"}}),
    ("Gun_Unknown_AR_GS", {"FireInterval": "0.067", "RecoilParams": {"RecoilRadius": "90", "RecoilMaxPitch": "10", "RecoilPatternInterval": "0.067"}}),
    ("Gun_SOFMOD_AR_GS", {"FireInterval": "0.067", "RecoilParams": {"RecoilRadius": "88", "RecoilMaxPitch": "10", "RecoilPatternInterval": "0.067"}}),
]
for a in ars1:
    name = a[0]
    props = a[1]
    content += weapon(name, props) + "\n\n"

with open(output_path, 'a', encoding='utf-8') as f:
    f.write(content)
print('Part 3a (Assault Rifles 1) appended successfully')
content = ""