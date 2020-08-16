"""
Renders `src/main.template.tex` LaTeX template file using a language
configuration file as context. Pass the language as first argument
of the script.
"""

import os
import sys

import ruamel.yaml as yaml
from jinja2 import Environment, FileSystemLoader


LANGUAGES_DIR = "i18n"
PRIVATE_DIR = "_private"
SOURCE_DIR = "src"
TEMPLATE_FILENAME = "main.template.tex"


def get_language():
    lang = sys.argv[1]
    available_languages = [
        os.path.splitext(f)[0] for f in os.listdir(LANGUAGES_DIR)]
    if lang not in available_languages:
        raise ValueError("Language '%s' not available" % lang)
    return lang


def read_language_config(lang):
    config = {}

    lang_filename = "%s.yml" % lang

    language_config_filepath = os.path.join(LANGUAGES_DIR, lang_filename)
    with open(language_config_filepath, "r") as f:
        config.update(yaml.safe_load(f) or {})

    # Merge private data
    private_filepath = os.path.join(LANGUAGES_DIR, PRIVATE_DIR, lang_filename)
    if os.path.exists(private_filepath):
        with open(private_filepath) as f:
            config.update(yaml.safe_load(f) or {})

    return config


def render_template(context):
    env = Environment(
        loader=FileSystemLoader(SOURCE_DIR),
        block_start_string="[[",
        block_end_string="]]",
        variable_start_string="$",
        variable_end_string="$",
    )
    template = env.get_template(TEMPLATE_FILENAME)
    print(template.render(**context))

    return 0

def main():
    config = read_language_config(get_language())
    return render_template(config)


if __name__ == "__main__":
    sys.exit(main())
