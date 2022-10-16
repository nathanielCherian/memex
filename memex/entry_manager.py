import logging

from memex.session import BaseSession

from .errors import InvalidKeywordException, handle_error
from .models import EntryModel


class EntryManager(BaseSession):
    INPUTS = ["url", "keywords"]

    def create_entry(self, entry_dict):
        try:
            self.create_session()
            kwargs = {k: entry_dict[k] for k in self.INPUTS}
            return EntryModel(**kwargs)
        except InvalidKeywordException as e:
            print("invalid keywords.")
        except Exception as e:
            handle_error("Unable to create entry.", e)

    def save_entry(self, entry):
        try:
            self.create_session()
            self.session.add(entry)
            self.session.commit()
            self.session.refresh(entry)
            logging.info(f"Saved entry to database [{entry.id}]")
            return True
        except Exception as e:
            handle_error("Unable to save entry.", e)
            return False

    def list_entries(self):
        try:
            self.create_session()
            return self.session.query(EntryModel).all()
        except Exception as e:
            handle_error("Unable to fetch entries.", e)

    def find_entry(self, id_):
        try:
            self.create_session()
            return self.session.query(EntryModel).filter(EntryModel.id == id_).first()
        except Exception as e:
            handle_error("Unable to find entry.", e)
