from influxdb import DataFrameClient
from collections import Counter
import settings


qenv = settings.Qenvs()

influx_info = {'host': qenv.influxdb_host, 'port': qenv.influxdb_port,
               'user': qenv.influxdb_user, 'pass': qenv.influxdb_pass, 'db': qenv.influxdb_name}


class QuarksInventory():
    def __init__(self, infdb):
        self.srv = qenv.server
        self.filter_sql = f'AND member_activity !~ /{qenv.filters}/'
        self.infdb = infdb
        self.influxdb_client = DataFrameClient(
            infdb.get('host'), infdb.get('port'), infdb.get('user'), infdb.get('pass'), infdb.get('db'))

    def get_member_logs(self, member_name, time_integer=7, time_unit='d'):
        # Returns dataframe of all the member activities from past <time_integer><time_unit>
        # Implemented but not really needed
        query = f'SELECT * FROM \"{self.srv}\" WHERE (member_name = \'{member_name}\' AND time >= now() - {time_integer}{time_unit} {self.filter_sql})'
        df_member_logs = self.influxdb_client.query(query).get(self.srv)
        return df_member_logs

    def get_distinct_activies(self, member_name=None, time_integer=7, time_unit='d'):
        # returns dataframe of the activities detected
        if member_name is None:
            # Get all activities by all members
            distincts_query = f'SELECT distinct(member_activity) FROM \"{self.srv}\" WHERE(time >= now() - {time_integer}{time_unit} {self.filter_sql})'
        else:
            # Get activities of specific member
            distincts_query = f'SELECT distinct(member_activity) FROM \"{self.srv}\" WHERE(member_name= \'{member_name}\' AND time >= now() - {time_integer}{time_unit} {self.filter_sql})'
        df_activities = self.influxdb_client.query(
            distincts_query).get(self.srv)
        return df_activities

    def calc_activity_duration(self, activity, member_name=None, time_integer=7, time_unit='d'):
        # Returns minutes spent on activity
        if member_name is None:
            minutes_query = f"SELECT (sum(a)*5)/60 as minutes FROM(SELECT count(member_activity) as a FROM \"{self.srv}\" WHERE(member_activity=\'{activity}\' AND time >= now() - {time_integer}{time_unit}))"
        else:
            minutes_query = f"SELECT (sum(a)*5)/60 as minutes FROM(SELECT count(member_activity) as a FROM \"{self.srv}\" WHERE(member_name= \'{member_name}\'  AND member_activity=\'{activity}\' AND time >= now() - {time_integer}{time_unit}))"
        df_duration = self.influxdb_client.query(minutes_query).get(self.srv)
        minutes = df_duration.iloc[-1]['minutes'].round(
            2) if df_duration is not None else 0
        return minutes

    def calculate_all_activities(self, member_name=None):
        # Need to add member activity calculation
        df_dist_activities = self.get_distinct_activies()
        if df_dist_activities is not None:
            activity_keys = df_dist_activities['distinct'].tolist()
            total_activity_minutes = dict.fromkeys(activity_keys, 0)

            for activity in activity_keys:
                game_minutes = self.calc_activity_duration(
                    activity, member_name=member_name)
                iter_result = {activity: game_minutes}
                total_activity_minutes = dict(
                    Counter(iter_result)+Counter(total_activity_minutes))
            total_activity_minutes['Total playtime'] = sum(
                total_activity_minutes.values())

        return total_activity_minutes


# qm = QuarksInventory(infdb=influx_info)
# totals = qm.calculate_all_activities()
