import os

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

def template(name):
    return f"""{name} :  struct.begin {{bpatch}}
   AimingEffects : struct.begin {{bpatch}}
      PlayerOnlyEffects : struct.begin {{bpatch}}
         [*] = LessSwayX
         [*] = LessSwayY
         [*] = LessSwayTime
      struct.end
   struct.end
struct.end"""

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

content = "// ============================================================\n"
content += "// STALKER 2 - WeaponGeneralSetupPrototypes.cfg\n"
content += "// Realistic Recoil + Tighter Shotgun Choke\n"
content += "// Semi-auto DMRs/Snipers = same fire rate as pistols (0.08)\n"
content += "// Merged with NoSway: Added AimingEffects (LessSwayX, LessSwayY, LessSwayTime)\n"
content += "// ============================================================\n\n"

# Templates
templates = ["TemplateWeapon", "TemplatePistol", "TemplateSMG", "TemplateMAC", "TemplateRifle", 
             "TemplateRifleSingleFire", "TemplateMG", "TemplateShotgun", "TemplateDMR", 
             "TemplateSniper", "TemplateGLaunch", "MeleeStub", "Default"]
content += "//------------------------------------------\n//--------------TEMPLATES (NoSway)----------\n//------------------------------------------\n\n"
for t in templates:
    content += template(t) + "\n\n"

# Pistols
content += "//------------------------------------------\n//--------------PISTOLS---------------------\n//------------------------------------------\n\n"
pistols = [
    ("GunPM_HG", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "210", "RecoilMaxPitch": "9", "RecoilPatternInterval": "0.08"}}),
    ("Gun_SkifGun_HG", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "195", "RecoilMaxPitch": "8.5", "RecoilPatternInterval": "0.08"}}, False),
    ("GunAPB_HG", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "160", "RecoilMaxPitch": "8", "RecoilPatternInterval": "0.08"}}),
    ("Gun_ProjectY_HG_GS", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "185", "RecoilMaxPitch": "8.5", "RecoilPatternInterval": "0.08"}}, False),
    ("GunUDP_HG", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "280", "RecoilMaxPitch": "11", "RecoilPatternInterval": "0.08"}}),
    ("GunKora_HG", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "300", "RecoilMaxPitch": "11.5", "RecoilPatternInterval": "0.08"}}),
    ("GunNightStalker_HG", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "220", "RecoilMaxPitch": "9", "RecoilPatternInterval": "0.08"}}),
    ("Gun_Deadeye_HG", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "260", "RecoilMaxPitch": "10.5", "RecoilPatternInterval": "0.08"}}, False),
    ("Gun_Krivenko_HG_GS", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "200", "RecoilMaxPitch": "9", "RecoilPatternInterval": "0.08"}}),
    ("Gun_Encourage_HG_GS", {"FireInterval": "0.08", "RecoilParams": {"RecoilRadius": "270", "RecoilMaxPitch": "11", "RecoilPatternInterval": "0.08"}}),
    ("GunRhino_HG", {"RecoilParams": {"RecoilRadius": "520", "RecoilMaxPitch": "14", "RecoilPatternInterval": "0.15"}}),
]
for p in pistols:
    name = p[0]
    props = p[1]
    aim = p[2] if len(p) > 2 else True
    content += weapon(name, props, aim) + "\n\n"

# NoSway only pistols
nosway_pistols = ["GunUDP_Deadeye_HG", "Gun_Star_HG_GS", "Gun_Kaimanov_HG_GS"]
content += "// Exclusive to NoSway\n"
for n in nosway_pistols:
    content += nosway_only(n) + "\n\n"

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Part 1 (templates + pistols) written successfully')