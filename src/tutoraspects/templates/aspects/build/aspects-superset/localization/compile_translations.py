import os
import glob
import shutil

import ruamel.yaml
import ruamel.yaml.comments

yaml = ruamel.yaml.YAML()


def recursive_sort_mappings(s):
    """Given a ruamel yaml object, recursively sort all mappings in order."""
    if isinstance(s, list):
        for elem in s:
            recursive_sort_mappings(elem)
        return
    if not isinstance(s, dict):
        return
    for key in sorted(s, reverse=True):
        value = s.pop(key)
        recursive_sort_mappings(value)
        s.insert(0, key, value)

def compile_translations():
    """
    Combine translated files into the single file we use for translation.

    This should be called after we pull translations using Atlas, see the
    pull_translations make target.
    """
    translations_path = "/app/localization/"

    all_translations = ruamel.yaml.comments.CommentedMap()
    yaml_files = glob.glob(os.path.join(translations_path, "**/locale.yaml"))

    for file_path in yaml_files:
        lang = file_path.split(os.sep)[-2]
        with open(file_path, "r", encoding="utf-8") as asset_file:
            loc_str = asset_file.read()
        loaded_strings = yaml.load(loc_str)

        # Sometimes translated files come back with "en" as the top level
        # key, but still translated correctly.
        try:
            all_translations[lang] = loaded_strings[lang]
        except KeyError:
            all_translations[lang] = loaded_strings["en"]

        if None in all_translations[lang]:
            all_translations[lang].pop(None)

    out_path = "/app/localization/locale.yaml"

    print(f"Writing all translations out to {out_path}")
    with open(out_path, "w", encoding="utf-8") as outfile:
        outfile.write("---\n")
        # If we don't use an extremely large width, the jinja in our translations
        # can be broken by newlines. So we use the largest number there is.
        recursive_sort_mappings(all_translations)
        yaml.dump(all_translations, outfile)
        outfile.write("\n{{ patch('superset-extra-asset-translations')}}\n")

    # We remove these files to avoid confusion about where translations are coming
    # from, and because otherwise we will need to re-save them with the large
    # width as above to avoid Jinja parsing errors.
    print("Removing downloaded translations files... ")
    # shutil.rmtree(translations_path)


if __name__ == "__main__":
    compile_translations()
