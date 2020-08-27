# cv (WIP)

My own curriculum vitae written in LaTeX. It uses the awesome template
 [liantze/AltaCV][altacv-link] edited to customize sections and render
 in multiple languages.

## Setup environment (Linux)

> Python with `virtualenv` installed is required.

1. Go to [TexLive download page][texlive-download-link] and download the
 package for your distribution.
2. Go to [quick installation instructions page][texlive-download-link] and
 follow the steps.
3. Initialize the virtualenv `python -m virtualenv venv && . venv/bin/activate`
4. Install requirements: `pip install -r requirements.txt`

## Add your info

- All rendered fields are declared in YAML files with fields by language code,
 stored in the directory `_i18n/`. Also, if you have private information
 that you don't want to publish, insert it in the files located at
 `i18n/_private/` directory, following the same language codes of `i18n/`.
- Template layout can be customized using the file `config/layout.yml`.
- Template styles can be customized using the file `config/styles.yml`.


[altacv-link]: https://github.com/liantze/AltaCV
[texlive-download-link]: http://www.tug.org/texlive/acquire-netinstall.html
[texlive-download-link]: http://www.tug.org/texlive/quickinstall.html
