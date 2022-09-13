from pydantic import BaseModel, validator
from typing import Optional
from typing_extensions import Literal


ALTREF = Literal["A", "C", "G", "T", "."]


class Model(BaseModel):
    class Config:
        extra = "forbid"


class VariantQueryParams(Model):
    page: int
    ID: Optional[str]


class VariantInfo(Model):
    CHROM: str
    POS: int
    ALT: str
    REF: str
    ID: str


class VariantInput(Model):
    CHROM: str
    POS: int
    ALT: ALTREF
    REF: ALTREF
    ID: str

    @validator("CHROM")
    def parse_chrom(cls, chrom):
        assert chrom.startswith("chr")
        chrom_strip = chrom.strip("chr")
        try:
            assert int(chrom_strip) in range(1, 23)
        except ValueError:
            assert chrom_strip in ("X", "Y", "M")
        return chrom

    @validator("ID")
    def parse_id(cls, id):
        assert id.startswith("rs")
        id_strip = id.strip("rs")
        int(id_strip)
        return id
