import logging

from memex.utils import load_module

from .config import read_config
from .errors import InvalidKeywordException
from .main import create_session
from .models import EntryModel


def create_entry(entry_dict, options=[]):
    try:

        # TEMPORARLIY TURN OFF OPTION-HANDLING

        # First generate options using user-provided function
        # conf = read_config()
        # option_gen = conf['option-provider'].get('option-gen', '')
        # if option_gen:
        #     option_gen_func = load_module(option_gen)
        #     new_opts = option_gen_func(entry_dict)
        #     if type(new_opts) != list:
        #         raise Exception(f"Return value of function at '{option_gen}' is not a list")
        #     options.extend(new_opts)

        # for option in options:
        #     option_handler_file = conf['option-provider'].get(option, '')
        #     if not option_handler_file:
        #         print(f"option handler not found for '{option}'. skipping...")
        #         continue
        #     option_handler = load_module(option_handler_file)
        #     entry_dict = option_handler(entry_dict)

        attribs = ["url", "keywords"]
        kwargs = {k: entry_dict[k] for k in attribs}
        return EntryModel(**kwargs)
    except InvalidKeywordException as e:
        print("invalid keywords")
    except Exception as e:
        print("something went wrong..", e)
    return None


def save_entry(entry):
    try:
        session = create_session()
        session.add(entry)
        session.commit()

        session.refresh(entry)
        logging.info(f"Saved entry to database [{entry.id}]")

        return True
    except Exception as e:
        print("something went wrong")
        return False


def list_entries():
    try:
        session = create_session()
        return session.query(EntryModel).all()
    except Exception as e:
        print("something went wrong...", e)


def find_entry(id_):
    try:
        session = create_session()
        return session.query(EntryModel).filter(EntryModel.id == id_).first()
    except Exception as e:
        print("something went wrong...", e)
    return None
