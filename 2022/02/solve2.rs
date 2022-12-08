use std::env;
use std::fs;


fn pair_score((opp, outcome): (i64, i64)) -> i64 {
    let outcome_score = outcome * 3;                     // X = 0 = Loss, Y = 1 = Draw, Z = 2 = Win
    let shape = if outcome == 0      { (opp + 2) % 3}    // Lose
                else if outcome == 1 { opp }             // Draw
                else                 { (opp + 1) % 3};   // Win
    let shape_score = 1 + shape;

    return shape_score + outcome_score;       
}

fn to_int_rep(pairvec: Vec<&str>) -> (i64, i64) {
    let opp = pairvec[0].chars().nth(0).unwrap();
    let outcome = pairvec[1].chars().nth(0).unwrap();

    return (opp as i64 - 'A' as i64, outcome as i64 - 'X' as i64);
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
        
        /* Split each line on space, creating a vector of str for each line 
         * Each line is then is mapped to a tuple (0-2, 0-2) representing each column
         * Then, we score each pair and add them up with 'fold'
        */
        let guide_pairs = lines.into_iter().map(|s| s.split(' '));
        let score_map = guide_pairs.map(|pair| pair_score(to_int_rep(pair.collect::<Vec<&str>>())));
        let total_score = score_map.fold(0, |x, y| x + y);
        println!("var :{:?}", total_score);
        // println!("var :{:?}", score_map.collect::<Vec<i64>>());
    }
}
