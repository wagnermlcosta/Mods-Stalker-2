# RePak Tool by Saymonn README

## Introduction

This guide provides step-by-step instructions for using **RePak Tool by Saymonn (v2.0)** to manage `.pak` files for S.T.A.L.K.E.R. 2 Heart of Chornobyl. It covers unpacking, merging, and repacking addons.

---

## Requirements

To use the tool, you will need the following:

1. **Notepad++** - For editing files efficiently.
2. **Beyond Compare** - For merging files (optional, but recommended).
3. **RePak Tool by Trumank** - The main tool for handling `.pak` files.

---

## File Structure Overview

The RePak Tool v2.0 comes with the following structure:

```
repak-tool-by-saymonn-v2.0
│   1-unpack_pak.bat
│   2-repack_pak.bat
│   LICENSE-APACHE
│   LICENSE-MIT
│   README.md
│   repak.exe
│
├───1-input-pak-files
├───2-extracted-pak-files
├───3-repacked-pak-files
```

### Key Components:
1. **1-unpack_pak.bat**: Automates unpacking `.pak` files.
2. **2-repack_pak.bat**: Automates repacking folders into `.pak` files.
3. **repak.exe**: Core executable for unpacking and repacking.

---

## How to Use the Tool (detailed simple version)

### Step-by-Step:
1. **Unpack**: Place `my-addon.pak` in `1-input-pak-files` and run `1-unpack_pak.bat`.
2. **Edit**: Modify the unpacked files in `2-extracted-pak-files\my-addon`.
3. **Merge**: Use Beyond Compare to combine changes from multiple sources if needed.
4. **Repack**: Run `2-repack_pak.bat` to create a new `.pak` file.
5. **Install**: Move the repacked `.pak` file to `S.T.A.L.K.E.R. 2 Heart of Chornobyl\Stalker2\Content\Paks\~mods`.

---

## How to Use the Tool (detailed version)

### **1. Unpacking a `.pak` File**

1. Place your `.pak` files into the `1-input-pak-files` folder.
2. Run `1-unpack_pak.bat`.
3. Follow the on-screen instructions to select the `.pak` file(s) for unpacking.
4. The tool will create a folder for each unpacked `.pak` file in `2-extracted-pak-files`.

#### Manual Unpacking (Advanced Users):
- Open `1-unpack_pak.bat` in Notepad++ to edit paths or modify the script for specific needs.

---

### **2. Merging Files**

#### Using Beyond Compare:
1. Create two folders: `1` and `2`.
2. Place the files you want to merge into these folders.
3. Open Beyond Compare and choose the **Compare Texts** option.
4. Select the files from both folders to compare.
5. Use the arrows to merge differences.
6. Save the merged file by selecting it and pressing `Ctrl+S`.

#### Notes:
- Merging can also be done manually in Notepad++ by comparing files side-by-side.

---

### **3. Repacking a Folder**

1. Place your modified addon into the appropriate folder structure:
   - Example: `Stalker2\Content\GameLite\GameData\YourAddon`.
2. Move the entire folder into `2-extracted-pak-files`.
3. Run `2-repack_pak.bat`.
4. Follow the on-screen instructions to select the folder you want to repack.
5. The tool will create a `.pak` file in `3-repacked-pak-files`.

#### Manual Repacking (Advanced Users):
- Edit `2-repack_pak.bat` to customize paths or options for repacking.

---

## Troubleshooting

### Common Issues:
1. **Missing Folders**:
   - Ensure that `1-input-pak-files`, `2-extracted-pak-files`, and `3-repacked-pak-files` exist in the tool's directory.
2. **Invalid Selection**:
   - If prompted with an invalid selection error, double-check the input paths and follow the tool’s instructions.

### Tips:
- Always back up your files before making any modifications.
- Use Notepad++ for a clean and readable editing experience.

---

## License

The RePak Tool is distributed under the **MIT** and **Apache-2.0** licenses. See the LICENSE files for details.