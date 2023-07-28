import sys
import yaml
from transifex.native import init, tx

from transifex.native.parsing import SourceString

LANGUAGES = ['en', 'es', 'it', 'fr', 'zh', 'ja', 'de', 'pt', 'pt_BR', 'ru', 'ko', 'sk', 'sl', 'nl']

init('token', 
    LANGUAGES, 
     'secret')

#tx.fetch_translations()

def main(root_path):
    assets_file = root_path + "/env/plugins/aspects/apps/superset/pythonpath/assets.yaml"
    
    file = yaml.load(open(assets_file, "r"), Loader=yaml.FullLoader)
    for asset in file:
        strings = mark_text_for_translation(asset)
        write_locale_file(strings)



def mark_text_for_translation(strings):
    """For every asset extract the text and mark it for translation"""
    source_strings = []
    for text in strings:
        ...
        #source_string = SourceString(
        #    text,
        #)
        #source_strings.append(source_string)

    # response_code, response_content = tx.push_source_strings(source_strings, purge=True)
    #print(response_code, response_content)
    #return source_strings

def write_locale_file(strings):
    """Write the locale file for every language"""
    for language in LANGUAGES:
        translations = tx.pull_translations(language)
        locale_file = open(language + ".yaml", "w")
        locale_file.write(yaml.dump(translations, default_flow_style=False))
        locale_file.close()



if __name__ == "__main__":
    main(sys.argv[1])
