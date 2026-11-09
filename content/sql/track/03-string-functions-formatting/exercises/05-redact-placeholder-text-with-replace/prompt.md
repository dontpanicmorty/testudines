Support ticket templates use a literal `{{customer}}` placeholder that never got filled in. Return `ticket_id` and a cleaned `description` where every `{{customer}}` token is replaced with the word `the customer`, then uppercased.

Order by `ticket_id`.
