-- SPDX-License-Identifier: BSD-4-Clause
-- Copyright (c) 2026 Leo Galambos and the Egothor team
-- Keep catalogue headings with landscape tables, including repeated longtable headers.
function Pandoc(document)
  local blocks = pandoc.List()
  for _, block in ipairs(document.blocks) do
    if block.t == 'Table' then
      local count = #block.colspecs
      for index, spec in ipairs(block.colspecs) do
        spec[2] = count == 1 and 1 or (index == 1 and 0.10 or 0.90 / (count - 1))
      end
      if FORMAT:match('latex') and count >= 5 then
        local heading = nil
        if #blocks > 0 and blocks[#blocks].t == 'Header' then
          heading = blocks:remove(#blocks)
        end
        blocks:insert(pandoc.RawBlock('latex', '\\begin{landscape}'))
        if heading then blocks:insert(heading) end
        blocks:insert(block)
        blocks:insert(pandoc.RawBlock('latex', '\\end{landscape}'))
      else
        blocks:insert(block)
      end
    else
      blocks:insert(block)
    end
  end
  document.blocks = blocks
  return document
end
