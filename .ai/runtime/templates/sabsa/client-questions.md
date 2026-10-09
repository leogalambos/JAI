{{! The open assumptions as a short, client-facing list. Edit or replace like any template. }}
# Questions for {{library.organisation}}

**{{library.name}}** · {{generated}}

To finish the security architecture for {{library.scope}}, we need to confirm the following. Each item is
something the architecture currently assumes; your answer either confirms it or tells us what is actually the case.

{{#has_questions}}
{{#questions}}
{{n}}. **{{title}}**
   We assumed: {{assumption}}
   {{#is_attribute}}Is the target *{{target}}* for *{{metric}}* right for you?{{/is_attribute}}

{{/questions}}
{{/has_questions}}
{{^has_questions}}
Nothing is open: every element rests on material you provided.
{{/has_questions}}
{{#open_cells}}
In addition, {{open_cells}} of the 36 questions of the architecture are not yet answered; we will come back to
those as the work proceeds.
{{/open_cells}}
