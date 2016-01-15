# coding: utf-8
# SQL madness copied from lykos ahead

import sqlite3
from collections import defaultdict
from functools import reduce

class SQLConnection(object):
	conn = None
	c = None

	def __init__(self, db_file = 'data.sqlite3'):
		self.conn = sqlite3.connect(db_file, check_same_thread = False)
		self.conn.row_factory = sqlite3.Row
		self.c = self.conn.cursor()

	def fetchone(self, *args):
		with self.conn:
			self.c.execute(*args)
			return self.c.fetchone()

	def get_player(self, name):
		return self.fetchone("SELECT player FROM rolestats WHERE player=? COLLATE NOCASE", (name,))

	def get_players(self):
		with self.conn:
			self.c.execute("SELECT player AS name, SUM(totalgames) as total_games FROM rolestats GROUP BY player ORDER BY total_games DESC")
			return self.c.fetchall()

	def get_player_totalgames(self, name):
		with self.conn:
			self.c.execute("SELECT SUM(totalgames) as total_games FROM rolestats WHERE player=? COLLATE NOCASE GROUP BY player", (name,))
			row = self.c.fetchone()

			if row:
				return row['total_games']

			return None

	def get_player_rolestats(self, name):
		ret = dict()

		with self.conn:
			self.c.execute("SELECT role, teamwins, individualwins, totalgames FROM rolestats WHERE player=? COLLATE NOCASE ORDER BY totalgames DESC", (name,))
			return self.c.fetchall()

	def get_players_average_totalgames(self):
		with self.conn:
			self.c.execute("SELECT SUM(totalgames) as total_games FROM rolestats GROUP BY player")
			data = self.c.fetchall()
			all_games = 0

			for row in data:
				all_games += row['total_games']

			return all_games / len(data)

	def player_is_simple(self, name):
		with self.conn:
			self.c.execute("SELECT acc FROM simple_role_accs WHERE acc=? COLLATE NOCASE", (name,))

			if self.c.fetchone():
				return True

			return False

	def get_player_pingif(self, name):
		with self.conn:
			self.c.execute("SELECT players FROM ping_if_prefs_accs WHERE acc=? COLLATE NOCASE", (name,))
			row = self.c.fetchone()

			if row:
				return row['players']

			return None

	def get_gamemode(self, name):
		return self.fetchone("SELECT gamemode FROM gamestats WHERE gamemode=? COLLATE NOCASE", (name,))

	def get_gamemodes(self):
		with self.conn:
			self.c.execute("SELECT gamemode AS name, SUM(totalgames) as total_games FROM gamestats GROUP BY gamemode ORDER BY total_games DESC")
			return self.c.fetchall()

	def get_gamemode_totalgames(self, name):
		with self.conn:
			self.c.execute("SELECT SUM(totalgames) as total_games FROM gamestats WHERE gamemode=? COLLATE NOCASE GROUP BY gamemode", (name,))
			row = self.c.fetchone()

			if row:
				return row['total_games']

			return None

	def get_gamemode_stats(self, name):
		ret = dict()

		with self.conn:
			self.c.execute("SELECT * FROM gamestats WHERE gamemode=? COLLATE NOCASE ORDER BY size ASC", (name,))
			return self.c.fetchall()

	def get_roles(self):
		with self.conn:
			self.c.execute("SELECT role AS name, SUM(totalgames) as total_games FROM rolestats GROUP BY role ORDER BY total_games DESC")
			return self.c.fetchall()

	def get_role(self, name):
		return self.fetchone("SELECT role FROM rolestats WHERE role=? COLLATE NOCASE", (name,))

	def get_role_totalgames(self, name):
		with self.conn:
			self.c.execute("SELECT SUM(totalgames) as total_games FROM rolestats WHERE role=? COLLATE NOCASE GROUP BY role", (name,))
			row = self.c.fetchone()

			if row:
				return row['total_games']

			return None

	def get_role_teamwins(self, name):
		with self.conn:
			self.c.execute("SELECT SUM(teamwins) as teamwins FROM rolestats WHERE role=? COLLATE NOCASE GROUP BY role", (name,))
			row = self.c.fetchone()

			if row:
				return row['teamwins']

			return None

	def get_role_individualwins(self, name):
		with self.conn:
			self.c.execute("SELECT SUM(individualwins) as individualwins FROM rolestats WHERE role=? COLLATE NOCASE GROUP BY role", (name,))
			row = self.c.fetchone()

			if row:
				return row['individualwins']

			return None