# db-from-scratch

A small SQLite-style database written in C, built stage by stage to understand
how a database works under the hood: from a REPL, through fixed-size pages on
disk, to a B-Tree that backs the table.

Based on the [cstack "Let's Build a Simple Database"](https://cstack.github.io/db_tutorial/)
tutorial. The goal is not a production database. The goal is to be able to
reason about real systems ("why is this query slow?", "why does an index help?",
"what happens on disk when I insert a row?") because I built the mechanism once.

## Architecture

```
            +-----------------------+
 input ---> |  REPL / front-end     |  read a line, split meta-commands from SQL
            +-----------+-----------+
                        |
            +-----------v-----------+
            |  Compiler (prepare)   |  text -> Statement { type, row }
            +-----------+-----------+
                        |
            +-----------v-----------+
            |  Virtual machine      |  execute Statement against the table
            +-----------+-----------+
                        |
            +-----------v-----------+
            |  Table / Cursor       |  "where is row N?" abstraction
            +-----------+-----------+
                        |
            +-----------v-----------+
            |  B-Tree               |  ordered keys, leaf + internal nodes
            +-----------+-----------+
                        |
            +-----------v-----------+
            |  Pager                |  fixed-size pages, in-memory cache
            +-----------+-----------+
                        |
                   database file
```

## Stages

| #  | Stage                                   | Topic                                          |
|----|-----------------------------------------|------------------------------------------------|
| 01 | REPL and SQL front-end                  | input loop, meta-commands, prepare/execute     |
| 02 | In-memory table                         | row layout, serialization, pages in RAM        |
| 03 | Persistence                             | pager, file I/O, flush on exit                 |
| 04 | Cursor                                  | decoupling "position" from table storage       |
| 05 | B-Tree leaf node                        | node layout, header, cells                     |
| 06 | Binary search and duplicate keys        | ordered inserts                                |
| 07 | Splitting a leaf node                   | what happens when a page is full               |
| 08 | Recursive search / internal nodes       | tree of pages                                  |
| 09 | Scanning a multi-level tree             | sibling pointers                               |
| 10 | Splitting an internal node              | growing the tree upward                        |

## Build and test

```sh
make          # builds build/db
make test     # runs black-box tests in tests/run_tests.py
./build/db    # starts the REPL
```

Requires a C11 compiler (clang or gcc), `make` and Python 3.

## Status

- [ ] 01 REPL and SQL front-end
