from .query_base import QueryBase
import pandas as pd

class Team(QueryBase):
    """
    Team-level interface used by the dashboard.
    Exposes methods:
      - name (class attribute)
      - names_and_ids()
      - event_counts(team_id) -> pandas.DataFrame
      - model_data(team_id) -> list-of-lists for ML model
      - notes(team_id) -> rows
    """

    name = "team"

    def names_and_ids(self):
        rows = self._all_teams()
        # rows: [(team_id, team_name), ...]
        return [(r[0], r[1]) for r in rows]

    def event_counts(self, team_id):
        """
        Return a pandas DataFrame with columns:
        ['date', 'positive', 'negative']
        """
        rows = self._team_events(team_id)
        df = pd.DataFrame(rows, columns=['date', 'positive', 'negative'])
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
        return df

    def model_data(self, team_id):
        """
        Return features for the ML model.
        For a team we return one record per team with
        aggregated positive and negative counts.
        """
        df = self.event_counts(team_id)
        if df.empty:
            return [[0, 0]]
        pos = int(df['positive'].sum())
        neg = int(df['negative'].sum())
        return [[pos, neg]]

    def notes(self, team_id):
        """
        Return notes rows for the given team.
        """
        return self._team_notes(team_id)
