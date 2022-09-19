STYLES = stylesheets
OUTPUT = kirlent_docutils

CONCAT = awk 'FNR==1{print ""}{print}'

html5 = $(STYLES)/minimal.css $(STYLES)/plain.css
slides = $(html5) $(STYLES)/slides_base.css
impressjs = $(html5) $(STYLES)/slides_base.css $(STYLES)/impressjs.css
revealjs = $(html5) $(STYLES)/slides_base.css $(STYLES)/revealjs.css

all: $(OUTPUT)/kirlent_html5.css $(OUTPUT)/kirlent_slides.css $(OUTPUT)/kirlent_impressjs.css $(OUTPUT)/kirlent_revealjs.css

$(OUTPUT)/kirlent_html5.css: $(html5)
	$(CONCAT) $(html5) > $@

$(OUTPUT)/kirlent_slides.css: $(slides)
	$(CONCAT) $(slides) > $@

$(OUTPUT)/kirlent_impressjs.css: $(impressjs)
	$(CONCAT) $(impressjs) > $@

$(OUTPUT)/kirlent_revealjs.css: $(revealjs)
	$(CONCAT) $(revealjs) > $@
