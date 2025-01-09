from app.models import CharityProject, Donation

from .charity_project import CRUDCharityProject
from .donation import CRUDDonation

project_crud = CRUDCharityProject(CharityProject)
donation_crud = CRUDDonation(Donation)