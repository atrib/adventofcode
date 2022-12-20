INPUTS = input1.simple input4.simple
INPUTS += input

SOLUTIONS = solve1.txt
SOLUTIONS += solve2.txt

# PRECIOUS targets are intermediate files which are not deleted
.PRECIOUS: ${SOLUTIONS} $(SOLUTIONS:%.txt=%/target/debug/exe)
.PHONY: solution clean
solution: ${SOLUTIONS}
	cat ${SOLUTIONS}

clean:
	rm -f ${SOLUTIONS} $(SOLUTIONS:.txt=.exe)

%.txt: %/target/debug/exe ${INPUTS}
	$< ${INPUTS} > $@

%/target/debug/exe: %.rs
	cd $(<:.rs=) && cargo build

