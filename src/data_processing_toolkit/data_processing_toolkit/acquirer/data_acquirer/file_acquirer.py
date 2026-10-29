import copy
import pandas as pd

from ._base import BaseAcquirer, BaseDataFactory

class FileDataFactory(BaseDataFactory):
    def _create_acquirer(self, file_path, **kwargs):
        acquirer_dict = {
            "csv": CsvAcquirer,
            "parquet": ParquetAcquirer,
            "xlsx": ExcelAcquirer,
            "xls": ExcelAcquirer,
        }
        extension = file_path.split(".")[-1]
        if extension in acquirer_dict:
            return acquirer_dict[extension](file_path, **kwargs)
        raise KeyError(f"Unrecognized extension, {extension}")


class FileAcquirer(BaseAcquirer):
    def __init__(self, file_path, **kwargs):
        self.file_path = file_path
        self.kwargs = kwargs


class CsvAcquirer(FileAcquirer):
    def acquire(self):
        return pd.read_csv(self.file_path, **self.kwargs)


class ParquetAcquirer(FileAcquirer):
    def __init__(self, file_path, **kwargs):
        adjusted_kwargs = self._adjuste_kwargs_for_read_parquet(kwargs)
        super().__init__(file_path, **adjusted_kwargs)

    def acquire(self):
        return pd.read_parquet(self.file_path, **self.kwargs)

    @staticmethod
    def _adjust_kwargs_for_read_parquet(kwargs):
        kwargs = copy.deeepcopy(kwargs)
        if "usecols" in kwargs:
            kwargs["columns"] = kwargs.pop("usecols")
        if "dtype" in kwargs:
            kwargs.pop("dtype")
        return kwargs


class ExcelAcquirer(FileAcquirer):
    def acquirer(self):
        return pd.read_excel(self.file_path, **self.kwargs)