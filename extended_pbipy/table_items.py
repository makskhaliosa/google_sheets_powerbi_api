import json
from enum import Enum
from typing import Union


class Measure():

    """
    ### Overview
    ----
    Represents a `Measure` inside of a `PowerBiColumn`
    object.
    """

    def __init__(self, name: str, expression: str) -> None:
        """Initializes a new `Measure` object.

        ### Parameters
        -----
        name : str
            The measure name.

        expression : str
            A valid DAX expression.
        """

        self.measure = {
            'name': name,
            'expression': expression,
            'formatString': '',
            'isHidden': False,
        }

    @property
    def name(self) -> str:
        """The measure name.

        ### Returns
        ----
        str :
            The measure name.
        """
        return self.measure.get('name', None)

    @name.setter
    def name(self, name: str) -> None:
        """Sets the measure name.

        ### Parameters
        ----
        name : str
            The name you want the measure to be.
        """

        self.measure.update({'name': name})

    @property
    def expression(self) -> str:
        """Returns the measure DAX expression.

        ### Returns
        ----
        str :
            A valid DAX expression.
        """
        return self.measure.get('dataType', None)

    @expression.setter
    def expression(self, expression: str) -> None:
        """Sets the measure DAX expression.

        ### Parameters
        ----
        expression : str
            A valid DAX expression.
        """

        self.measure.update({'expression': expression})

    @property
    def format_string(self) -> str:
        """Returns the format string of the measure.

        ### Returns
        ----
        str :
            The format of the measure as specified in
            FORMAT_STRING.
        """
        return self.measure.get('formatString', None)

    @format_string.setter
    def format_string(self, format_string: str) -> None:
        """Sets the optional format of the measure.

        ### Parameters
        ----
        format_string : str
            The format of the measure as specified in
            FORMAT_STRING.
        """

        self.measure.update({'formatString': format_string})

    @property
    def is_hidden(self) -> bool:
        """Returns the property indicating if the measure
        is hidden from client tools.

        ### Returns
        ----
        bool :
            If `True` the measure is hidden, `False`
            otherwise.
        """
        return self.measure.get('isHidden', None)

    @is_hidden.setter
    def is_hidden(self, is_hidden: bool) -> None:
        """Sets the `isHidden` property of the column.

        ### Parameters
        ----
        is_hidden : bool
            Property indicating if the measure is hidden from
            client tools. Default is `False`.
        """

        self.measure.update({'isHidden': is_hidden})

    def to_dict(self) -> dict:
        """Returns the measure properties.

        ### Returns
        ----
        dict
            A dictionary containing each of the measure
            properties.
        """

        return self.measure

    def to_json(self) -> str:
        """Returns the measure properties as
        a JSON formatted string.

        ### Returns
        ----
        str
            A string that contains the measure
            properties.
        """
        return json.dumps(obj=self.measure, indent=4)


class Column():

    """
    ### Overview
    ----
    Represents a column inside of a `PowerBiTable`
    object.
    """

    def __init__(self, name: str, data_type: Union[str, Enum]) -> None:
        """Initializes a new `Column` object.

        ### Parameters
        ----
        name : str
            The column name.

        data_type : Union[str, Enum]
            One of the allowed data types.
        """

        if isinstance(data_type, Enum):
            data_type = data_type.value

        self.column = {
            'name': name,
            'dataType': data_type,
            'dataCategory': '',
            'formatString': '',
            'isHidden': False,
            'sortByColumn': None,
            'summarizeBy': None
        }

    @property
    def name(self) -> str:
        """The column name.

        ### Returns
        ----
        str :
            The column name.
        """
        return self.column.get('name', None)

    @name.setter
    def name(self, name: str) -> None:
        """Sets the column name.

        ### Parameters
        ----
        name : str
            The name you want the column to be.
        """

        self.column.update({'name': name})

    @property
    def data_type(self) -> str:
        """Returns the data type of column.

        ### Returns
        ----
        str :
            One of the allowed data types.
        """
        return self.column.get('dataType', None)

    @data_type.setter
    def data_type(self, data_type: Union[str, Enum]) -> None:
        """Sets the column data type.

        ### Parameters
        ----
        data_type : Union[str, Enum]
            One of the allowed data types.
        """

        if isinstance(data_type, Enum):
            data_type = data_type.value

        self.column.update({'dataType': data_type})

    @property
    def format_string(self) -> str:
        """Returns the format string of the column.

        ### Returns
        ----
        str :
            The format of the column as specified in
            FORMAT_STRING.
        """
        return self.column.get('formatString', None)

    @format_string.setter
    def format_string(self, format_string: str) -> None:
        """Sets the optional format of the column.

        ### Parameters
        ----
        format_string : str
            The format of the column as specified in FORMAT_STRING.
        """

        self.column.update({'formatString': format_string})

    @property
    def data_category(self) -> str:
        """Returns the data category of the column,
        if any is specified.

        ### Returns
        ----
        str :
            String value to be used for the data category
            which describes the data within this column.
        """
        return self.column.get('dataCategory', None)

    @data_category.setter
    def data_category(self, data_category: str) -> None:
        """Sets the data category of the column.

        ### Parameters
        ----
        data_category : str
            Value to be used for the data category which
            describes the data within this column. Some
            common values include: `[Address, City, Continent,
            Country, Image, ImageUrl, Latitude, Longitude,
            Organization, Place, PostalCode, StateOrProvince,
            WebUrl]`
        """

        self.column.update({'dataCategory': data_category})

    @property
    def is_hidden(self) -> bool:
        """Returns the property indicating if the column
        is hidden from view.

        ### Returns
        ----
        bool :
            If `True` the column is hidden, `False`
            otherwise.
        """
        return self.column.get('isHidden', None)

    @is_hidden.setter
    def is_hidden(self, is_hidden: bool) -> None:
        """Sets the `isHidden` property of the column.

        ### Parameters
        ----
        is_hidden : bool
            Property indicating if the column is hidden from view.
            Default is `False`.
        """

        self.column.update({'isHidden': is_hidden})

    @property
    def sort_by_column(self) -> str:
        """Returns the property indicating the column
        that the table is ordered by.

        ### Returns
        ----
        str :
            String name of a column in the same table to be
            used to order the current column.
        """
        return self.column.get('sortByColumn', None)

    @sort_by_column.setter
    def sort_by_column(self, sort_by_column: str) -> None:
        """Sets the `sortByColumn` property of the column.

        ### Parameters
        ----
        sort_by_column : str
            String name of a column in the same table to be
            used to order the current column.
        """

        self.column.update({'sortByColumn': sort_by_column})

    @property
    def summarize_by(self) -> str:
        """Returns the property indicating how the column
        is aggregated.

        ### Returns
        ----
        str :
            Aggregate Function to use for summarizing this
            column.
        """
        return self.column.get('summarizeBy', None)

    @summarize_by.setter
    def summarize_by(self, summarize_by: Union[str, Enum]) -> None:
        """Sets the `summarizeBy` property of the column.

        ### Parameters
        ----
        summarize_by : Union[str, Enum]
            Aggregate Function to use for summarizing this
            column.
        """

        if isinstance(summarize_by, Enum):
            summarize_by = summarize_by.value

        self.column.update({'summarizeBy': summarize_by})

    def to_dict(self) -> dict:
        """Returns the column properties.

        ### Returns
        ----
        dict
            A dictionary containing each of the column
            properties.
        """
        return self.column

    def to_json(self) -> dict:
        """Returns the column properties as a JSON string.

        ### Returns
        ----
        dict
            A string containing each of the column
            properties.
        """
        return self.column
