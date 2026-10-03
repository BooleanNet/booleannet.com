
# 
# WWW_HOST must be set in bash to sync correctly
#

serve:
	quarto preview www --port 8000

build:
	quarto render www

web: build
	@test -n "$(WWW_HOST)" || { echo "# Error WWW_HOST is not set"; exit 1; }
	rsync -avz --delete -e "ssh -p 21098" www/_site/ $(WWW_HOST)