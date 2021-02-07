from DBConnection.DatabaseConnection import getResults
from classes.Move import Move
from classes.Coach import Coach
from classes.Player import Player
from classes.Session import Session
from classes.SessionDetails import SessionDetails
from classes.Team import Team
from classes.TeamPerformance import TeamPerformance
from classes.teamPerformanceDetails import TeamPerformanceDetails


def get_Performance_Details_List_By_PerformanceId(performanceId):
    teamPerformanceDetailsList = []
    query = "SELECT t.`moveId`, a.name , " \
            "t.`id` , t.`totalCorrectMoves`, t.`totalwrongMoves`, " \
            "t.`totalDuration`, t.`performancePercentage` " \
            "FROM `teamperformancedetails` AS t " \
            "JOIN `activity` AS a " \
            "ON (a.id = t.moveId) " \
            "WHERE t.isdeleted = 0 " \
            "AND a.isdeleted = 0 " \
            f"AND t.`teamPerformanceId` = {performanceId}"
    for row in getResults(query):
        move = Move(row[0], row[1])
        teamPerformanceDetails = TeamPerformanceDetails(row[2], move.__dict__, row[3], row[4], row[5], row[6])
        teamPerformanceDetailsList.append(teamPerformanceDetails.__dict__)

    return teamPerformanceDetailsList


def getPerformanceList(teamId):
    performanceList = []
    query = "SELECT `id`, `totalCorrectMoves`, `totalWrongMoves`, `totalDuration`, `year`, `month`, `performancePercentage` " \
            "FROM `teamperformance` " \
            f"WHERE `teamId`= {teamId} AND `isdeleted` = 0"

    for row in getResults(query):
        performanceDetailsList = get_Performance_Details_List_By_PerformanceId(row[0])
        performance = TeamPerformance(performanceDetailsList, row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        performanceList.append(performance.__dict__)
    return performanceList


def getTeamsByCoachId(coachId):
    teams = []
    query = "SELECT t.id , t.name " \
            "FROM `team` AS t " \
            "JOIN `teammembers` AS tm " \
            "ON (t.id = tm.teamId) " \
            f"WHERE `coachId` = {coachId} " \
            "AND t.isdeleted = 0 " \
            "AND tm.isdeleted = 0 "
    print(query)
    for row in getResults(query):
        team = Team(row[0],row[1])
        teams.append(team)
    return teams


def getCoachTeamsList(coachId):
    teamsList = []
    teams = getTeamsByCoachId(coachId)
    for team in teams:
        performances = getPerformanceList(team.id)
        team.setTeamPerformance(performances)
    for team in teams:
        teamsList.append(team.__dict__)
    return teamsList





def get_sessionDetailsListbySessionId(sessionId):
    sessionDetailsList = []
    query = "SELECT sessiondetails.id, start, end , activityId ,name " \
            "FROM sessiondetails " \
            "JOIN activity " \
            "ON activityId = activity.id " \
            f"WHERE sessionId = {sessionId} " \
            "AND activity.isdeleted = 0 AND sessiondetails.isdeleted = 0"
    for row in getResults(query):
        move = Move(row[3],row[4])
        sessionDetails = SessionDetails(row[0], row[1], row[2], move.__dict__)
        sessionDetailsList.append(sessionDetails.__dict__)
    return sessionDetailsList


def getSessionsList(playerId):
    SessionsList = []
    query = f"SELECT id, duration FROM `session` WHERE playerId = {playerId} AND isdeleted = 0"
    for row in getResults(query):
        sessionId = row[0]
        sessiondetailsList = get_sessionDetailsListbySessionId(sessionId)
        session = Session(sessionId, sessiondetailsList)
        SessionsList.append(session.__dict__)
    return SessionsList


def getUserSessionsData(playerId):
    player = Player()
    player.setId(playerId)
    player.setSessionList(getSessionsList(playerId))
    return player.__dict__


def getCoachPayersList(coachId):
    players = []
    teams = []
    query = "SELECT `playerId` ,`teamId` ,user.`name`, team.`name` " \
            "FROM `teammembers` " \
            "JOIN `user` " \
            "JOIN `team` " \
            "ON user.id = playerId " \
            "AND team.id = teamId " \
            f"WHERE coachId = {coachId} " \
            "AND user.isdeleted = 0 AND team.isdeleted = 0 AND teammembers.isdeleted = 0"

    for row in getResults(query):
        team = Team(row[1], row[3])
        player = Player()
        player.setData(row[0], row[2], team.__dict__)
        players.append(player.__dict__)
    coach = Coach()
    coach.setPlayers(players)
    return coach



