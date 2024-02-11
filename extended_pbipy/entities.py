import json
from enum import Enum
from typing import Dict, Union

from .entity_managers import Columns, DataSources, Measures, Tables
from .table_items import Column, Measure


class PowerBiEncoder(json.JSONEncoder):

    def __init__(self, *args, **kwargs):
        json.JSONEncoder.__init__(self, *args, **kwargs)

    def default(self, obj):
        if isinstance(obj, Columns):
            return obj.columns
        elif isinstance(obj, Measures):
            return obj.measures
        if isinstance(obj, Column):
            return obj.column
        elif isinstance(obj, Measure):
            return obj.measure
        elif isinstance(obj, DatasetCreate):
            return obj.push_dataset
        elif isinstance(obj, Tables):
            return obj.tables
        elif isinstance(obj, Table):
            return obj.table
        # elif isinstance(obj, Relationships):
        #    return obj.relationships
        # elif isinstance(obj, Relationship):
        #    return obj.relationship
        elif isinstance(obj, DataSources):
            return obj.datasources
        elif isinstance(obj, DataSource):
            return obj.data_source


class DatasourceConnectionDetails:
    '''The Power BI data source connection details.'''
    def __init__(
            self,
            account: str = None,
            classInfo: str = None,
            database: str = None,
            domain: str = None,
            emailAddress: str = None,
            kind: str = None,
            loginServer: str = None,
            path: str = None,
            server: str = None,
            url: str = None
    ):
        self.url = url


class DataSource:
    '''A Power BI data source.'''

    def __init__(
            self,
            data_source_type: Union[str, Enum],
            connection_details: Dict = None
    ) -> None:
        """Initializes the `DataSource` object.

        ### Parameters
        ----
        data_source_type : Union[str, Enum]
            The datasource type, can also be a `DataSourceType`
            enum.
        """

        if isinstance(data_source_type, Enum):
            data_source_type = data_source_type.value

        self.data_source_type = data_source_type

        self.connection_details = {}
        if connection_details:
            self.connection_details = connection_details

        self.data_source = {
            'datasourceType': self.data_source_type,
            'connectionDetails': self.connection_details,
            'dataSourceId': '',
            'gatewayId': ''
        }

    @property
    def data_source_type(self) -> str:
        """Gets the `dataSourceType` property.

        ### Returns
        ----
        str :
            The `dataSourceType` property.
        """
        return self.data_source.get('datasourceType', None)

    @data_source_type.setter
    def data_source_type(self, data_source_type: str) -> None:
        """Sets the `dataSourceType` property.

        ### Parameters
        ----
        data_source_type : str
            The `dataSourceType` with the properties set.
        """

        self.data_source.update({'datasourceType': data_source_type})

    @property
    def connection_details(self) -> str:
        """Gets the `connectionDetails` property.

        ### Returns
        ----
        str :
            The `connectionDetails` property.
        """
        return self.data_source.get('connectionDetails', None)

    @connection_details.setter
    def connection_details(self, connection_details: str) -> None:
        """Sets the `connectionDetails` property.

        ### Parameters
        ----
        connection_details : str
            The `connectionDetails` with the properties set.
        """

        self.data_source.update({'connectionDetails': connection_details})

    def to_dict(self) -> dict:
        """Converts the Object to dict.

        ### Returns
        ----
        dict:
            The resource itself as a dictionary.
        """

        return self.data_source

    def to_json(self) -> str:
        """Converts the Object to JSON string.

        ### Returns
        ----
        str:
            The resource itself as a JSON string.
        """

        return json.dumps(obj=self.data_source, cls=PowerBiEncoder)


