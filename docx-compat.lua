-- Adjustments for the Word (docx) version of the book, which is produced for sharing.
-- Has no effect on the HTML version.

if FORMAT:match("html") then
  return {}
end

-- Links to the lecture slides (HTML files next to the book) do not work in a Word
-- document: keep the link text only.
-- The same applies to links to the other language versions (../fr/, ../pt/, ...).
function Link(el)
  if el.target:match("^slides/.*%.html") or el.target:match("^%.%./") then
    return el.content
  end
end

-- Flow diagrams are SVG files; Word uses the PNG copies made by images/svg_to_png.py.
function Image(el)
  if el.src:match("^images/.*%.svg$") then
    el.src = el.src:gsub("%.svg$", ".png")
    return el
  end
end

-- Raw HTML is dropped in Word: <br> becomes a line break, and <code>...</code>
-- (used where a "|" must appear inside a table cell) becomes inline code.
function Inlines(inlines)
  local out = pandoc.List()
  local i = 1
  while i <= #inlines do
    local el = inlines[i]
    if el.t == "RawInline" and el.format == "html" then
      if el.text:match("^<br%s*/?>$") then
        out:insert(pandoc.LineBreak())
        i = i + 1
      elseif el.text == "<code>" then
        local j = i + 1
        local parts = pandoc.List()
        while j <= #inlines and not (inlines[j].t == "RawInline" and inlines[j].text == "</code>") do
          parts:insert(inlines[j])
          j = j + 1
        end
        out:insert(pandoc.Code(pandoc.utils.stringify(parts)))
        i = j + 1
      else
        i = i + 1
      end
    else
      out:insert(el)
      i = i + 1
    end
  end
  return out
end
