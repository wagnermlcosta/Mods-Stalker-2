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

# Special / Exotic
content += "//------------------------------------------\n//-------------SPECIAL / EXOTIC-------------\n//------------------------------------------\n\n"
specials = [
    ("GunGauss_SP", {"FireInterval": "1.5", "RecoilParams": {"RecoilRadius": "80", "RecoilMaxPitch": "6", "RecoilPatternInterval": "1.5"}}),
    ("GunGauss_Scar_SP_GS", {"FireInterval": "1.0", "RecoilParams": {"RecoilRadius": "90", "RecoilMaxPitch": "7", "RecoilPatternInterval": "1.0"}}, False),
    ("GunRpg7_GL", {"FireInterval": "3.0", "RecoilParams": {"RecoilRadius": "900", "RecoilMaxPitch": "22", "RecoilPatternInterval": "3.0"}}),
]
for s in specials:
    name = s[0]
    props = s[1]
    aim = s[2] if len(s) > 2 else True
    content += weapon(name, props, aim) + "\n\n"

# NoSway only specials
nosway_specials = ["UA_GLaunch_Weapon_Data_Ru", "UA_GLaunch_Weapon_Data_En", "EN_BuckLaunch_Data"]
content += "// Exclusive to NoSway\n"
for n in nosway_specials:
    content += nosway_only(n) + "\n\n"

with open(output_path, 'a', encoding='utf-8') as f:
    f.write(content)
print('Part 7 (Special/Exotic) appended successfully')