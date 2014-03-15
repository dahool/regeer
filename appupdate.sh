#!/bin/bash
echo "Applying update ... (this could take some time)"
python manage.py collectstatic --noinput
python manage.py compilemessages
touch build.ver
echo "Reload"
touch wsgi.py
echo ""
echo "Finished"
echo ""