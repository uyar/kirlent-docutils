STYLES = stylesheets
OUTPUT = kirlent_docutils

CONCAT = awk 'FNR==1{print ""}{print}'
RMHEAD = tail -n +2

html5 = $(STYLES)/minimal.css $(STYLES)/plain.css
slides = $(html5) $(STYLES)/slides_base.css $(STYLES)/slides.css
impressjs = $(html5) $(STYLES)/slides_base.css $(STYLES)/impressjs.css
revealjs = $(html5) $(STYLES)/slides_base.css $(STYLES)/revealjs.css

.PHONY: all

all: $(OUTPUT)/kirlent_html5.css $(OUTPUT)/kirlent_slides.css $(OUTPUT)/kirlent_impressjs.css $(OUTPUT)/kirlent_revealjs.css

$(OUTPUT)/kirlent_html5.css: $(html5)
	$(CONCAT) $(html5) | $(RMHEAD) > $@

$(OUTPUT)/kirlent_slides.css: $(slides)
	$(CONCAT) $(slides) | $(RMHEAD) > $@

$(OUTPUT)/kirlent_impressjs.css: $(impressjs)
	$(CONCAT) $(impressjs) | $(RMHEAD) > $@

$(OUTPUT)/kirlent_revealjs.css: $(revealjs)
	$(CONCAT) $(revealjs) | $(RMHEAD) > $@

clean:
	rm -f $(OUTPUT)/kirlent_html5.css
	rm -f $(OUTPUT)/kirlent_slides.css
	rm -f $(OUTPUT)/kirlent_impressjs.css
	rm -f $(OUTPUT)/kirlent_revealjs.css
