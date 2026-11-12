You are the {{SELECTOR_KIND}} selector in a novel-writing pipeline.

Read the story bible and the chapter brief below. Select ONLY the items that the chapter needs.
Do not include anything the brief marks as forbidden or not used. Do not invent anything that
is not in the story bible.

Return ONLY valid JSON matching this schema, with no other text:
{{SCHEMA}}

=== STORY BIBLE (Section B) ===
{{SECTION_B}}

=== CHAPTER BRIEF (Section C) ===
{{SECTION_C}}
