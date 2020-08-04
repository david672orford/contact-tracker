export PATH := $(HOME)/Trinity_College/Web_Development/Tools/hypertext-toolbox/bin:$(PATH)

none:

favicon:
	@echo "Rendering favicon.ico..."
	# 16, 32, 48 are for favicon.ico:
	#   https://github.com/audreyr/favicon-cheat-sheet
    #   https://en.wikipedia.org/wiki/Favicon
	svg2png-icon favicon.svg 16 32 48
	icotool -c -o favicon.ico favicon-16x16.png favicon-32x32.png favicon-48x48.png
	rm favicon-??x??.png

	# 180 is for iOS homescreen:
	#   https://github.com/audreyr/favicon-cheat-sheet
	svg2png-icon favicon.svg 180

	# 192, and 512 are for the web app manifest:
	#   https://web.dev/add-manifest/
	svg2png-icon favicon.svg 192
	svg2png-icon favicon-large.svg 512

