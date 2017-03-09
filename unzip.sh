find . -iname "*.zip" -mindepth 5 -maxdepth 5 -execdir unzip '{}' \;
find . -iname "*.zip" -mindepth 5 -maxdepth 5 -exec rm -r "{}" \;