from __future__ import annotations

import marshmallow.fields as mf
import marshmallow.validate as mv
from marshmallow_dataclass import dataclass

from typing import List, Dict, Union, Literal, Annotated

@dataclass
class Constant():
    constant: str

@dataclass
class LocatorData():
    path: Union[str, Constant]
    type: Literal['dimension', 'attribute', 'variable']
    attr: Literal['value', 'type', 'length', 'name']
    index: List[int] = None

@dataclass
class Locator():
    locator: LocatorData

@dataclass
class Range():
    min: Union[int, float, Locator, Constant] = None
    max: Union[int, float, Locator, Constant] = None

@dataclass
class ValueExpander():
    re: Union[str, Constant]
    comparator: ValueComparator
    cast: Literal['int', 'float'] = None

@dataclass
class UdunitsCheck():
    is_valid: bool = True
    is_calendartime: bool = False
    is_dimensionless: bool = False
    is_latitude: bool = False
    is_longitude: bool = False
    is_pressure: bool = False
    is_reftime: bool = False
    is_time: bool = False

@dataclass
class Finder():
    variable: SchemaMatch = None
    attribute: SchemaMatch = None
    dimension: SchemaMatch = None
    token: Union[str, Constant] = '$VALUE'
    count: Union[int, float, Constant] = None

@dataclass
class ValueComparator():
    range: Union[Range, List[int], List[float]] = None
    neq: Union[Locator, str, int, float, Constant] = None
    choice: Union[List[str], List[int], List[float], Constant] = None
    contains: Union[Locator, str, int, float, List[int], List[float], Constant] = None
    gt: Union[Locator, str, int, float, Constant] = None
    gte: Union[Locator, str, int, float, Constant] = None
    lt: Union[Locator, str, int, float, Constant] = None
    lte: Union[Locator, str, int, float, Constant] = None
    neq: Union[Locator, str, int, float, Constant] = None
    udunits: UdunitsCheck = None
    re: Union[str, Constant] = None
    find: Finder = None
    parse: ValueExpander = None
    monotonic: bool = None

@dataclass
class CountOperator():
    operator: Literal['<', '<=', '>', '>=']
    value: Union[int, Constant]

@dataclass
class SchemaMatch():
    name: Union[ValueComparator, Locator, str, Constant] = None
    type: Union[ValueComparator, Locator, str, Constant] = None
    value: Union[ValueComparator, Locator, str, int, float, Constant] = None
    
    dimensions: List[SchemaMatch] = None
    attributes: List[SchemaMatch] = None

    unique_dimensions: bool = None
    attributes_count: Union[ValueComparator, Locator, int, Constant] = None
    dimensions_count: Union[ValueComparator, Locator, int, Constant] = None
    length: Union[ValueComparator, Locator, int, Constant] = None

@dataclass
class SchemaNegator():
    negated: Union[SchemaMatch, SchemaConnector]

@dataclass
class SchemaConnector():
    connector:  Literal['AND', 'OR']
    statements: List[Union[SchemaMatch, SchemaNegator, SchemaConnector]]

@dataclass
class Item():
    criteria: Union[SchemaMatch, SchemaNegator, SchemaConnector] = None
    schema: Union[SchemaMatch, SchemaNegator, SchemaConnector] = None
    count: Union[int, CountOperator, Constant] = None
    severity: Literal['error', 'warning', 'info'] = 'error'
    comments: Union[str, List[str], Constant, List[Constant]] = None

@dataclass
class GroupSchema():
    name: str
    attributes: List[Item] = None
    dimensions: List[Item] = None
    variables: List[Item] = None

@dataclass
class NetCDFSchema():
    groups: List[GroupSchema]
    constants: Dict[str, Union[str, float, int, List[str], List[int], List[float]]]
    netcdf_schema_version: Literal['1.0']

    def validate(file : str) -> tuple[bool, dict]:
        pass