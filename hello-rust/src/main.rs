// use ferris_says::say;
// use std::io::{stdout, BufWriter};
use std::fs;

fn main() {
    // let stdout = stdout();

    let filename = String::from("../2021/day01input.txt");
    let contents = fs::read_to_string(filename)
        .expect("Something went wrong reading the file");

    let csplit = contents.split("\n");

    // println!("csplit: {:?}.", csplit);

    let csplitints: Vec<i32> = csplit.map(|line| {
        // println!("I like {}.", line);
        line.trim().parse::<i32>().unwrap()
    }).collect();

    // println!("csplitints: {:?}.", csplitints);

    // part 1
    let mut tint = 1000000;
    let mut counter = 0;
    for i in csplitints {
        if i > tint {
            counter+= 1;
        }
        tint = i;
    }
    println!("part1 counter: {}", counter)
    // let message = counter.to_string();
    // // let message = String::from("Hello fellow Rustaceans!");
    // let width = message.chars().count();

    // let mut writer = BufWriter::new(stdout.lock());
    // say(message.as_bytes(), width, &mut writer).unwrap();

}

