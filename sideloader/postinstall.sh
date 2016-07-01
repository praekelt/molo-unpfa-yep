cd "${INSTALLDIR}/${NAME}/"
manage="${VENV}/bin/python ${INSTALLDIR}/${NAME}/manage.py"

# run the following if migration `core 0031` has faild
# $manage migrate core 0031 --fake --settings=tuneme.settings.production
$manage migrate --settings=tuneme.settings.production

# process static files
$manage collectstatic --noinput --settings=tuneme.settings.production
$manage compress --settings=tuneme.settings.production

# compile i18n strings
$manage compilemessages --settings=tuneme.settings.production

# Update the search index
$manage update_index --settings=tuneme.settings.production


# Malawi
# ------
$manage migrate --settings=tuneme.settings.malawi
$manage collectstatic --noinput --settings=tuneme.settings.malawi
$manage compress --settings=tuneme.settings.malawi
$manage compilemessages --settings=tuneme.settings.malawi
$manage update_index --settings=tuneme.settings.malawi
