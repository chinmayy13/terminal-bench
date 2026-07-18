There is an Apache-style access log at `/app/access.log` in the working directory.
Parse it and write a JSON summary report to `/app/report.json`.

The report must be a single JSON object with exactly these fields:

1. `total_requests` (integer) is the total number of log lines (requests) in the file.
2. `unique_ips` (integer) is the count of distinct client IP addresses that appear.
3. `top_path` (string) is the request path (e.g. `/index.html`) that appears most often
   across all requests.

Success criteria (all must hold):

1. `/app/report.json` exists and is valid JSON.
2. It contains the fields `total_requests`, `unique_ips`, and `top_path`.
3. `total_requests` equals the number of non-empty lines in `/app/access.log`.
4. `unique_ips` equals the number of distinct IP addresses among those lines.
5. `top_path` equals the most frequently requested path in the log.
