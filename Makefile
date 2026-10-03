
# 
# REMOTE_SITE must be set in bash to sync correctly
#

serve:
	quarto preview www --port 8000

build:
	quarto 

sync:
	@test -n "$(REMOTE_SITE)" || { echo "ERROR: REMOTE_SITE is not set"; exit 1; }
	rsync -avz site "$(REMOTE_SITE)"