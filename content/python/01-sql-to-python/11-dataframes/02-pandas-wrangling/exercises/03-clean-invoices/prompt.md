Write `clean_invoices(raw)` that turns a raw frame like the bundled `messy_invoices.csv` (read with `pd.read_csv`) into a tidy one. Input columns have inconsistent case and padding: `Invoice #`, `Customer Name `, `AMOUNT`, `Invoice Date`, `Status`.

Return a new DataFrame with exactly these columns, in order:

- `invoice` (str, stripped), `customer_name` (stripped, Title Case), `amount` (float, NaN when missing or unparseable; strip `$` and `,`), `invoice_date` (datetime; formats `2025-09-26`, `05/26/2025` month-first, `20 Jun 2025`), `status` (stripped lowercase, `"unknown"` if missing).

Rows that are exact duplicates **after cleaning** are removed (keep the first). The index is `0..n-1`. The input must not be modified.
