from typing import Any, Dict, Final, Tuple, Union

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import (
    CheckConstraint,
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    SchemaItem,
)
from sqlalchemy.sql.sqltypes import String

from ...._mixins import Timestamped
from ....base_interface import Base
from ....misc.locales.locale_model import LocaleModel
from .company_bonus_category_model import CompanyBonusCategoryModel


class CompanyBonusCategoryLocaleModel(Timestamped, Base):
    category_id: Final[Column[str]] = Column(
        CompanyBonusCategoryModel.id.type,
        ForeignKey(
            CompanyBonusCategoryModel.id,
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        primary_key=True,
    )
    locale_language_code: Final[Column[str]] = Column(
        LocaleModel.language_code.type,
        primary_key=True,
    )
    locale_country_code: Final[Column[str]] = Column(
        LocaleModel.country_code.type,
        primary_key=True,
    )

    name: Final[Column[str]] = Column(
        String(255),
        CheckConstraint("name <> ''"),
        nullable=False,
    )

    locale: Final['RelationshipProperty[LocaleModel]'] = relationship(
        'LocaleModel',
        back_populates='company_bonus_category_locales',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    category: Final[
        'RelationshipProperty[CompanyBonusCategoryModel]'
    ] = relationship(
        'CompanyBonusCategoryModel',
        back_populates='locales',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )

    __table_args__: Final[Tuple[Union[SchemaItem, Dict[str, Any]]]] = (
        ForeignKeyConstraint(
            [locale_language_code, locale_country_code],
            [LocaleModel.language_code, LocaleModel.country_code],
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
    )
