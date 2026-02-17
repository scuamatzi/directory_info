# Directory Info

## This script shows this info:
- Total files inside directory
- Total files inside each subfolder
- Top 10 file extensions in directory (the extension and how many)
- Total size of directory
- Total size of each subdirectory
- [Optional] write down tree command for diretory with 3 levels

## Usage

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
python3 get_full_directory_info.py
```

## Input

```
============================================================
DIRECTORY INFORMATION
============================================================

Enter full path to analyze: /mnt/common/office

Do you need tree command info? (y/n) y

Enter filename for tree command results: office
```

## Output (shortend)
```
------------------------------------------------------------
FILE COUNTS
------------------------------------------------------------

Number of files in directory: 27677

Number of files in each subfolder:
  0102346859-FACT/: 2 files
  NAS_HDEs/: 38 files
  aleon/: 9068 files
  ansible/: 169 files
.
.
.

Top 10 extension files 
   1. .pcm               9,015 files (32.6%)
   2. .php               6,653 files (24.0%)
   3. .js                2,060 files (7.4%)
   4. .jpg               1,825 files (6.6%)
.
.
.

------------------------------------------------------------
DIRECTORY SIZES
------------------------------------------------------------

Size of directory: 2.07 GB

Size of each subfolder:
  0102346859-FACT/: 1.12 MB
  NAS_HDEs/: 3.67 MB
  aleon/: 835.20 MB
  ansible/: 1.17 MB
.
.
.

------------------------------------------------------------
TREE STRUCTURE OUTPUT
------------------------------------------------------------

Generating tree command output...

Level 1:
Tree output saved to : office_L1_20260217.txt

Level 2:
Tree output saved to : office_L2_20260217.txt

Level 3:
Tree output saved to : office_L3_20260217.txt

============================================================
SUMMARY
============================================================
• Directory analyzed: /mnt/common/office
• Files in directory: 27677
• Total size: 2.07 GB
• Tree outputs generated:
 - Leveln 1: office_L1_20260217.txt
 - Leveln 2: office_L2_20260217.txt
 - Leveln 3: office_L3_20260217.txt

Script completed successfully

```

