# Exploratory research: the research library

For research that looks **beyond the current version** (new directions, adjacent fields, ideas a person wants explored), as opposed to research that tests a design assumption. A ticket is exploratory when its description has the line `Track: exploratory`. `research-question` then follows this file.

## Set up (once per project, by a person or the first exploratory ticket)
- A Notion page `<Project> - Research library` under the Notion home: a short intro, how to read a page (the four evidence tags below), a **Themes** list and a **Recently added** list (10 newest).
- One child page per theme (`Theme: <name>`), each with a one-line scope and a **Pages** list.
- Add `Library: <URL>` to the Linear project description, below the other contract lines.
- Add the select option `Future version` to the findings database's Status.

## Ticket contract
Description: the question; "A good answer lets us decide"; then the lines `Track: exploratory`, `Theme: <theme page title>`, `Research depth: <n>`, `Library: <URL>`, and for follow-ups `Parent: <ticket ID>`.

## Scope
- Never changes the current design, its requirements or its tickets. Findings rows use Status **Future version**, never `New`, so the design loop does not revise from them. A person asks for a next-version design when they want one.
- Public desk research only (the research-question rules on contacting people apply).

## Investigate
As research-question step 2, plus:
- **Evidence ladder**, strongest first: systematic reviews and meta-analyses; randomized trials; controlled or longitudinal studies; qualitative studies and surveys; practitioner and expert writing; user accounts. Say which rung each claim stands on, and report what makes it trustworthy or not: sample size, effect size, comparison group, replication, preregistration, conflicts of interest.
- For a therapy, faith or philosophical tradition: describe it as its own serious practitioners and primary texts do, then separately say what outside evidence shows. Never rank traditions or judge their truth.
- Laws, regulations and product facts: current official sources, dated.

## Write the page (the main output)
A child of the theme page, titled with the topic in plain words, for a smart reader with no background in the field, on a phone: short paragraphs, plain words, examples, about 1,200 to 2,500 words. Outline:
1. **At a glance**: 3 to 5 bullets a reader could stop after.
2. **Why this matters for the app**.
3. **Key ideas, explained**, each with a concrete example from the app's world; a small table where it helps.
4. **What the evidence says**: each claim tagged **Strong** (systematic reviews or several good trials agree), **Moderate** (some trials or consistent studies), **Early** (small, few or uncontrolled studies) or **Speculative** (theory, practitioner experience, our reasoning), with its source linked.
5. **Where people disagree**.
6. **What this could mean for the app**: 2 to 4 options with trade-offs, not decisions.
7. **Risks and ethics**.
8. **Open questions**, each linked to its follow-up ticket or marked "not filed" with the reason.
9. **Related pages** (Notion mentions).
10. **Start here**: the 3 best sources to go deeper, approachable to expert.
11. **Sources**.

When a topic splits into distinct parts that each deserve an explanation (one tradition, model or component each), give each part a child page in the same outline, shorter, and link siblings to each other. Research only people can do gets a **Research guide for humans** section and one `Needs human research` row; people add their results as `Future version` rows, not `New`.

## Findings rows
1 to 5 rows: one claim each, honest Source type and Confidence, Evidence = the page URL, Implication = what it might mean for a future version, Status **Future version**.

## Follow-ups (the library grows itself)
1. From the Open questions, pick at most **3** that matter most for the app and that no library page or research ticket in the project (any state; search titles) already covers.
2. File none, marking them "not filed: depth limit" or "not filed: queue full", when this ticket's `Research depth:` is 3 or more (a missing line counts as 1), or when the project already has 20 or more open exploratory tickets.
3. Otherwise create each as a `research` ticket: same project, priority Low, state Todo, related to this ticket, with the ticket contract above, depth + 1.

## Close
Add the page to its theme's **Pages** list (one line on what it covers) and to the top of **Recently added**. Comment on the ticket: page link, one-line answer, confidence, rows added, follow-ups filed. Set it Done.
