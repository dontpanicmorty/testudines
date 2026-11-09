Write `collect_words(items)`. Go through the list `items` from the start and build a new list of the entries to keep:

- skip entries that are empty strings;
- stop completely when you reach the entry `"STOP"` (it is not kept);
- keep everything else, in order.

Use a `while` loop. `collect_words(["a", "", "b", "STOP", "c"])` returns `["a", "b"]`.
