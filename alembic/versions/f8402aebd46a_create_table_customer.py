"""create table customer

Revision ID: f8402aebd46a
Revises: 
Create Date: 2023-09-27 19:55:38.087423

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from faker import Faker
import random

faker = Faker('id_ID')
Faker.seed(4321)

# Generate custom NIK and Bank Account Provider
from faker.providers import BaseProvider

class ProviderNIK(BaseProvider):
    def nik_provider(self) -> str:
        nik = []
        for _ in range(16):
            x = random.randint(0, 9)
            nik.append(str(x))
        return ''.join(nik)
    
class ProviderBA(BaseProvider):
    def ba_provider(self) -> str:
        ba = ['232']
        for _ in range(5):
            x = random.randint(0, 9)
            ba.append(str(x))
        return ''.join(ba)

# Adding newly-created Providers to faker
faker.add_provider(ProviderNIK)
faker.add_provider(ProviderBA)


# revision identifiers, used by Alembic.
revision: str = 'f8402aebd46a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    customer = op.create_table(
        'm_customer',
        sa.Column('id_customer', sa.Integer, primary_key=True),
        sa.Column('norek_customer', sa.CHAR(8), nullable=False, unique=True),
        sa.Column('nama_customer', sa.String(255), nullable=False),
        sa.Column('nik_customer', sa.CHAR(16), nullable=False),
        sa.Column('hp_number_customer', sa.String(50), nullable=False),
        sa.Column('saldo_customer', sa.Integer, default=0)
    )

    op.bulk_insert(
        customer,
        [{
            'nama_customer': faker.name(),
            'norek_customer': faker.ba_provider(),
            'nik_customer': faker.nik_provider(),
            'hp_number_customer': faker.phone_number(),
            'saldo_customer': random.randrange(500000, 10000000, 10000)
        } for _ in range(100)]
    )


def downgrade():
    op.drop_table('m_customer')
