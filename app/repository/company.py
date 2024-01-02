from app.model.company import Company



class CompanyRepository:

    _session = None

    def find_by_internal_company_name(self, company_name):
        return self._session.query(Company).filter_by(internal_company_name=company_name) \
            .first()

    def find_by_id(self, id):

        return self._session.query(Company).get(id)

    def get_by_internal_company_id(self, internal_company_id):
        # print("I AM FIND BY ID and MY ID IS: ", id)
        return self._session.query(Company).filter_by(internal_company_id=internal_company_id) \
            .first()

    def get_internal_company_by_name(self, internal_company_name):
        return self._session.query(Company).filter_by(internal_company_name=internal_company_name) \
            .first()

    def join_with_user(self, id):
        company = self._session.query(Company).filter_by(id=id).first()
        return company.users

    def join_with_car(self, id):
        company = self._session.query(Company).filter_by(id=id).first()
        return company.cars

    def set_session(self, db_session):
        if db_session:
            self._session = db_session

    def get_company_by_name(self, company_name):
        return self._session.query(Company).\
            filter(Company.internal_company_name.like(company_name)).\
            all()


    def create_new_company(self,
                           internal_company_name,
                           internal_company_id,
                           internal_company_balance_ref,
                           internal_company_status="Active"):

        self._session.add(Company(internal_company_name=internal_company_name,
                                  internal_company_id=internal_company_id,
                                  internal_company_balance_ref=internal_company_balance_ref,
                                  internal_company_status=internal_company_status))

        self._session.commit()


    def get_all_active_companies(self):
        return self._session.query(Company).\
            filter_by(internal_company_status='Active').\
            all()
