// extern crate regex;

use std::env;
use std::fs;
// use regex::Regex;
use circular_queue::CircularQueue;
use std::collections::HashSet;

fn main() {
    /* Usage:q
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

        let n_distinct = 14;

        let mut queue = CircularQueue::with_capacity(n_distinct);
        let mut n_chars = 0;
        for c in contents.chars() {
            n_chars += 1;
            queue.push(c);
            if queue.is_full() {
                let mut chars = HashSet::new();
                for c in queue.iter() {
                    chars.insert(c);
                }
                // println!("{}: len = {}", n_chars, chars.len());
                if chars.len() == n_distinct {
                    println!("{}", n_chars);
                    break;
                }
            }
        }     
    }
}
