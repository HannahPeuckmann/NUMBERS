
## intent: yes
  - ja
  - richtig
  - das stimmt
  - ja, richtig
  - genau
  
## intent: no
  - ne
  - nein
  - falsch
  - fehler

## intent: ignore
  -[ok super](noise)
  -[dann fangen wir jetzt an oder?](noise)
  -[gut das habe ich verstanden](noise)

## intent: repeat
  - noch mal bitte
  - wie bitte?
  - was?
  - was muss ich machen?
  - kannst du das wiederholen bitte?
  - wiederholen bitte

## intent: help
  - hilfe
  - ich brauche hilfe


## regex: number
  -\d+

## regex: noise
  -(?!ja|richtig|das stimmt|genau|ja, richtig|nein|ne|falsch|Fehler|da ist ein Fehler|\d+|noch mal bitte|wie bitte\?|was\?|was muss ich machen\?|kannst du das wiederholen bitte\?|wiederholen bitte|hilfe|ich brauche hilfe)

## intent: transmit_number
  - [45](number)
  - [9](number)
  - [237](number)


