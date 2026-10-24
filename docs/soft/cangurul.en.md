---
category: Software
tags: [algorithms, Rust, Windows, macOS, Linux]
summary: The “Cangurul” (Kangaroo) environment for learning algorithms — a program written with simple commands makes the kangaroo hop around the field and draw lines.
image: assets/images/soft/preview-cangurul.png
logo: assets/images/soft/logo-cangurul.png
website: https://nazdravan.github.io/cangurul/en/
repo: https://github.com/nazdravan/cangurul
---

The kangaroo sits on a grid field. The student writes a program with simple commands — `STEP`, `JUMP`, `ROTATE`, loops, conditions, and procedures — and the kangaroo runs it, drawing lines on the field. A handful of commands is enough for letters, squares, spirals, and even the kangaroo's own name. Cangurul 3 is a Rust rewrite of the “Cangurul” program (version 2), and old `.cng` files open and run unchanged. *Cangurul* is Romanian for “the kangaroo”.

![Cangurul: an original example after running](../assets/images/soft/preview-cangurul.png)

**[Download Cangurul](https://github.com/nazdravan/cangurul/releases/latest)** · [Program website](https://nazdravan.github.io/cangurul/en/) · [Source code on GitHub](https://github.com/nazdravan/cangurul)

## Download and install

On the [Releases](https://github.com/nazdravan/cangurul/releases/latest) page, pick the right file:

| System | File |
|---|---|
| Windows 10 / 11, 64-bit | `cangurul-<version>-windows-x64.msi` (installer) or `-windows-x64-portable.zip` |
| Windows 10 / 11, 32-bit | `cangurul-<version>-windows-x86.msi` or `-windows-x86-portable.zip` |
| Windows 7 and 8 (32- and 64-bit) | `cangurul-<version>-windows7-x86-portable.zip` |
| macOS (Apple Silicon and Intel) | `cangurul-<version>-macos-universal.dmg` |
| Ubuntu / Debian / Mint | `cangurul-<version>-linux-x86_64.deb` |
| Any Linux | `cangurul-<version>-linux-x86_64.AppImage` |

- **Windows:** the `.msi` installer adds Cangurul to the Start menu, and `.cng` files open with a double click. The `.zip` needs no installation: unzip it and run `Cangurul.exe`.
- **macOS:** open the `.dmg` and drag `Cangurul.app` onto *Applications*. The app is not signed with an Apple certificate, so on first launch: right click → *Open* (on macOS 15+: *System Settings → Privacy & Security → Open Anyway*).
- **Linux:** `sudo apt install ./cangurul-*.deb` or `chmod +x cangurul-*.AppImage && ./cangurul-*.AppImage`.

!!! tip "A whole lab"
    The installer can run silently: `msiexec /i cangurul-*.msi /qn`. Add `INSTALLFOLDER="D:\Cangurul"` for another folder and `DESKTOPSHORTCUT=""` to skip the desktop shortcut.

## The language

| Command | What it does |
|---|---|
| `STEP` | one step forward, leaving a trace |
| `JUMP` | one step forward, no trace |
| `ROTATE` | turn 90° clockwise |
| `REPEAT N TIMES … END REPEAT` | repeats N times |
| `WHILE [NOT] condition … END CYCLE` | repeats while the condition is true |
| `IF [NOT] condition command1 ELSE command2` | branching (`ELSE` is optional) |
| `PROCEDURE Name … END PROCEDURE` | defines a procedure (before the main program) |
| `EXECUTE Name` | calls the procedure |
| `[ … ]` | the main program |
| `// …` and `* … *` | comments |

Conditions: `IS_BORDER` (the kangaroo is facing the edge of the field) and `IS_LINE` (there is already a line, or the edge, in front of it). The kangaroo starts in the top-left corner, facing right.

### First program: a square

Four sides of 5 steps each, with a turn after each one:

```text
// A square with a side of 5 steps
[
repeat 4 times
    repeat 5 times
        step
    end repeat
    rotate
end repeat
]
```

### Conditional loops: the spiral

The original “Spirala” example: the kangaroo walks forward until it hits a line (or the edge), then turns. Since each lap stops in front of the line from the previous lap, the drawing winds in toward the center. Here it is in Romanian, as it ships with the program:

```text
// Acest program prezinta
//  modul de a desena o
//       Spirala
[
cit nu e_linie
    cit nu e_linie
        pas
    sfirsitul ciclului
    rotire
sfirsitul ciclului
]
```

### Keywords in three languages

They can be written in any of the languages, with or without diacritics, in upper or lower case.

| Română | English | Русский |
|---|---|---|
| `PAS SALT ROTIRE` | `STEP JUMP ROTATE` | `ШАГ ПРЫЖОК ПОВОРОТ` |
| `REPETĂ ORI` | `REPEAT TIMES` | `ПОВТОРИ РАЗ` |
| `CÎT` | `WHILE` | `ПОКА` |
| `DACĂ ATUNCI ALTFEL` | `IF THEN ELSE` | `ЕСЛИ ТОГДА ИНАЧЕ` |
| `NU` | `NOT` | `НЕ` |
| `PROCEDURA EXECUTĂ` | `PROCEDURE EXECUTE` | `ПРОЦЕДУРА ВЫПОЛНИТЬ` |
| `SFÎRȘITUL REPETĂRII / CICLULUI / PROCEDURII` | `END REPEAT / CYCLE / PROCEDURE` | `КОНЕЦ ПОВТОРА / ЦИКЛА / ПРОЦЕДУРЫ` |
| `E_MARGINE E_LINIE` | `IS_BORDER IS_LINE` | `КРАЙ ЛИНИЯ` |

## Code analyzer

![The code analyzer with errors and suggestions](../assets/images/soft/cangurul-analizor.png)

The program is checked on every change, and the analyzer finds all the mistakes, not just the first one:

- misspelled words get a wavy underline (red = error, yellow = warning); hovering shows the explanation;
- the **Problems** list below the editor shows every error, and a click takes the cursor to the word;
- misspelled words get a suggested fix (“Did you mean JUMP?”) that the **Fix** button applies;
- a program with errors won't run; warnings (unused procedures, empty blocks, `WHILE` loops that don't move the kangaroo) don't block it.

## Keyboard shortcuts

| Key | Action |
|---|---|
| ++f5++ | run / pause |
| ++f6++ | step by step |
| ++esc++ | stop |
| ++f7++ | check |
| ++ctrl+shift+f++ | format the program |
| ++ctrl+n++ / ++ctrl+o++ / ++ctrl+s++ | new / open / save |

## What's new compared to the original

| | |
|---|---|
| **Interface** | light and dark theme; interface in Romanian, Russian, and English |
| **Editor** | line numbers, syntax highlighting, buttons that insert commands, auto-indent |
| **Execution** | smooth animation, current line highlighted; step by step, pause, adjustable speed or instant |
| **Field** | adjustable size (20 × 20 by default); jumps can be shown as dotted lines |
| **Files** | the program and settings are kept between launches; open by drag & drop |

!!! info "Open-source"
    Cangurul 3 is free software under the [GPL-3.0](https://github.com/nazdravan/cangurul/blob/main/LICENSE) license. Source code, changelog, and issue tracker are on [GitHub](https://github.com/nazdravan/cangurul).
