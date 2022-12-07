use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        return;
    }

    for file_path in &args[1..] {
        let contents = fs::read_to_string(file_path)
            .expect("Should have been able to read the file");
    
        let elf_rations: Vec<&str> = contents.split("\n\n").collect();
    
        let elfration_ints: Vec<i64> = elf_rations
                                                .into_iter().map(|s| s.split('\n').map(|ns| ns.parse::<i64>().unwrap()).collect())
                                                .map(|nv:Vec<i64>| nv.into_iter().fold(0, |x, y| x + y))
                                                .collect();
    
        let max_elf_ration = elfration_ints.iter().max().unwrap();
    
        println!("Max ration:\n{:?}", max_elf_ration);
    }
    // let file_path: &str = &args[1];
}
