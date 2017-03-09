find . -mindepth 5 -maxdepth 5 -execdir zip -r '{}'.zip '{}' \;
find . ! -iname "*.zip" -mindepth 5 -maxdepth 5 -exec rm -r "{}" \;