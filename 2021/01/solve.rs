use std::io;
use std::io::prelude::*;
use std::fs::File;

fn main() -> io::Result<()> {
  let mut f = File::open("input")?;
  let mut buffer = [0; 1 << 10];

  // Count newlines in file
  loop {
    let n = f.read(&mut buffer)?;


    println!("bytes: {:?}", &buffer[..n]);
  }

  Ok(())
}