class Table():

    """
    ### Overview
    ----
    Represents a Table inside of a PowerBi
    dataset.
    """

    def __init__(self, name: str) -> None:
        """Initializes the `Table` object.

        ### Parameters
        ----
        name : str
            User defined name of the table.
            It is also used as the identifier
            of the table.
        """

        self._columns = Columns()
        self._measures = Measures()

        self.table = {
            'name': name,
            'columns': self._columns,
            'measures': self._measures,
            'rows': []
        }

    def __repr__(self) -> str:
        """Represents the string representation of the
        table object.

        ### Returns
        ----
        str
            A JSON formatted string.
        """

        return json.dumps(obj=self.table, indent=4, cls=PowerBiEncoder)

    def __getitem__(self, index: int) -> object:
        return self.table[index]

    def __delitem__(self, index: int) -> None:
        del self.table[index]

    def __iter__(self):
        return iter(self.table)

    @property
    def name(self) -> str:
        """The table name.

        ### Returns
        ----
        str :
            User defined name of the table.
            It is also used as the identifier
            of the table.
        """
        return self.table.get('name', None)

    @name.setter
    def name(self, name: str) -> None:
        """Sets the table name.

        ### Parameters
        ----
        name : str
            User defined name of the table.
            It is also used as the identifier
            of the table.
        """

        self.table.update({'name': name})

    @property
    def columns(self) -> str:
        """Gets the `columns` property.

        ### Returns
        ----
        str :
            Collection of `Column` objects.
        """

        return self._columns

    def add_column(self, column: Column) -> None:
        """Adds a new `Column` to the `Columns`
        collection.

        ### Parameters
        ----
        column : Column
            A `Column` object with the properties
            set.
        """

        self._columns[len(self._columns)] = column

    def get_column(self, index: int) -> Column:
        """Gets a `Column` from the `Columns`
        collection.

        ### Parameters
        ----
        index : int
            The index of the column you want
            to return from the collection.

        ### Returns
        ----
        Column :
            A `PowerBiColumn` object.
        """

        return self._columns[index]

    def del_column(self, index: int) -> None:
        """Deletes a `Column` to the `Columns`
        collection.

        ### Parameters
        ----
        index : int
            The index of the column you want
            to delete from the collection.
        """

        del self._columns[index]

    @property
    def measures(self) -> str:
        """Gets the `measures` property.

        ### Returns
        ----
        str :
            Collection of `measure` objects.
        """

        return self._measures

    @property
    def add_measure(self, measure: Measure) -> None:
        """Adds a column to the `measures` collection.

        ### Parameters
        ----
        measure : measure
            A `Measure` object with the properties
            set.
        """

        measures = self.table.get('measures', [])
        measures.append(measure)

    def del_measure(self, index: int = 0) -> None:
        """Deletes a `Measure` in the `measures` collection.

        ### Parameters
        ----
        index : int (optional=, Default=0)
            The index of the `Measure` object
            that you wish to delete.
        """

        measures = self.table.get('measures', [])
        measures.pop(index)

    def get_measure(self, index: int = 0) -> Column:
        """Gets a `Measure` in the `measures` collection by
        indexing it.

        ### Parameters
        ----
        index : int (optional=, Default=0)
            The index of the `Measure` object
            that you wish to get.
        """

        return self.table.get('measures', [])[index]

    @property
    def rows(self) -> str:
        """Gets the `rows` property.

        ### Returns
        ----
        str :
            Collection of `row` objects.
        """

        return self.table.get('rows', [])

    def add_row(self, row: Union[list, dict]) -> None:
        """Adds a `Row` object to the `rows` collection.

        ### Parameters
        ----
        row : dict
            A `Row` object with the properties
            set.
        """

        rows = self.table.get('rows', [])

        if isinstance(row, dict):
            rows.append(row)
        elif isinstance(row, list):
            rows.extend(row)

    def del_row(self, index: int = 0) -> None:
        """Deletes a `Row` in the `rows` collection.

        ### Parameters
        ----
        index : int (optional=, Default=0)
            The index of the `Row` object
            that you wish to delete.
        """

        rows = self.table.get('rows', [])
        rows.pop(index)

    def get_row(self, index: int = 0) -> dict:
        """Gets a `Row` in the `rows` collection by
        indexing it.

        ### Parameters
        ----
        index : int (optional=, Default=0)
            The index of the `Row` object
            that you wish to get.
        """

        return self.table.get('rows', [])[index]

    def to_dict(self) -> dict:
        return json.loads(s=json.dumps(obj=self.table, cls=PowerBiEncoder))

    def to_json(self) -> dict:
        return json.dumps(obj=self.table, cls=PowerBiEncoder)


