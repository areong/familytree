DOT = dot -v -Tsvg -o
NEATO = neato -v -Tsvg -o
DIAGRAMS = \
	FamilyTree.dot.svg\
	FamilyTree.neato.svg

%.dot.svg: %.dot
	$(DOT) $@ $<

%.neato.svg: %.dot
	$(NEATO) $@ $<

all: $(DIAGRAMS)
