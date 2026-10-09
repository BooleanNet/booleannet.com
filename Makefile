
# 

USER = www

README_URL = https://raw.githubusercontent.com/ialbert/booleannet-central/master/README.md
README = docs/booleannet.readme.md

DOC_DIR = docs
SITE_DIR = _site

# Serve the website locally
serve:
	quarto preview $(DOC_DIR) --port 8000

# Fetch the booleannet-central README used by www/booleannet.qmd
fetch:
	curl -fsSL $(README_URL) -o $(README)

# Build the website
build: 
	quarto render $(DOC_DIR) --output-dir $(SITE_DIR)

# Sync the website to the remote host
sync: build
	rsync -avz -e "ssh -p 21098" ${DOC_DIR}/${SITE_DIR}/ $(USER)@booleannet.com:www/

# Shortcut to commit/push
push:
	git commit -am "Update website"
	git push

# Shortcut to sync/push
web: sync push
