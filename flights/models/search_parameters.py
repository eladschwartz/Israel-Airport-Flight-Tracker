from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date


class SearchParameters(BaseModel):
    flight_option: str  = Field(..., description="arrivals or departure")
    city: str | None = Field(None, description="city name")
    country: str | None = Field(None, description="country name")
    airline_compnay : str | None = Field(None, description="airline name")
    from_date: str | None = Field(None, description="From date in DD/MM/YYYY format")
    to_date: str | None = Field(None, description="To date date in DD/MM/YYYY format")
    with_filter: bool = Field(...,description="if user want to filter or just get all the flights without filters")

    
model_config = {
        "validate_assignment": True,
        "extra": "forbid",
    }
    
@field_validator('from_date', 'to_date')
@classmethod
def validate_date_format(cls, v: str) -> str:
        try:
            datetime.strptime(v, '%d-%m-%Y')
            return v
        except ValueError:
            raise ValueError(f"Date '{v}' is not in DD/MM/YYYY  format")
    
    
@field_validator('from_date, to_date')
@classmethod
def validate_not_in_past(cls, v: str) -> str:
        date_to_check = datetime.strptime(v, '%d-%m-%Y').date()
        today = date.today()
        if date_to_check < today:
            raise ValueError("Date cannot be in the past")
        return v