from pydantic import BaseModel

creel_prj_cd_regex = r"[A-Z]{3}\_SC\d{2}\_[A-Z0-9]{3}"


class FNBase(BaseModel):
    class Config:
        anystr_strip_whitespace = True
        use_enum_values = True
        extra = "ignore"
