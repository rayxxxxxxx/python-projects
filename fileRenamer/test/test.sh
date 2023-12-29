#!/bin/bash

echo "[*] copy test_dir to test_dir_copy"
cp -r test_dir test_dir_copy

echo "[*] running renamer.py with args: test_dir_copy snake-case"
python3 ../renamer.py test_dir_copy snake-case

echo "[*] running renamer.py with args: test_dir_copy camel-case --all"
python3 ../renamer.py test_dir_copy camel-case --all

echo "[*] removing test_dir_copy"
rm -rf test_dir_copy