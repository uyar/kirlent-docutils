# Copyright 2022 H. Turgut Uyar <uyar@tekir.org>
#
# kirlent_docutils is released under the BSD license.
# Read the included LICENSE.txt file for details.

from docutils import frontend


def stylesheet_path_option(sheets):
    return (
        'Comma separated list of stylesheet paths. '
        'Relative paths are expanded if a matching file is found in '
        'the --stylesheet-dirs. With --link-stylesheet, '
        'the path is rewritten relative to the output HTML file. '
        '(default: "%s")' % ','.join(sheets),
        ["--stylesheet-path"],
        {
            "metavar": "<file[,file,...]>",
            "overrides": "stylesheet",
            "validator": frontend.validate_comma_separated_list,
            "default": sheets,
        }
    )


def stylesheet_dirs_option(dirs):
    return (
        'Comma-separated list of directories where stylesheets are found. '
        'Used by --stylesheet-path when expanding relative path arguments. '
        '(default: "%(dirs)s")' % {"dirs": ','.join(dirs)},
        ["--stylesheet-dirs"],
        {
            "metavar": "<dir[,dir,...]>",
            "validator": frontend.validate_comma_separated_list,
            "default": dirs,
        }
    )
