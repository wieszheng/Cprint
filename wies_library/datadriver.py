# -*- coding: utf-8 -*-

"""
@file    : datadriver.py
@author  : v_wieszheng
@Data    : 2023-03-15 下午 05:45
@software: PyCharm
"""
import pandas
from collections import OrderedDict
import inspect
import functools


class DataDriver(object):
    @staticmethod
    def run_data_from_excel(path, sheet_name = 0, field_on_column = False):
        """
        说明：
            测试数据驱动测试案例
        示例：
            例如Excel中sheet页存在如下4行3列的数据，第1行通常为字段名，数据为3行3列（默认）。
                字段1	    字段2	    字段3
                字段1_数值1	字段2_数值1	字段3_数值1
                字段1_数值2	字段2_数值2	字段3_数值2
                字段1_数值3	字段2_数值3	字段3_数值3
            或  sheet页中第一列为字段名 其他列为数据 （指定参数field_on_column=True）
                字段1 字段1_数值1 字段1_数值2 字段1_数值3
                字段2 字段2_数值1 字段2_数值2 字段2_数值3
                字段3 字段3_数值1 字段3_数值2 字段3_数值3

            我们在编写某个自动化案例场景时，如果测试步骤相同只是测试数据不同的话，可以像这样编写：
            class Test(unittest.TestCase):
                ...
                @run_data_from_excel(path=r".\Data\data.xlsx")
                def test_func(self, 字段1, 字段2, 字段3):
                    ...
                    # 测试执行
                    ...
                ...
            在编写定义test_func时，参数名要与Excel中的字段名一致

        :param path: Excel路径
        :param sheet_name: sheet页编号或名称
        :param field_on_column: False-第一行为字段名(默认) True-第一列为字段名
        """
        def decorator(func):
            return DataDriver._return_wrapper(func=func, file_type='excel', path=path, sheet_name=sheet_name,
                                              field_on_column=field_on_column)
        return decorator

    @staticmethod
    def run_date_from_csv(path, sep = ",", field_on_column = False):
        """
        说明：
            测试数据驱动测试案例
        示例：
            例如Csv中存在如下4行3列的数据，第1行通常为字段名，数据为3行3列（默认）。
                字段1	  ,字段2	     ,字段3
                字段1_数值1,字段2_数值1,字段3_数值1
                字段1_数值2,字段2_数值2,字段3_数值2
                字段1_数值3,字段2_数值3,字段3_数值3
            或  Csv中第一列为字段名，其他列为数值（指定参数field_on_column=True）
                字段1,字段1_数值1,字段1_数值2,字段1_数值3
                字段2,字段2_数值1,字段2_数值2,字段2_数值3
                字段3,字段3_数值1,字段3_数值2,字段3_数值3

            我们在编写某个自动化案例场景时，如果测试步骤相同只是测试数据不同的话，可以像这样编写：
            class Test(unittest.TestCase):
                ...
                @run_date_from_csv(path=r".\Data\data.csv")
                def test_func(self, 字段1, 字段2, 字段3):
                    ...
                    # 测试执行
                    ...
                ...
            在编写定义test_func时，参数个数与Csv中的列名个数要一致

        :param path: Csv路径
        :param sep: Csv数据分隔符，默认为“,”
        :param field_on_column: False-第一行为字段名(默认) True-第一列为字段名
        """
        def decorator(func):
            return DataDriver._return_wrapper(func=func, file_type='csv', path=path, sep=sep,
                                              field_on_column=field_on_column)
        return decorator

    @staticmethod
    def _return_wrapper(func, **kwargs):
        """
        说明：
            返回被装饰的函数wrapper
        :param func: 被装饰函数func
        :return:
        """

        co_var_names = tuple(inspect.signature(func).parameters)  # 获取func函数的形参
        if 'self' in co_var_names:
            _co_var_names = list(co_var_names)
            _co_var_names.remove('self')
            co_var_names = tuple(_co_var_names)
        file_type = kwargs.get('file_type', '')

        @functools.wraps(func)
        def wrapper(*args):
            nkwargs = []
            if file_type == 'excel':
                nkwargs = DataDriver._get_kwargs_from_execl(
                    field_on_column=kwargs.get('field_on_column'),
                    path=kwargs.get('path'),
                    sheet_name=kwargs.get('sheet_name'),
                )
            elif file_type == 'csv':
                nkwargs = DataDriver._get_kwargs_from_csv(
                    field_on_column=kwargs.get('field_on_column'),
                    path=kwargs.get('path'),
                    sep=kwargs.get('sep'),
                )
            nkwargs = ({key: kw[key] for key in co_var_names} for kw in nkwargs)
            for nkw in nkwargs:
                func(*args, **nkw)
        return wrapper

    @staticmethod
    def _get_kwargs_from_execl(**kwargs):
        field_on_column = kwargs.get('field_on_column', False)
        path = kwargs.get('path', '')
        sheet_name = kwargs.get('sheet_name', 0)

        if not field_on_column:
            excel_data = pandas.read_excel(io=path, sheet_name=sheet_name, header=0)
            # OrderedDict可以将一个Series转换为key-value，其中key为Series的index
            nkwargs = (OrderedDict(excel_data.iloc[row]) for row in range(excel_data.shape[0]))
        else:
            excel_data = pandas.read_excel(io=path, sheet_name=sheet_name, header=None, index_col=0)
            nkwargs = (OrderedDict(excel_data[column + 1]) for column in range(excel_data.shape[1]))

        return nkwargs

    @staticmethod
    def _get_kwargs_from_csv(**kwargs):
        field_on_column = kwargs.get('field_on_column', False)
        path = kwargs.get('path', '')
        sep = kwargs.get('sep', ',')

        if not field_on_column:
            csv_data = pandas.read_csv(filepath_or_buffer=path, sep=sep, header=0)
            nkwargs = (OrderedDict(csv_data.iloc[row]) for row in range(csv_data.shape[0]))
        else:
            csv_data = pandas.read_csv(filepath_or_buffer=path, sep=sep, header=None, index_col=0)
            nkwargs = (OrderedDict(csv_data[column + 1]) for column in range(csv_data.shape[1]))

        return nkwargs

