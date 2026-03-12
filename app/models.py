from pydantic import BaseModel, Field
from typing import List

class ResourceAssessmentRequest(BaseModel):
    resource_identifier: str = Field(
        ...,
        description="Identifier of the resource to assess",
        example="https://github.com/oeg-upm/rsfc"
    )


class IndicatorIdentifier(BaseModel):
    identifier: str


class Assessment(BaseModel):
    context: str
    type: str
    name: str
    description: str
    dateCreated: str
    license: dict
    assessedSoftware: dict
    checks: list
