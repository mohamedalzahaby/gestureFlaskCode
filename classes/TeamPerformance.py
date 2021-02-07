class TeamPerformance:

    def __init__(self, TeamPerformanceDetailsList, id, team, createdat, updatedat, isdeleted, totalCorrectMoves, totalWrongMoves, totalDuration, year, month, performancePercentage):
        self.TeamPerformanceDetailsList = TeamPerformanceDetailsList
        self.id = id
        self.team = team
        self.createdat = createdat
        self.updatedat = updatedat
        self.isdeleted = isdeleted
        self.totalCorrectMoves = totalCorrectMoves
        self.totalWrongMoves = totalWrongMoves
        self.totalDuration = totalDuration
        self.year = year
        self.month = month
        self.performancePercentage = performancePercentage

    def __init__(self, TeamPerformanceDetailsList, id, totalCorrectMoves, totalWrongMoves, totalDuration, year, month, performancePercentage):
        self.TeamPerformanceDetailsList = TeamPerformanceDetailsList
        self.id = id
        self.totalCorrectMoves = totalCorrectMoves
        self.totalWrongMoves = totalWrongMoves
        self.totalDuration = totalDuration
        self.year = year
        self.month = month
        self.performancePercentage = performancePercentage