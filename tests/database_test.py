from app.repository.keywords import KeywordsRepo
import sqlalchemy
from sqlalchemy.orm import sessionmaker

keyword_repo = KeywordsRepo()

keyword_repo.set_session(sessionmaker(sqlalchemy.create_engine(""))())

print(keyword_repo.get_current_keyword()[0].week_no)
