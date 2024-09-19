
- You can always talk to your Team Leader or the repo owner for any question regarding this project.

## Data model

The data model for this project is as follows:

```mermaid
classDiagram
User <|-- Collection
User <|-- Picture
PictureComment <|-- Picture
Contest <|-- Picture
Contest <|-- ContestSubmission
Contest <|-- User
ContestSubmission <|-- User
PictureComment <|-- User
Collection <|-- Picture
ContestSubmission <|-- Picture
Picture:
  +user: User
  +file: str
  +likes: List[User]
  +description: str

Comment:
  ...
```