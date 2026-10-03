
# 
# WWW_HOST must be set in bash to sync correctly
#

# Serve the website locally
serve:
	quarto preview www --port 8000

# Build the website
build:
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
