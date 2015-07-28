cd "${INSTALLDIR}/${NAME}/unpfayep/"
manage="${VENV}/bin/python ${INSTALLDIR}/${NAME}/unpfayep/manage.py"

$manage migrate --settings=unpfayep.settings.production

# process static files
$manage compress --settings=unpfayep.settings.production
$manage collectstatic --noinput --settings=unpfayep.settings.production

# compile i18n strings
$manage compilemessages --settings=unpfayep.settings.production
