extern crate regex;

use std::env;
use std::fs;
use regex::Regex;

fn overlap(first: (i64, i64), second: (i64, i64)) -> bool {
    return (first.0 <= second.0 && first.1 >= second.1) ||
            (second.0 <= first.0 && second.1 >= first.1) || 
            (first.0 <= second.0 && second.0 <= first.1) ||
            (first.0 <= second.1 && second.1 <= first.1);
}

#[allow(dead_code)]
fn full_overlap(first: (i64, i64), second: (i64, i64)) -> bool {
    return (first.0 <= second.0 && first.1 >= second.1) ||
            (second.0 <= first.0 && second.1 >= first.1);
}

fn interpret_input(contents: &str) -> Vec<((i64, i64), (i64, i64))>  {
    let re = Regex::new(r"(\d+)-(\d+),(\d+)-(\d+)").unwrap();

    let pairs
            = re.captures_iter(contents)
                .map(|cap| ( (cap.get(1).unwrap().as_str().parse::<i64>().unwrap(), cap.get(2).unwrap().as_str().parse::<i64>().unwrap()),
                             (cap.get(3).unwrap().as_str().parse::<i64>().unwrap(), cap.get(4).unwrap().as_str().parse::<i64>().unwrap()) ) )
                .collect();
    
    return pairs;
}

fn main() {
    /* Usage:
     * ./<exe> [input files]
     * E.g.: ./solve1.exe input input.simple
     */
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        return;
    }

    for file_path in &args[1..] {
        /* Read in file as a list of lines, truncate last empty line */
        let contents = fs::read_to_string(file_path)
            .expect("Should have been able to read the file");

        let assn_pairs = interpret_input(&contents);
        let assn_overlap = assn_pairs.into_iter()
                                        .map(|pair| if overlap(pair.0, pair.1) {1} else {0});
        let overlap_sum = assn_overlap.fold(0, |x, y| x + y);
        println!("{}", overlap_sum);
    }
}
