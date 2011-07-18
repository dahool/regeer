Installing Regeer in a Production Environment
==============================================

Regeer core is django, so it can be installed in any environment supported by django,
see https://docs.djangoproject.com/en/dev/howto/deployment/ for more information.

In the following document we will tell you how to install it over Apache and mod_wsgi.

We assume you already has mod_wsgi and apache installed, and you followed the *Quick Install*
and *Running The Development Server* instructions.

In the doc/dist folder you'll find two files to help you with the server configuration.

* regeer.conf: put this file under your apache vhosts directory and modify at your needs
* regeer.wsgi: this is the wsgi script needed to run the application, modifiy the paths
  with your application settings and put it under a directory accesible by apache.
  Have in mind that the path to this script is in the regeer.conf file.

Edit 60-local.pyconf and add:

    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
    SITE_NAME = '<your desired site name>'


 


