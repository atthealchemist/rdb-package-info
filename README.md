# RDB Comparison

## Installation
No required. Just launch `rdb-comparison.sh`

## Usage

```bash
$ ./rdb-comparison.sh 
[174091 packages] Fetching branch (p10) from web...
Ok!
[173482 packages] Fetching branch (sisyphus) from web...
Ok!
Performed next comparisons: 
1. Packages exists in p10 only -> 47772 pkgs
2. Packages exists in sisyphus only -> 48381 pkgs
3. Packages with greatest version in sisyphus only -> 11593 pkgs
Writed comparisons result @ result.rdb-comparison.json
```

Then navigate the file `result.rdb-comparison.json` which contains all required data.