"""Convert TextExpander CSV files to Alfred .alfredsnippets files"""

import argparse
import csv
import os
import uuid
import shutil
import sys
import tempfile
from jinja2 import Environment, PackageLoader, select_autoescape


def read_csv(csv_file):
    """Read a TextExpander CSV file and return a list of dictionaries"""

    with open(csv_file, encoding='utf-8') as file:
        reader = csv.DictReader(file, fieldnames=['keyword', 'snippet', 'name'])
        return list(reader)


def render_snippet(env, snippet):
    """Render a TextExpander snippet as an Alfred snippet"""

    template = env.get_template("snippet.json")
    return template.render(**snippet)


def main():
    """Read options and convert TextExpander CSV file to Alfred .snippet file"""

    parser = argparse.ArgumentParser(
        description='Convert TextExpander CSV files to Alfred .alfredsnippets files.')
    parser.add_argument('-c', '--text-expander-csv', required=True, help="TextExpander CSV file")
    args = parser.parse_args()

    csv_file = args.text_expander_csv

    if not csv_file.endswith('.csv'):
        print(f'Error: File {csv_file} does not end with .csv', file=sys.stderr)
        sys.exit(1)

    basename = csv_file[:-4]
    snippet_file = basename + '.alfredsnippets'

    if os.path.isfile(snippet_file):
        print(f'Error: File {snippet_file} already exists.', file=sys.stderr)
        sys.exit(1)

    #  Read TextExpander CSV file
    snippets = read_csv(csv_file)

    #  Added a UUID to each snippet
    for snippet in snippets:
        snippet['uid'] = str(uuid.uuid4()).upper()

    #  Initialise Jinja2
    env = Environment(
        loader=PackageLoader('textexpander_to_alfred'),
        autoescape=select_autoescape()
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        # Write snippets to temp directory
        for snippet in snippets:
            filename = f'{temp_dir}/{snippet["name"]} [{snippet["uid"]}].json'

            with open(filename, 'w', encoding='utf-8') as snippet_json:
                snippet_json.write(render_snippet(env, snippet))

        # Copy plist file to temp directory
        shutil.copy('templates/info.plist', temp_dir)

        # Create .snippet file
        shutil.make_archive(basename, 'zip', temp_dir)
        shutil.move(f'{basename}.zip', snippet_file)


if __name__ == "__main__":
    main()
