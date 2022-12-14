INPUTS = input.simple
# INPUTS += input

SOLUTIONS = solve1.txt
# SOLUTIONS += solve2.txt

.PRECIOUS: ${SOLUTIONS} $(SOLUTIONS:.txt=.exe)
.PHONY: solution clean
solution: ${SOLUTIONS}
	cat ${SOLUTIONS}

clean:
	rm -f ${SOLUTIONS} $(SOLUTIONS:.txt=.exe)

%.txt: %.exe ${INPUTS}
	./$< ${INPUTS} > $@

%.exe: %.rs
	rustc -o $@ $< 

