#!/usr/bin/env python

primers = {
    "outer_fwd": [(None, "tcggtctctatatgcaggtgtggccgattcattaatgcag")],
    "outer_rev": [(None, "agggtctcaatatgcaggtgtcttcgctattacgccag")],
    "inner_rev": [(None, "ctgtggtgataaaatatccca")],
    "inner_fwd": [("purple",    "tgggatattttatcaccacagtgtcagtacggaagcataccattcacca"),
                  ("orange",    "tgggatattttatcaccacaggttggatacggaagcataccattcacca"),
                  ("lightpink", "tgggatattttatcaccacaggttagttacggaagcataccattcacca"),
                  ("pink",      "tgggatattttatcaccacaggcatgttacggaagcataccattcacca"),
                  ("magenta",   "tgggatattttatcaccacaggttctatacggaagcataccattcacca"),
                  ("blue",      "tgggatattttatcaccacaggttaactacggaagcataccattcacca")]
}

for primer_type, seqs in primers.items():
    for prefix, seq in seqs:
        if prefix is None:
            with open(f"{primer_type}.txt", "w") as f:
                f.write(f"{seq}\n")
        else:
            with open(f"{primer_type}_{prefix}.txt", "w") as f:
                f.write(f"{seq}\n")

print("Done.")
