import importlib, os, sys
APP_DIRS = (os.path.abspath(os.path.join(PROJECT_ROOT, 'test')),)
sys.path.extend(APP_DIRS)

def auto_install_app(app_dirs, installed_apps):
    base_url_confs = []
    for app_dir in app_dirs:
        for app in os.listdir(app_dir):
            if not app.startswith('.') and app not in installed_apps:
                try:
                    app_settings = importlib.import_module('%s.settings' % app)
                    if getattr(app_settings, 'APP_NAME', '') != '':
                        print "Auto Installed %s" % app
                        INSTALLED_APPS = installed_apps + (app,)
                    base_url_conf = getattr(app_settings, 'BASE_URL_CONF', '')
                    if base_url_conf != '':
                        base_url_confs.append(base_url_conf)
                except ImportError:
                    pass
