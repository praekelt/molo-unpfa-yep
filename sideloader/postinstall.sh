cd "${INSTALLDIR}/${NAME}/"
manage="${VENV}/bin/python ${INSTALLDIR}/${NAME}/manage.py"

$manage migrate --settings=tuneme.settings.production

# process static files
$manage collectstatic --noinput --settings=tuneme.settings.production
$manage compress --settings=tuneme.settings.production

# compile i18n strings
$manage compilemessages --settings=tuneme.settings.production

# Update the search index
$manage update_index


# Malawi
# ------
$manage migrate --settings=tuneme.settings.malawi
$manage collectstatic --noinput --settings=tuneme.settings.malawi
$manage compress --settings=tuneme.settings.malawi
$manage compilemessages --settings=tuneme.settings.malawi
$manage update_index --settings=tuneme.settings.malawi
