"""
__init__ — three isolated dicts, three counters, verified independence between instances
create_document — verified id assignment, counter increment, storage
create_ticket — verified default status, optional related_document_id, id assignment
create_comment — verified the foreign-key existence check (a real "prevent silent failures"
 edge case you can point to directly in your presentation), plus the URL-path ticket_id pattern
"""
from app.models.document import Document, DocumentCreate
from app.models.ticket import Ticket, TicketCreate
from app.models.comment import Comment, CommentCreate
class DataStore:
    def __init__(self):
        self.documents: dict[int, Document] = {}
        self.comments: dict [int, Comment] = {}
        self.tickets: dict[int, Ticket] = {}
        self._document_counter: int = 1
        self._comment_counter: int = 1
        self._ticket_counter: int = 1
   
    #combine documentCreate with 
    #store assigned fields to build
    # and save a full document 
    #id for document get set here 
    def create_document(self, data: DocumentCreate)-> Document:
        new_id = self._document_counter
        new_document = Document(id=new_id, title=data.title, category=data.category, body=data.body, owner_id=data.owner_id)
        self.documents[new_id] = new_document
        self._document_counter += 1
        return new_document

    def create_ticket(self, data: TicketCreate)-> Ticket:
        new_id = self._ticket_counter
        new_ticket = Ticket(id = new_id, title = data.title, priority = data.priority, assignee_id = data.assignee_id, related_document_id = data.related_document_id)
        self.tickets[new_id] = new_ticket
        self._ticket_counter += 1
        return new_ticket

    def create_comment(self, ticket_id: int, data: CommentCreate)-> Comment:
        #key guard for given ticket_id doesn't exist 
        if ticket_id not in self.tickets:
            raise ValueError(f"No ticket with id {ticket_id} exists")        
        new_id = self._comment_counter
        new_comment = Comment(id = new_id, author_id = data.author_id, body = data.body, ticket_id = ticket_id)
        self.comments[new_id] = new_comment
        self._comment_counter += 1
        return new_comment 
    #.get is built into python dictionaries
    def get_document(self, document_id: int)-> Document | None:
        return self.documents.get(document_id)

    def get_ticket(self, ticket_id: int)-> Ticket | None:
        return self.tickets.get(ticket_id)

    def get_comment(self, comment_id: int)-> Comment | None:
        return self.comments.get(comment_id)

    #values() built into dicts to get all values of dictionary 
    def list_documents(self) -> list[Document]:
        return list(self.documents.values())

    def list_tickets(self)-> list[Ticket]:
        return list(self.tickets.values())

    def list_comments(self)-> list[Comment]:
        return list(self.comments.values())
