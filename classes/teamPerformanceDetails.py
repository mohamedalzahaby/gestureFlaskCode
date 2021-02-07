class TeamPerformanceDetails:

    def __init__(self, id, moveId, totalCorrectMoves, totalwrongMoves, totalDuration, performancePercentage, teamPerformanceId, createdat):
        self.id = id
        self.moveId = moveId
        self.totalCorrectMoves = totalCorrectMoves
        self.totalwrongMoves = totalwrongMoves
        self.totalDuration = totalDuration
        self.performancePercentage = performancePercentage
        self.teamPerformanceId = teamPerformanceId
        self.createdat = createdat

    def __init__(self, id, move, totalCorrectMoves, totalwrongMoves, totalDuration, performancePercentage):
        self.id = id
        self.move = move
        self.totalCorrectMoves = totalCorrectMoves
        self.totalwrongMoves = totalwrongMoves
        self.totalDuration = totalDuration
        self.performancePercentage = performancePercentage