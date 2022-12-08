// extern crate itertools;

use std::env;
use std::fs;
// use std::slice;
// use itertools::Itertools;

fn find_common(left_char_arr: &Vec<char>, right_char_arr: &Vec<char>) -> Vec<char> {
    // println!("{:?}", left_char_arr);
    // println!("{:?}", right_char_arr);
    let mut left_idx = 0;
    let mut right_idx = 0;
    let left_len = left_char_arr.len();
    let right_len = right_char_arr.len();

    let mut common_chars: Vec<char> = vec![];

    while left_idx < left_len && right_idx < right_len {
        let leftc: char = left_char_arr[left_idx];
        let rightc: char = right_char_arr[right_idx];

        if leftc == rightc {
            common_chars.push(leftc);
            left_idx += 1;
            right_idx += 1;
        } else if leftc < rightc {
            left_idx += 1;
        } else {
            right_idx += 1;
        }
    }
    return common_chars;
}

fn char_to_prio(c: char) -> i64 {
    return  if c >= 'a' && c <= 'z'      { c as i64 - 'a' as i64 + 1}
            else if c >= 'A' && c <= 'Z' { c as i64 - 'A' as i64 + 27}
            else { 0 };
}

fn sorted<T: Clone + Ord>(v: &Vec<T>)-> Vec<T> {
    let mut v = v.clone();
    v.sort();
    v
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
        
        /* Break each line into a sorted vector of chars */
        let lines: Vec<Vec<char>>
                    = lines.into_iter()
                           .map(|line| line.chars().collect())
                           .map(|chars| sorted(&chars))
                           .collect();
        
        let mut prio_sum = 0;
        for group_idx in 0..lines.len() / 3 {
            /* Find common chars in three consecutive lines */
            let common_chars = find_common(&find_common(&lines[3*group_idx], &lines[3*group_idx + 1]), &lines[3*group_idx + 2]);
            // println!("var :{:?}", common_chars);

            /* Just take the first, don't care if there are more than one */
            let prio = char_to_prio(common_chars[0]);
            prio_sum += prio;
        }
        println!("var :{:?}", prio_sum);
    }
}
