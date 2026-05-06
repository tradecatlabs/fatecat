use amlich::{Calendar, DayOfWeek, GregorianMonth};
use chrono::prelude::*;
use std::fmt::{Display, Error, Formatter};
use tui::backend::RustboxBackend;
use tui::layout::{Constraint, Direction, Layout, Rect};
use tui::style::{Color, Style};
use tui::widgets::{Block, Borders, Paragraph, Row, Table, Text, Widget};
use tui::Terminal;

const TABLE_HEADER: &[&str] = &["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const HELP_TEXT: &str = "q: quit  h: prev month  l: next month";

pub struct CalTable {
    month: GregorianMonth,
    terminal: Terminal<RustboxBackend>,
}

fn get_current_month() -> GregorianMonth {
    let now = Local::today();
    GregorianMonth::new(now.year(), now.month() as i32)
}

fn to_subscript(s: &str) -> String {
    fn char_2_char(c: char) -> char {
        match c {
            '0' => '₀',
            '1' => '₁',
            '2' => '₂',
            '3' => '₃',
            '4' => '₄',
            '5' => '₅',
            '6' => '₆',
            '7' => '₇',
            '8' => '₈',
            '9' => '₉',
            '-' => '₋',
            '+' => '+',
            _ => panic!("Oops"),
        }
    }
    let mut ss = String::with_capacity(s.len());
    for i in s.chars() {
        ss.push(char_2_char(i));
    }
    ss
}

struct TableCell {
    value: Option<String>,
}

impl TableCell {
    fn empty() -> TableCell {
        TableCell { value: None }
    }
}

impl Display for TableCell {
    fn fmt(&self, f: &mut Formatter) -> Result<(), Error> {
        match self.value {
            Some(ref s) => f.write_str(s.as_str()),
            None => Ok(()),
        }
    }
}

fn make_cell(x: u32, y: u32) -> TableCell {
    let mut s = format!("{:02}", x);
    s.push_str(to_subscript(format!("{:02}", y).as_str()).as_str());
    TableCell { value: Some(s) }
}

fn vcenter(area: &Rect, sz: u16) -> Rect {
    let padding = (area.height - sz) / 2;
    Layout::default()
        .direction(Direction::Vertical)
        .constraints(vec![
            Constraint::Min(padding),
            Constraint::Length(sz),
            Constraint::Min(padding),
        ])
        .split(area.clone())[1]
}

fn hcenter(area: &Rect, sz: u16) -> Rect {
    let padding = (area.width - sz) / 2;
    Layout::default()
        .direction(Direction::Horizontal)
        .constraints(vec![
            Constraint::Min(padding),
            Constraint::Length(sz),
            Constraint::Min(padding),
        ])
        .split(area.clone())[1]
}

impl CalTable {
    pub fn new() -> CalTable {
        let mut terminal = Terminal::new(RustboxBackend::new().unwrap()).unwrap();
        terminal.autoresize().unwrap();
        CalTable {
            month: get_current_month(),
            terminal,
        }
    }

    fn get_table(&self) -> Vec<Vec<TableCell>> {
        let mut template: Vec<Vec<TableCell>> = (0..6)
            .map(|_| (0..7).map(|_| TableCell::empty()).collect())
            .collect();
        let range = self.month.get_bound();
        let mut row_idx = 0;
        for d in range.iter() {
            template[row_idx][d.day_of_week() as usize] =
                make_cell(d.inner.day as u32, d.to_lunar().inner.day as u32);
            if d.day_of_week() == DayOfWeek::Saturday {
                row_idx += 1;
            }
        }
        template
    }

    pub fn run(&mut self) {
        loop {
            let table_title = &format!("[ {} ]", self.month.to_title());
            let mut table = Table::new(
                TABLE_HEADER.iter(),
                self.get_table()
                    .into_iter()
                    .map(|v| Row::Data(v.into_iter())),
            )
            .block(Block::default().title(table_title).borders(Borders::ALL))
            .widths(&[4; 7])
            .column_spacing(1)
            .header_style(Style::default().fg(Color::Green));
            let txts = [Text::raw(HELP_TEXT)];
            let mut help_txt = Paragraph::new(txts.iter());
            let desc = [Text::styled(
                format!(
                    "{} to {}",
                    self.month.get_bound().to_tuple().0.to_lunar(),
                    self.month.get_bound().to_tuple().1.to_lunar()
                ),
                Style::default().fg(Color::Cyan),
            )];
            let mut desc_txt = Paragraph::new(desc.into_iter());
            self.terminal
                .draw(|mut f| {
                    let size = f.size();
                    // Make layout
                    let mut chunks = tui::layout::Layout::default()
                        .direction(Direction::Vertical)
                        .constraints(vec![Constraint::Min(0), Constraint::Length(1)])
                        .split(size.clone());
                    if HELP_TEXT.len() as u16 <= size.width {
                        chunks[1] = hcenter(&chunks[1], HELP_TEXT.len() as u16);
                    }
                    let table_area = vcenter(&hcenter(&chunks[0], 38), 10);
                    table.render(&mut f, table_area.clone());
                    let desc_area = Rect {
                        y: table_area.y + table_area.height,
                        height: 1,
                        ..table_area
                    };
                    desc_txt.render(&mut f, hcenter(&desc_area, 30));
                    help_txt.render(&mut f, chunks[1]);
                })
                .unwrap();
            let t = self.terminal.backend().rustbox().poll_event(false).unwrap();
            if let rustbox::Event::KeyEvent(rustbox::Key::Char(c)) = t {
                match c.to_lowercase().to_string().chars().next().unwrap() {
                    'q' => break,
                    'h' => self.month = self.month.previous(),
                    'l' => self.month = self.month.next(),
                    _ => continue,
                }
            }
        }
    }
}
