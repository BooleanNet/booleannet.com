
# 
# WWW_HOST must be set in bash to sync correctly
#

README_URL = https://raw.githubusercontent.com/ialbert/booleannet-central/master/README.md
README = src/BOOLEAN_README.md

# Serve the website locally
serve: readme
	quarto preview www --port 8000


# Fetch the booleannet-central README used by www/booleannet.qmd
readme:
	curl -fsSL $(README_URL) -o $(README)

# Build the website
build: readme
	quarto render www

# Sync the website to the remote host
sync: build
	@test -n "$(WWW_HOST)" || { echo "# Error WWW_HOST is not set"; exit 1; }
	rsync -avz --delete -e "ssh -p 21098" www/_site/ $(WWW_HOST)

# Shortcut to commit/push
push:
	git commit -am "Update website"
	git push

# Shortcut to sync/push
web: sync push
