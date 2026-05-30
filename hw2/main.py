from pydantic import BaseModel, EmailStr, Field, model_validator, ValidationError


class Address(BaseModel):
    city: str = Field(min_length=2)
    street: str = Field(min_length=3)
    house_number: int = Field(gt=0)


class User(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(ge=0, le=120)
    email: EmailStr
    is_employed: bool = Field(description="User employment status", default=True)
    address: Address

    @model_validator(mode="after")
    def validate_age_and_employment(self):
        if self.is_employed and not (18 <= self.age <= 65):
            raise ValueError(
                "If the user is employed, their age must be between 18 and 65."
            )
        return self


def check_input(json_input):
    try:
        user = User.model_validate_json(json_input)
        return user.model_dump_json(indent=4)
    except ValidationError as error:
        return str(error)


if __name__ == '__main__':
    json_input = """{
        "name": "John Doe",
        "age": 70,
        "email": "john.doe@example.com",
        "is_employed": true,
        "address": {
            "city": "New York",
            "street": "5th Avenue",
            "house_number": 123
        }
    }"""

    print(check_input(json_input))