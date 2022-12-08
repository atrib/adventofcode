INPUTS = input.simple
INPUTS += input

SOLUTIONS = solve.txt
SOLUTIONS += solve2.txt

.PHONY: solution
solution: ${SOLUTIONS}
	cat ${SOLUTIONS}

%.txt: %
	./$< ${INPUTS} > $@

%: %.rs
	rustc -o $@ $< 

.PHONY: clean
clean:
	rm ${SOLUTIONS} $(SOLUTIONS:.txt=)
