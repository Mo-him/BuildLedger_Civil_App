from sqlalchemy.orm import Session

from app.repositories.master_repository import master_repository


class MasterService:

    @staticmethod
    def get_party_types(db: Session):
        return master_repository.get_party_types(db)

    @staticmethod
    def get_bill_types(db: Session):
        return master_repository.get_bill_types(db)

    @staticmethod
    def get_units(db: Session):
        return master_repository.get_units(db)

    @staticmethod
    def get_deduction_types(db: Session):
        return master_repository.get_deduction_types(db)

    @staticmethod
    def get_tax_types(db: Session):
        return master_repository.get_tax_types(db)


master_service = MasterService()