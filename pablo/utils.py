from django.conf import settings as django_settings

from pablo import app_settings as settings
from pablo.logging import logger

from importlib import import_module

import os
import time
import sass
import jsmin
import shutil


def get_asset_directories():
    ''' get every app path that contains an "asset" folder on its root '''

    asset_apps = {}

    for app_name in django_settings.INSTALLED_APPS:
        app_module = import_module(app_name)
        app_path = app_module.__path__[0]

        if os.path.isdir(os.path.join(app_path, settings.ASSET_DIRECTORY_NAME)):
            asset_apps.update({
                app_name: {
                    'app_path': app_path,
                    'static_path': os.path.join(app_path, settings.STATIC_DIRECTORY_NAME, app_name),
                    'asset_path': os.path.join(app_path, settings.ASSET_DIRECTORY_NAME)
                }
            })

    return asset_apps


def build_scss(app_name, app_directories, verbose=True):
    logger.debug('Building \033[36msass\033[0m for app "{}" ...'.format(app_name))
    start = time.time()

    init_file_path = os.path.join(app_directories['asset_path'], settings.SASS_DIRECTORY_NAME, settings.SASS_INIT_FILENAME)

    if not os.path.isdir(os.path.dirname(init_file_path)):
        return
    elif not os.path.isfile(init_file_path):
        print('Init scss file not found! Searched for "{}"'.format(init_file_path))
        return

    with open(init_file_path, 'r') as init_scss_file:
        content = init_scss_file.read()

    sass_path = os.path.join(app_directories['asset_path'], settings.SASS_DIRECTORY_NAME)

    expanded_output = sass.compile(string=content, include_paths=[sass_path], output_style='expanded')
    compressed_output = sass.compile(string=content, include_paths=[sass_path], output_style='compressed')

    with open(os.path.join(app_directories['static_path'], '{}.css'.format(settings.CSS_OUTPUT_FILENAME)), 'w') as outfile:
        outfile.write(expanded_output)
    with open(os.path.join(app_directories['static_path'], '{}.min.css'.format(settings.CSS_OUTPUT_FILENAME)), 'w') as outfile:
        outfile.write(compressed_output)

    logger.debug('Finished after {:.3f} seconds\n'.format(time.time() - start))


def build_javascript(app_name, app_directories, verbose=True):
    logger.debug('Building \033[33mjavascript\033[0m for app "{}" ...'.format(app_name))

    start = time.time()

    js_files = []
    for root, dirs, files in os.walk(os.path.join(app_directories['asset_path'], settings.JS_DIRECTORY_NAME)):
        for f in files:
            if f.endswith('.js'):
                js_files.append(os.path.join(root, f))

    for js_file in js_files:
        with open(js_file, 'r') as infile:
            content = infile.read()

            dest_js_path = os.path.join(app_directories['static_path'], settings.JS_DIRECTORY_NAME)
            dest_file_name = os.path.basename(js_file)
            dest_file_name_stripped, dest_file_extenstion = os.path.splitext(dest_file_name)

            if not os.path.isdir(dest_js_path):
                os.makedirs(dest_js_path)

            with open(dest_js_path + dest_file_name, 'w') as outfile:
                outfile.write(content + '\n')

            with open(dest_js_path + dest_file_name_stripped + '.min' + dest_file_extenstion, 'w') as outfile:
                outfile.write(jsmin.jsmin(content))

    logger.debug('Finished after {:.3f} seconds\n'.format(time.time() - start))


def copy_images(app_name, app_directories, verbose=True):
    if not os.path.isdir(app_directories['asset_path'] + '/img'):
        return

    if app_name == 'hshassets':
        shutil.copy2(
            app_directories['asset_path'] + '/img/hsh_brand/favicons/{}/favicon.ico'.format(COLOR_SCHEME),
            app_directories['static_path'] + '/../favicon.ico'  # favicon for every app
        )

    start = time.time()
    logger.debug('Copying images ...')

    if os.path.isdir(app_directories['static_path'] + '/img'):
        shutil.rmtree(app_directories['static_path'] + '/img')

    shutil.copytree(
        app_directories['asset_path'] + '/img',
        app_directories['static_path'] + '/img'
    )

    logger.debug('Finished after {:.3f} seconds\n'.format(time.time() - start))


def copy_fonts(app_name, app_directories, verbose=True):
    if not os.path.isdir(app_directories['asset_path'] + '/fonts'):
        return

    start = time.time()
    logger.debug('Copying fonts ...')

    if os.path.isdir(app_directories['static_path'] + '/fonts'):
        shutil.rmtree(app_directories['static_path'] + '/fonts')

    shutil.copytree(
        app_directories['asset_path'] + '/fonts',
        app_directories['static_path'] + '/fonts'
    )

    logger.debug('Finished after {:.3f} seconds\n'.format(time.time() - start))


def discover_app(file_path):
    app_directories = {}

    for app_name, current_app_directories in get_asset_directories().items():
        if file_path.startswith(current_app_directories['app_path']):
            app_directories = current_app_directories
            break

    return (app_name, app_directories)


def do_everything(verbose=False):
    for app_name, app_directories in get_asset_directories().items():

        if os.path.isdir(app_directories['static_path']):
            shutil.rmtree(app_directories['static_path'])

        os.makedirs(app_directories['static_path'])

        build_scss(app_name, app_directories, verbose=verbose)
        build_javascript(app_name, app_directories, verbose=verbose)
        copy_images(app_name, app_directories, verbose=verbose)
        copy_fonts(app_name, app_directories, verbose=verbose)


def build_specific(app_name, app_directories, file_path):
    if file_path.endswith(('.sass', '.scss', '.css')):
        build_scss(app_name, app_directories)
    elif file_path.endswith(('.js')):
        build_javascript(app_name, app_directories)
