import datetime
import os

from sqlmodel import select

import reflex as rx

from .auth_session import AuthSession
from .user import User
from llama_index import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.readers import PDFReader
from llama_iris import IRISVectorStore

import getpass
import os
from dotenv import load_dotenv

load_dotenv(override=True)

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")

username = 'SUPERUSER'
password = 'SYS2' 
hostname = 'localhost' 
port = '1972' 
namespace = 'USER'
CONNECTION_STRING = f"iris://{username}:{password}@{hostname}:{port}/{namespace}"

pdf_path = os.path.join("treehacks2024/data", "OTHandbook.pdf")

ot_pdf = PDFReader().load_data(file=pdf_path)

vector_store = IRISVectorStore.from_params(
    connection_string=CONNECTION_STRING,
    table_name="OT_handbook",
    embed_dim=1536,  # openai embedding dimension
)

storage_context = StorageContext.from_defaults(vector_store=vector_store)
# service_context = ServiceContext.from_defaults(
#     embed_model=embed_model, llm=None
# )

index = VectorStoreIndex.from_documents(
    ot_pdf, 
    storage_context=storage_context, 
    show_progress=True, 
    # service_context=service_context,
)

query_engine = index.as_query_engine()

AUTH_TOKEN_LOCAL_STORAGE_KEY = "_auth_tokens"
DEFAULT_AUTH_SESSION_EXPIRATION_DELTA = datetime.timedelta(days=7)


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str

DEFAULT_CHATS = {
    "Intros": [],
}

class State(rx.State):
    # The auth_token is stored in local storage to persist across tab and browser sessions.
    auth_token: str = rx.LocalStorage(name=AUTH_TOKEN_LOCAL_STORAGE_KEY)

    chats: dict[str, list[QA]] = DEFAULT_CHATS

    # The current chat name.
    current_chat = "Intros"

        # The name of the new chat.
    new_chat_name: str = ""

    # Whether the drawer is open.
    drawer_open: bool = False

    # The current question.
    question: str

    chat: list[QA]

    # Whether we are processing the question.
    processing: bool = False

    # Whether the modal is open.
    modal_open: bool = False

    def reset_chat(self):
        self.chat = []
        self.processing = False

    def ensure_current_chat_initialized(self):
        """Ensure the current chat is initialized with at least one QA entry."""
        if self.current_chat not in self.chats:
            self.chats[self.current_chat] = []
        if not self.chats[self.current_chat]:
            # Append an empty QA object if the list is empty
            self.chats[self.current_chat].append(QA(question="", answer=""))

    async def process_question(self, form_data: dict[str, str]):
        # Get the question from the form
        question = form_data["question"]

        # Check if the question is empty
        if question == "":
            return

        async for value in self.openai_process_question(question):
            yield value

    async def openai_process_question(self, question: str):
        """Get the response from the API.

        Args:
            form_data: A dict with the current question.
        """
        # Add the question to the list of questions.
        qa = QA(question=question, answer="")
        self.chat.append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield

        # Build the messages.
        messages = [
            {"role": "system", "content": "You are a friendly chatbot named Reflex."}
        ]
        for qa in self.chat:
            messages.append({"role": "user", "content": qa.question})
            messages.append({"role": "assistant", "content": qa.answer})

        # Remove the last mock answer.
        messages = messages[:-1]

        user_messages = [msg for msg in messages if msg['role'] == 'user']
        print(user_messages)

        query_input = " ".join([msg["content"] for msg in user_messages])
        query_result = query_engine.query(query_input)
        print(query_result)
        
        """
        # Start a new session to answer the question.
        session = openai.ChatCompletion.create(
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            messages=messages,
            stream=True,
        )
        # Stream the results, yielding after every word.
        for item in query_result:
            if hasattr(item.choices[0].delta, "content"):
                answer_text = item.choices[0].delta.content
                self.chats[self.current_chat][-1].answer += answer_text
                self.chats = self.chats
                yield
        """ 
        self.ensure_current_chat_initialized()
        for word in query_result.response:
            # Construct the response incrementally. For example:
            self.chats[self.current_chat][-1].answer += word 
            self.chats = self.chats
            print(self.chats)
            yield

        # Toggle the processing flag.
        self.processing = False
        

    @rx.cached_var
    def authenticated_user(self) -> User:
        """The currently authenticated user, or a dummy user if not authenticated.

        Returns:
            A User instance with id=-1 if not authenticated, or the User instance
            corresponding to the currently authenticated user.
        """
        with rx.session() as session:
            result = session.exec(
                select(User, AuthSession).where(
                    AuthSession.session_id == self.auth_token,
                    AuthSession.expiration
                    >= datetime.datetime.now(datetime.timezone.utc),
                    User.id == AuthSession.user_id,
                ),
            ).first()
            if result:
                user, session = result
                return user
        return User(id=-1)  # type: ignore

    @rx.cached_var
    def is_authenticated(self) -> bool:
        """Whether the current user is authenticated.

        Returns:
            True if the authenticated user has a positive user ID, False otherwise.
        """
        return self.authenticated_user.id >= 0

    def do_logout(self) -> None:
        """Destroy AuthSessions associated with the auth_token."""
        with rx.session() as session:
            for auth_session in session.exec(
                AuthSession.select.where(AuthSession.session_id == self.auth_token)
            ).all():
                session.delete(auth_session)
            session.commit()
        self.auth_token = self.auth_token

    def _login(
        self,
        user_id: int,
        expiration_delta: datetime.timedelta = DEFAULT_AUTH_SESSION_EXPIRATION_DELTA,
    ) -> None:
        """Create an AuthSession for the given user_id.

        If the auth_token is already associated with an AuthSession, it will be
        logged out first.

        Args:
            user_id: The user ID to associate with the AuthSession.
            expiration_delta: The amount of time before the AuthSession expires.
        """
        if self.is_authenticated:
            self.do_logout()
        if user_id < 0:
            return
        self.auth_token = self.auth_token or self.get_token()
        with rx.session() as session:
            session.add(
                AuthSession(  # type: ignore
                    user_id=user_id,
                    session_id=self.auth_token,
                    expiration=datetime.datetime.now(datetime.timezone.utc)
                    + expiration_delta,
                )
            )
            session.commit()
