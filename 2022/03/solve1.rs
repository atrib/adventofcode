use std::env;
use std::fs;
// use std::slice;

fn find_common(left: &str, right: &str) -> char {
    let mut left_char_arr: Vec<char> = left.chars().collect();
    left_char_arr.sort();

    let mut right_char_arr: Vec<char> = right.chars().collect();
    right_char_arr.sort();

    // println!("{:?}", left_char_arr);
    // println!("{:?}", right_char_arr);
    let mut left_idx = 0;
    let mut right_idx = 0;

    while left_idx < left.len() && right_idx < right.len() {
        let leftc: char = left_char_arr[left_idx];
        let rightc: char = right_char_arr[right_idx];

        if leftc == rightc {
            return leftc;
        } else if leftc < rightc {
            left_idx += 1;
        } else {
            right_idx += 1;
        }
    }
    unreachable!();
}

fn char_to_prio(c: char) -> i64 {
    return  if c >= 'a' && c <= 'z'      { c as i64 - 'a' as i64 + 1}
            else if c >= 'A' && c <= 'Z' { c as i64 - 'A' as i64 + 27}
            else { 0 };
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
        let mut lines: Vec<&str> = contents.split("\n").collect();
        lines.truncate(lines.len() - 1);
        
        let backpack_halves = lines.into_iter().map(|line| line.split_at(line.len() / 2));
        // println!("var :{:?}", backpack_halves);
        let common_letter = backpack_halves.map(|(left, right)| find_common(left, right));
        // println!("var :{:?}", common_letter);
        let common_letter_prios = common_letter.map(|c| char_to_prio(c));
        // println!("var :{:?}", common_letter_prios);
        let prio_sum: i64 = common_letter_prios.fold(0, |x, y| x + y);
        println!("var :{:?}", prio_sum);
    }
}
