from sqlmodel import Field

import reflex as rx

class WillState(rx.Model, table=True):
    """Handle will form submission and redirect to dashboard page after submission."""

    username: str = Field()
    executor: str = Field()
    alternate_executor: str = Field()
    beneficiaries: str = Field()
    funeral_arrangements: str = Field()
    assets: str = Field()
    residuary_beneficiary: str = Field()

