# A row's state holds its own fields

Skill: conventions
Fixture: an app on build-kit, arch-kit and paging-kit with a `features/chat` feature whose domain has a
`ChatMessage` (`id`, `author`, `text`, `sentAt`, `isRead`) and no screen yet

## Prompt
Add a paged chat messages screen to the chat feature: each row shows the author, the text, the time and an
unread dot.

## Passes when
- the row's state class sits in the row's file under `components/` and its fields are flat: no field's type
  is a class from a `model/` package (`grep -n "import .*\.model\." <row file>` finds none, or only an enum)
- the list's state holds `PagingState<…RowState>`, not `PagingState<ChatMessage…>` of a presentation model
- no `model/` class is written for the message unless more than one state holds it or the Logic uses it

## Runs
| Date | Model | Without the skill | With it |
|---|---|---|---|
