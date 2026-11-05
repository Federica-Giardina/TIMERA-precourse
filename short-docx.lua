-- Short Word version of the book: the text, equations and figures of the lectures,
-- without R code, printed output, practical sessions, exercises, solutions or
-- teaching plans. Active only when the metadata field `short-version` is true, e.g.
--   quarto render --to docx -M short-version:true      (see render-short-docx.py)
-- Has no effect on the normal HTML and Word versions.
--
-- Practical sessions are recognised by their identifiers (#sec-...-p1, #sec-...-p2).
-- The chapter "Introduction to R" (#sec-r) is reduced to its introduction and the
-- sections marked with the class .keep-short, which refer to existing R tutorials.

local short = false

local function starts_with(s, prefix)
  return s:sub(1, #prefix) == prefix
end

local function is_practical(id)
  return id ~= nil and id:match("%-p%d$") ~= nil
end

-- titles of boxes that are left out (English, French, Portuguese)
local dropped_titles = { "Solution", "Exercise", "Teaching plan",
                         "Exercice", "Plan d'enseignement",
                         "Exercício", "Solução", "Plano de ensino" }

local function dropped_title(title)
  local t = pandoc.utils.stringify(title or "")
  for _, prefix in ipairs(dropped_titles) do
    if starts_with(t, prefix) then return true end
  end
  return false
end

-- 1. Is this the short version?
local check = {
  Meta = function(meta)
    local v = meta["short-version"]
    short = v == true or (v ~= nil and pandoc.utils.stringify(v) == "true")
  end
}

-- 2. Remove practical sessions and shorten the chapter "Introduction to R".
local sections = {
  Pandoc = function(doc)
    if not short then return nil end
    local out = pandoc.List()
    local in_r, skip_level = false, nil
    for _, b in ipairs(doc.blocks) do
      if b.t == "Header" then
        if skip_level and b.level <= skip_level then skip_level = nil end
        if b.level == 1 then
          in_r = (b.identifier == "sec-r")
        elseif b.level == 2 and in_r and not b.classes:includes("keep-short") then
          skip_level = 2
        elseif b.level == 2 and is_practical(b.identifier) then
          skip_level = 2
        end
      end
      if not skip_level then out:insert(b) end
    end
    doc.blocks = out
    return doc
  end
}

-- 3. Remove code, output, boxes and references to the removed practical sessions.
local elements = {
  CodeBlock = function()
    if short then return {} end
  end,
  Div = function(el)
    if not short then return nil end
    if el.classes:includes("cell-output-stdout") or el.classes:includes("cell-output-stderr")
       or el.classes:includes("session-marker") then
      return {}
    end
  end,
  Callout = function(el)
    if short and dropped_title(el.title) then return {} end
  end,
  Cite = function(el)
    if short and #el.citations == 1 and is_practical(el.citations[1].id) then
      return pandoc.Str("the practical session (complete version)")
    end
  end,
  -- figures produced by R: smaller than in the complete version
  Image = function(el)
    if short and not el.attributes.width then
      el.attributes.width = "70%"
      return el
    end
  end
}

return { check, sections, elements }
