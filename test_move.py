from pdf_joiner import move


def check(items, sel, delta, want_items, want_sel):
    items = list(items)
    got_sel = move(items, sel, delta)
    assert items == list(want_items), (items, want_items)
    assert sorted(got_sel) == want_sel, (got_sel, want_sel)


check("ABCD", [1], -1, "BACD", [0])        # single row
check("ABCD", [0, 1], -1, "ABCD", [0, 1])  # group at the top stays put
check("ABCD", [2, 3], 1, "ABCD", [2, 3])   # group at the bottom stays put
check("ABCD", [1, 2], -1, "BCAD", [0, 1])  # group moves together
check("ABCD", [0, 2], -1, "ACBD", [0, 1])  # gap: only the free row moves
check("ABCD", [], 1, "ABCD", [])           # nothing selected
print("ok")
