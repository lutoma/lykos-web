# coding: utf-8

# Author: Lukas Martini <lutoma@ohai.su>
#
# Licensed under the European Union Public Licence (EUPL), Version 1.1 or - as
# soon they will be approved by the European Commission - subsequent versions
# of the EUPL (the "Licence"); You may not use this work except in compliance
# with the Licence.
#
# You may obtain a copy of the Licence at:
# http://ec.europa.eu/idabc/eupl.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the Licence is distributed on an "AS IS" basis, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# Licence for the specific language governing permissions and limitations
# under the Licence.

from flask import Flask, render_template, abort, redirect
from sql import SQLConnection
import settings

app = Flask(__name__)
app.debug = True
sql_connection = SQLConnection()

@app.route("/")
def index():
	return redirect("/players/", code=302)

@app.route("/players/")
def players():
	players = sql_connection.get_players()
	return render_template('players.html', players = players)

@app.route("/players/<name>/")
def player(name):
	player = sql_connection.get_player(name)

	if not player:
		abort(404)

	total_games = sql_connection.get_player_totalgames(name)
	stats = sql_connection.get_player_rolestats(name)
	average_games = sql_connection.get_players_average_totalgames()
	is_simple = sql_connection.player_is_simple(name)
	pingif = sql_connection.get_player_pingif(name)
	best_role = {'name': None, 'percentage': 0}
	worst_role = {'name': None, 'percentage': 100}

	for role in stats:
		percentage = max(
			role['individualwins'] / role['totalgames'] * 100,
			role['teamwins'] / role['totalgames'] * 100
		)

		if percentage > best_role['percentage']:
			best_role['percentage'] = percentage
			best_role['name'] = role['role']

		if percentage < worst_role['percentage']:
			worst_role['percentage'] = percentage
			worst_role['name'] = role['role']

	return render_template('player.html',
		name = name,
		total_games = total_games,
		stats = stats,
		admins = settings.ADMINS,
		average_games = average_games,
		is_simple = is_simple,
		pingif = pingif,
		best_role = best_role,
		worst_role = worst_role,
	)

@app.route("/gamemodes/")
def gamemodes():
	gamemodes = sql_connection.get_gamemodes()
	return render_template('gamemodes.html', modes = gamemodes)

@app.route("/gamemodes/<name>/")
def gamemode(name):
	mode = sql_connection.get_gamemode(name)
	total_games = sql_connection.get_gamemode_totalgames(name)
	stats = sql_connection.get_gamemode_stats(name)

	if not mode:
		abort(404)

	return render_template('gamemode.html',
		name = name,
		total_games = total_games,
		stats = stats,
	)

@app.route("/roles/")
def roles():
	roles = sql_connection.get_roles()
	return render_template('roles.html', roles = roles)

@app.route("/roles/<name>/")
def role(name):
	role = sql_connection.get_role(name)
	total_games = sql_connection.get_role_totalgames(name)
	team_wins = sql_connection.get_role_teamwins(name)
	individual_wins = sql_connection.get_role_individualwins(name)

	if not role:
		abort(404)

	return render_template('role.html',
		name = name,
		total_games = total_games,
		team_wins = team_wins,
		individual_wins = individual_wins,
	)


if __name__ == "__main__":
	app.run()