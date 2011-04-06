from django.conf import settings as main_settings

FLOOD_TIMEOUT=getattr(main_settings, 'FLOOD_TIMEOUT',30)
FLOOD_TEMPLATE=getattr(main_settings, 'FLOOD_TEMPLATE','flood.html')