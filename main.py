import os
from os import listdir
from os.path import isdir
import sys
import argparse
import yaml


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"Input dir: {path} is not a valid path")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate changelog")
    parser.add_argument('-d', metavar='', help='input directory', dest='input_dir', action='store', type=dir_path, default='.')
    parser.add_argument('-o', '--output', metavar='', help='output directory', dest='output_dir', action='store', type=dir_path, default='.')
    parser.add_argument('--dry-run', action='store_true', help='doesn\'t write or comit anything, just print to output')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    return parser.parse_args()


def get_entries(version_dir, type):
    logs = []
    path = os.path.join(version_dir, type)
    if os.path.exists(path):
        entries = [os.path.join(path, f) for f in listdir(path)]
        for entry in entries:
            with open(entry, 'r') as stream:
                try:
                    logs.append(yaml.safe_load(stream))
                except yaml.YAMLError as e:
                    print(e)

    return logs


def write_changelog_section(section, entries, config, output):
    if entries:
        output.write(f'### {section}:\n')
        for it in entries:
            output.write(f'- {it["title"]} [{it["id"]}]({config["jira-url"]}browse/{it["id"]})\n')

        output.write('\n')


def main():
    args = parse_arguments()

    config = {}
    with open(os.path.join(args.input_dir, "config.yaml"), 'r') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(e)

    release_dirs = [os.path.join(args.input_dir, f) for f in listdir(args.input_dir) if isdir(os.path.join(args.input_dir, f))]
    release_dirs.sort(reverse=True)

    if args.dry_run:
        output = sys.stdout
    else:
        output = open(os.path.join(args.output_dir, 'CHANGELOG.md'), 'w')

    for d in release_dirs:
        release_file = os.path.join(d, 'release.yaml')
        release_date = ""
        if os.path.exists(release_file):
            with open(release_file, 'r') as stream:
                try:
                    release_date = yaml.safe_load(stream)['date']
                except yaml.YAMLError as e:
                    print(e)

        output.write(f'## [{d.split("/")[-1]}]')
        if release_date:
            output.write(f' - {release_date}')
        output.write('\n')

        added_entries = get_entries(d, 'added')
        write_changelog_section('added', added_entries, config, output)

        changed_entries = get_entries(d, 'changed')
        write_changelog_section('changed', changed_entries, config, output)

        deprecated_entries = get_entries(d, 'deprecated')
        write_changelog_section('deprecated', deprecated_entries, config, output)

        removed_entries = get_entries(d, 'removed')
        write_changelog_section('removed', removed_entries, config, output)

        fixed_entries = get_entries(d, 'fixed')
        write_changelog_section('fixed', fixed_entries, config, output)

        security_entries = get_entries(d, 'security')
        write_changelog_section('security', security_entries, config, output)

    output.close()


if __name__ == "__main__":
    main()
