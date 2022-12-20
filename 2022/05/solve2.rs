extern crate regex;

use std::env;
use std::fs;
use regex::Regex;

// struct Vec<T> {
//     Node(T,My<T>),
//     Empty
// }

// let Node(a,Node(b,_)) = mylist;

struct Stack<'a> {
    _name: &'a str,
    elems: Vec<&'a str>
}

struct Move {
    n: usize,
    from: usize,
    to: usize
}

fn interpret_input(contents: &str) -> (Vec<Stack>, Vec<Move>) {
    // let parts: Vec<&str> = contents.split("\n\n").take(2).collect();
    // if let [first, second] = parts[0..2] {
    //     println!("Hello");
    // }    else {
    //     panic!();
    // }
    
    let parts: Vec<&str> = contents.split("\n\n").collect();
    let stacks: Vec<&str> = parts[0].split('\n').collect();
    let (stack_items, stack_names) = stacks.split_at(stacks.len() - 1);
    let moves = parts[1].split('\n');

    let re = Regex::new(r"\s*([0-9])+\s+").unwrap();
    let mut stacks = re.captures_iter(stack_names[0])
                        .map(|cap| Stack {
                                        _name: cap.get(1).unwrap().as_str(),
                                        elems: vec![]
                                    }
                            )
                        .collect::<Vec<Stack>>();

    // println!("{}", stacks.len());

    let re = Regex::new(r"(\s{4}|\[[A-Z]\](\s|$))").unwrap();
    let re_item = Regex::new(r"\[([A-Z]*)\]").unwrap();
    for line in stack_items {
        // println!("{}", line);
        re.captures_iter(line)
            .zip(&mut stacks)
            .for_each(|(cap, stack)| {
                let s = cap.get(1).unwrap().as_str();
                // println!("item: <{}>", s);
                if s != "    " {
                    let item_cap = re_item.captures(s).unwrap();
                    let item_name = item_cap.get(1).unwrap().as_str();
                    stack.elems.push(item_name);
                }
            });
        // for stack in &stacks {
        //     for elem in &stack.elems {
        //         print!("{} ", elem);
        //     }
        //     println!("");
        // }
    }

    stacks.iter_mut().for_each(|stack| stack.elems.reverse());

    let re_move = Regex::new(r"move ([0-9]+) from ([0-9]+) to ([0-9]+)").unwrap();
    let moves = moves
                .filter_map(|line| 
                    {
                        // println!("{}", &line);
                        let move_cap = re_move.captures(line);
                        match move_cap {
                            None => None,
                            Some(move_cap) => Some(Move {
                                    n:    move_cap.get(1).unwrap().as_str().parse::<usize>().unwrap(),
                                    from: move_cap.get(2).unwrap().as_str().parse::<usize>().unwrap(),
                                    to:   move_cap.get(3).unwrap().as_str().parse::<usize>().unwrap(),
                                })
                        }
                    })
                .collect::<Vec<Move>>();

    return (stacks, moves);
}

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

        let (mut stacks, moves) = interpret_input(&contents);
        // for stack in &stacks {
        //     for elem in &stack.elems {
        //         print!("{} ", elem);
        //     }
        //     println!("");
        // }
        for mov in moves {
            let mut tmp_stack = vec![];
            for _ in 0..mov.n {
                let val = stacks[mov.from - 1].elems.pop().unwrap();
                tmp_stack.push(val);
            }
            for _ in 0..mov.n {
                let val = tmp_stack.pop().unwrap();
                stacks[mov.to - 1].elems.push(val);
            }
        }

        let top_crates = stacks
                            .into_iter()
                            .map(|mut stack| stack.elems.pop().unwrap())
                            .collect::<Vec<&str>>();

        // for t in top_crates {
        //     println!("{}", t);
        // }
        // top_crates.fold("", |exist, next| format!("{}{}", exist, next).to_str());
        println!("{}", top_crates.join(""));
    }
}
