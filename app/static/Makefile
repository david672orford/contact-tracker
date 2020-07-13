export PATH := $(HOME)/Trinity_College/Web_Development/Tools/hypertext-toolbox/bin:$(PATH)

none:

favicon:
	@echo "Rendering favicon to PNG..."
	# 48 is for the page header
	# 16, 32, 48 are for favicon.ico:
	#   https://github.com/audreyr/favicon-cheat-sheet
    #   https://en.wikipedia.org/wiki/Favicon
	# 152 is for iOS homescreen:
	#   https://github.com/audreyr/favicon-cheat-sheet
	# 144 is for the Web App Manifest:
	#   https://developers.google.com/web/updates/2014/11/Support-for-installable-web-apps-with-webapp-manifest-in-chrome-38-for-Android?hl=en
	svg2png-icon favicon.svg 16 32 48 64 96 144 152 192
	@echo "Making favicon.ico..."
	icotool -c -o favicon.ico favicon-16x16.png favicon-32x32.png favicon-48x48.png

