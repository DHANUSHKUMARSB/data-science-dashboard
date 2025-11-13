from .sql_execution import with_db_connection

class QueryBase:
    """
    Base query class with decorated methods that return SQL strings.
    The decorator will execute the SQL and return rows.
    """

    # Basic table access
    @with_db_connection
    def _all_employees(self):
        return "SELECT employee_id, first_name, last_name FROM employee;"

    @with_db_connection
    def _all_teams(self):
        return "SELECT team_id, team_name FROM team;"

    # Events
    @with_db_connection
    def _employee_events(self, employee_id):
        return f"""
        SELECT event_date, positive_events, negative_events
        FROM employee_events
        WHERE employee_id = {employee_id}
        ORDER BY event_date;
        """

    @with_db_connection
    def _team_events(self, team_id):
        return f"""
        SELECT event_date, positive_events, negative_events
        FROM employee_events
        WHERE team_id = {team_id}
        ORDER BY event_date;
        """

    # Notes
    @with_db_connection
    def _employee_notes(self, employee_id):
        return f"""
        SELECT note_date, note
        FROM notes
        WHERE employee_id = {employee_id}
        ORDER BY note_date;
        """

    @with_db_connection
    def _team_notes(self, team_id):
        return f"""
        SELECT note_date, note
        FROM notes
        WHERE team_id = {team_id}
        ORDER BY note_date;
        """
