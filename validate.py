from src.netcdf_schema.schema import NetCDFSchema
from marshmallow import ValidationError

import pprint

import yaml
import sys

def main():
    try:
        input = sys.argv[1]
    except IndexError:
        print('Please provide a .yml file')
        return

    with open(input) as f:
        data = yaml.safe_load(f)
    try:
        parsed = NetCDFSchema.Schema().load(data)
    except ValidationError as err:
        pprint.pprint(err.messages)

if __name__ == '__main__':
    main()


