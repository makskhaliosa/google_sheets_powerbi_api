from .table_items import Column, Measure


class Columns():

    """
    ### Overview
    ----
    Represents a collection of `Column` objects
    that are found inside of a `PowerBiTable` object.
    """

    def __init__(self) -> None:
        self.columns = []

    def __setitem__(self, index: int, data: Column) -> None:
        self.columns.append(data)

    def __getitem__(self, index: int) -> Column:
        return self.columns[index]

    def __delitem__(self, index: int) -> None:
        del self.columns[index]

    def __len__(self) -> int:
        return len(self.columns)

    def __iter__(self):
        return iter(self.columns)


class Measures():

    """
    ### Overview
    ----
    Represents a collection of `Measure` objects
    that are found inside of a `PowerBiTable` object.
    """

    def __init__(self) -> None:
        self.measures = []

    def __setitem__(self, index: int, data: Measure) -> None:
        self.measures[index] = data

    def __getitem__(self, index: int) -> Measure:
        return self.measures[index]

    def __delitem__(self, index: int) -> None:
        del self.measures[index]

    def __len__(self) -> int:
        return len(self.measures)

    def __iter__(self):
        return iter(self.measures)


class Tables():

    """
    ### Overview
    ----
    Represents a collection of `Table` objects
    that are found inside of a `PowerBiDataset`
    object.
    """

    def __init__(self) -> None:
        self.tables = []

    def __setitem__(self, index: int, data: dict) -> None:
        self.tables.append(data)

    def __getitem__(self, index: int) -> dict:
        return self.tables[index]

    def __delitem__(self, index: int) -> None:
        del self.tables[index]

    def __len__(self) -> int:
        return len(self.tables)

    def __iter__(self):
        return iter(self.tables)


class DataSources():

    """
    ### Overview
    ----
    Represents a collection of `Datasource` objects
    that are found inside of a `PowerBiDataset`
    object.
    """

    def __init__(self) -> None:
        self.datasources = []

    def __setitem__(self, index: int, data: object) -> None:
        self.datasources.append(data)

    def __getitem__(self, index: int) -> object:
        return self.datasources[index]

    def __delitem__(self, index: int) -> None:
        del self.datasources[index]

    def __len__(self) -> int:
        return len(self.datasources)

    def __iter__(self):
        return iter(self.datasources)
