# Locale Files

These files are managed via the OEP-58 process and should not be manually edited as they will be overwritten. The process is:

1. A Github action on `openedx-translations` will pull this repo and run `make extract-translations` on this repo's Makefile. This pulls all translatable strings from the Superset assets. These are then uploaded to Transifex for translation.
2. As translations are updated in Transifex they will be pushed to the correct language's files in `openedx-translations`.
3. A Github action on this repo will run `make pull-translations` periodically. This will run the Atlas tool to synchronize the translation files in this directory with what is stored in `openedx-translations`. Then it will run a command to compile all of the separate translated files into one `locale.yaml` that is used to create the localized dashboard and chart strings during the Tutor init command. It will then automatically merge those changed files.
