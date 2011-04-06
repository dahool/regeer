from django.conf import settings as main_settings

GRAVATAR_URL=getattr(main_settings, 'GRAVATAR_URL','http://www.gravatar.com/')
GRAVATAR_SIZE=getattr(main_settings, 'GRAVATAR_SIZE','32')
# mm: (mystery-man) a simple, cartoon-style silhouetted outline of a person (does not vary by email hash)
# identicon: a geometric pattern based on an email hash
# monsterid: a generated 'monster' with different colors, faces, etc
# wavatar: generated faces with differing features and backgrounds
GRAVATAR_DEFAULT=getattr(main_settings, 'GRAVATAR_DEFAULT','wavatar')