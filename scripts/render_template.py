"""
Renders `src/main.template.tex` LaTeX template file using a language
configuration file as context. Pass the language as first argument
of the script.
"""

import os
import sys

import ruamel.yaml as yaml
from jinja2 import Environment, FileSystemLoader

CONFIG_DIR = 'config'
INFO_FILEPATH = os.path.join(CONFIG_DIR, 'info.yml')
LAYOUT_FILEPATH = os.path.join(CONFIG_DIR, 'layout.yml')
STYLING_FILEPATH = os.path.join(CONFIG_DIR, 'styling.yml')
LANGUAGES_DIR = "i18n"
PRIVATE_DIR = "_private"
SOURCE_DIR = "src"
TEMPLATE_FILENAME = "main.template.tex"


def get_language():
    """Read the language code passed as first command line argument."""
    if len(sys.argv) < 2:
        raise ValueError("You need to pass an available"
                         " language as first parameter.")

    lang = sys.argv[1]
    available_languages = [
        os.path.splitext(f)[0] for f in os.listdir(LANGUAGES_DIR)]
    if lang not in available_languages:
        raise ValueError("Language '%s' not available" % lang)
    return lang


def read_config(language_code):
    """Read and returns the configuration for a language by their code.

    Args:
        language_code (str): A language code which configuration files exists
            in the project.
    """
    config = {"language_code": language_code}

    lang_filename = "%s.yml" % language_code

    config_filepaths = [INFO_FILEPATH, LAYOUT_FILEPATH, STYLING_FILEPATH]
    for config_filepath in config_filepaths:
        with open(config_filepath, "r") as f:
            config.update(yaml.safe_load(f) or {})

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
    """Render the template with the language context data.

    Args:
        context (dict): Data used as context for the Jinja2 template.

    Returns:
        Exit code for the script, if success.
    """
    env = Environment(
        loader=FileSystemLoader(SOURCE_DIR),
        block_start_string="[[",
        block_end_string="]]",
        variable_start_string="$",
        variable_end_string="$",
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(TEMPLATE_FILENAME)
    sys.stdout.write(template.render(**context))

    return 0

if __name__ == "__main__":
    config = read_config(get_language())
    sys.exit(render_template(config))
