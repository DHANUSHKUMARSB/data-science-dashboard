from .query_base import QueryBase
import pandas as pd

class Employee(QueryBase):
    """
    Employee-level interface used by the dashboard.
    Exposes methods the dashboard expects:
      - name (class attribute)
      - names_and_ids()
      - event_counts(employee_id) -> pandas.DataFrame
      - model_data(employee_id) -> list-of-lists or 2D array compatible with model
      - notes(employee_id) -> rows
    """

    name = "employee"

    def names_and_ids(self):
        rows = self._all_employees()
        # rows: [(employee_id, first_name, last_name), ...]
        return [(r[0], f"{r[1]} {r[2]}") for r in rows]

    def event_counts(self, employee_id):
        """
        Return a pandas DataFrame with columns:
        ['date', 'positive', 'negative']
        """
        rows = self._employee_events(employee_id)
        df = pd.DataFrame(rows, columns=['date', 'positive', 'negative'])
        # ensure date is parsed if present (string)
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
        return df

    def model_data(self, employee_id):
        """
        Return features for the ML model.
        Here we return total positive and negative event counts.
        """
        df = self.event_counts(employee_id)
        if df.empty:
            return [[0, 0]]
        pos = int(df['positive'].sum())
        neg = int(df['negative'].sum())
        return [[pos, neg]]

    def notes(self, employee_id):
        """
        Return notes rows for the given employee.
        """
        return self._employee_notes(employee_id)
