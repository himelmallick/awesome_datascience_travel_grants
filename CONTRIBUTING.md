# Contributing

Thank you for helping keep this list current. Award pages move and deadlines change every year, so every correction counts, however small.

## Three ways to contribute

**1. Fill in a form (no Git needed).**
[Suggest an award](https://github.com/himelmallick/awesome_datascience_travel_grants/issues/new?template=new-award.yml) or [report a correction](https://github.com/himelmallick/awesome_datascience_travel_grants/issues/new?template=correction.yml). A maintainer makes the change for you.

**2. Edit the table in your browser.**
Open [`awards.csv`](awards.csv) on GitHub, click the pencil icon, edit or add a row, and click "Propose changes". GitHub creates the pull request for you.

**3. Open a pull request.**
Fork the repository, edit `awards.csv`, and open a pull request against `master`.

In all three cases, edit `awards.csv` only. `README.md` is rebuilt from it automatically after a change is merged.

## What belongs on the list

An award fits if all of these hold:

- It supports **students or early-career researchers** (roughly within ten years of the final degree) in statistics, biostatistics, data science, machine learning or computational biology.
- It helps with **travel or recognition**: a travel grant, a paper or poster award, a conference fellowship, or an early-career prize.
- It has an **open call** (application or nomination) that **recurs**, usually every year.
- It has an **official page** you can link to.

Awards from any country or society are welcome.

## The columns of `awards.csv`

| Column | What to write | Example |
|---|---|---|
| `category` | One of `students`, `asa-sections`, `early-career`, `conferences`, `other` | `students` |
| `name` | The official name of the award | `ENAR Distinguished Student Paper Awards` |
| `organization` | The society or organizer | `International Biometric Society, Eastern North American Region` |
| `url` | The official page, starting with `https://` | `https://www.enar.org/meetings/StudentPaperAwards/` |
| `eligibility` | Who can apply, in one sentence, in the words of the official page | `ENAR member; degree candidate during the calendar year; first author` |
| `support` | What the award covers, in one sentence | `Travel reimbursement up to $650 and one short-course tuition waiver` |
| `deadline` | When the call usually closes, without a year | `Mid-October`, `November 15`, `Varies each year, typically May` |
| `deadline_month` | The month of that deadline as a number from 1 to 12. Leave empty if it varies by conference | `10` |
| `verified` | The date you checked the official page, as year-month-day | `2026-10-04` |

Three rules keep the list trustworthy:

- **Write only what the official page says.** If the page gives no amount, write "amount not stated". Please do not estimate.
- **Keep deadlines general.** Write the usual date or time of year ("February 1", "Mid-November"), and leave the year out. That way an entry stays right from one year to the next.
- **Give the date you checked** in `verified`.
- **Keep it short.** One sentence per cell, and no `|` characters.

If a text cell contains a comma, wrap the cell in double quotes, as the existing rows do. GitHub's table editor does this for you.

## Checking your change (optional)

With Python 3 installed:

```
python scripts/build_readme.py --check   # checks awards.csv
python scripts/build_readme.py           # also rebuilds README.md
```

The same check runs automatically on every pull request.

## For maintainers

- Merging a change to `awards.csv` triggers the "Build README" workflow, which rebuilds and commits `README.md`.
- The "Check links" workflow runs on the first day of each month and opens an issue listing links that no longer work.
- A full re-check of every entry once a year, in September, catches awards whose usual deadline has moved.

## Conduct

Be kind and assume good intent. This list exists to help people at the start of their careers.