class DatasetCreate:
    '''Класс с параметрами для создания датасета.'''

    def __init__(self, name: str, tables: Tables = None) -> None:
        """Initializes the `Dataset` object.

        ### Parameters
        ----
        name : str
            User defined name of the dataset.
            It is also used as the identifier
            of the dataset.

        tables : Tables (optional, Default=[])
            A collection of `Table` objects
            you want to be part of the dataset.
        """

        if tables is None:
            self._tables = Tables()
        else:
            self._tables = tables

        # self._relationships = Relationships()
        self._data_sources = DataSources()
        self._default_mode = 'Push'

        self.push_dataset = {
            'name': name,
            'tables': self._tables,
            'datasources': self._data_sources,
            'defaultMode': self._default_mode,
            # 'relationships': self._relationships
        }

    def __repr__(self) -> str:
        """Represents the string representation of the
        table object.

        ### Returns
        ----
        str
            A JSON formatted string.
        """

        return json.dumps(obj=self.push_dataset, indent=4, cls=PowerBiEncoder)

    def __getitem__(self, index: int) -> object:
        return self.push_dataset[index]

    def __delitem__(self, index: int) -> None:
        del self.push_dataset[index]

    @property
    def name(self) -> str:
        """The dataset name.

        ### Returns
        ----
        str :
            The dataset name.
        """
        return self.push_dataset.get('name', None)

    @name.setter
    def name(self, name: str) -> None:
        """Sets the dataset name.

        ### Parameters
        ----
        name : str
            The name you want the dataset to be.
        """

        self.push_dataset.update({'name': name})

    @property
    def default_mode(self) -> str:
        """Gets the `defaultMode` property.

        ### Returns
        ----
        str :
            The dataset mode or type.
        """
        return self.push_dataset.get('defaultMode', None)

    @default_mode.setter
    def default_mode(self, default_mode: str) -> None:
        """Sets the `defaultMode` property.

        ### Parameters
        ----
        default_mode : str
            The dataset mode or type.
        """

        self.push_dataset.update({'defaultMode': default_mode})

    @property
    def tables(self) -> Tables:
        """Returns the `Tables` collection from
        the dataset.

        ### Returns
        ----
        Tables
            The dataset's `Tables` collection.
        """
        return self._tables

    def add_table(self, table: Table) -> None:
        """Adds a new `Table` object to the `Tables`
        collection.

        ### Parameters
        ----
        table : Table
            A table object with the properties set.
        """

        self._tables[len(self._tables)] = table

    def del_table(self, index: int) -> None:
        """Deletes a `Table` to the `Tables`
        collection.

        ### Parameters
        ----
        index : int
            The index of the table you want
            to delete from the collection.
        """

        del self._tables[index]

    def get_table(self, index: int) -> Table:
        """Gets a `Table` to the `Tables`
        collection.

        ### Parameters
        ----
        index : int
            The index of the table you want
            to get from the collection.
        """

        return self._tables[index]

    '''@property
    def relationships(self) -> Relationships:
        """Returns the `Relationships` collection from
        the dataset.

        ### Returns
        ----
        Relationships
            The dataset's `Relationships` collection.
        """

        return self._relationships

    def add_relationship(self, relationship: Relationship) -> None:
        """Adds a `Relationship` to the `Relationships`
        collection.

        ### Parameters
        ----
        relationship : Relationship
            The relationship object you want to add
            to the collection.
        """

        self._relationships[len(self._relationships)] = relationship

    def del_relationship(self, index: int) -> None:
        """Deletes a `Relationship` to the `Relationships`
        collection.

        ### Parameters
        ----
        index : int
            The index of the relationship you want
            to delete from the collection.
        """

        del self._relationships[index]

    def get_relationship(self, index: int) -> Relationship:
        """Gets a `Relationship` to the `Relationships`
        collection.

        ### Parameters
        ----
        index : int
            The index of the relationship you want
            to get from the collection.
        """

        return self._relationships[index]'''

    @property
    def data_sources(self) -> DataSources:
        """Returns the `DataSources` collection from
        the dataset.

        ### Returns
        ----
        Datasources
            The dataset's `DataSources` collection.
        """

        return self._data_sources

    def add_data_source(self, data_source: object) -> None:
        """Adds a `DataSource` to the `DataSources`
        collection.

        ### Parameters
        ----
        data_source : DataSource
            The data source object you want to add
            to the collection.
        """

        self._data_sources[len(self._data_sources)] = data_source

    def del_data_source(self, index: int) -> None:
        """Deletes a `DataSource` to the `DataSources`
        collection.

        ### Parameters
        ----
        index : int
            The index of the data source you want
            to delete from the collection.
        """

        del self._data_sources[index]

    def get_data_source(self, index: int) -> object:
        """Adds a `DataSource` to the `DataSources`
        collection.

        ### Parameters
        ----
        index : int
            The index of the data source you want
            to add to the collection.
        """

        return self._data_sources[index]

    def _prep_for_post(self) -> dict:
        """Preps the `Dataset` object so it's
        valid JSON for the PostDataset endpoint.

        ### Returns
        ----
        dict
            A dataset with valid keys.
        """

        copy_push_dataset = self.push_dataset.copy()
        # del copy_push_dataset['datasources']

        # for table in copy_push_dataset['tables']:
        #     del table['rows']

        return copy_push_dataset

    def to_dict(self) -> dict:
        return json.loads(
            s=json.dumps(obj=self.push_dataset, cls=PowerBiEncoder)
        )

    def to_json(self) -> dict:
        return json.dumps(obj=self.push_dataset, cls=PowerBiEncoder)
