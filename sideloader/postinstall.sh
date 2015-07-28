cd "${INSTALLDIR}/${NAME}/tuneme/"
manage="${VENV}/bin/python ${INSTALLDIR}/${NAME}/tuneme/manage.py"

$manage migrate --settings=tuneme.settings.production

# process static files
$manage compress --settings=tuneme.settings.production
$manage collectstatic --noinput --settings=tuneme.settings.production

# compile i18n strings
$manage compilemessages --settings=tuneme.settings.production
