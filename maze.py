import requests
import json

# Moves position in the specified direction
def move(turn, url2, header):
	return requests.post(url2, data = json.dumps(turn), headers = header).json()['result']

# Get token with UID
url = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session'
uid = {'uid':'604919786'}
headers = {'Accept':'application/x-www-form-url','Content-type':'application/json'}
r = requests.post(url, data=json.dumps(uid), headers=headers)
token = r.json()['token']

# URL to get state of maze and make moves
url2 = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=' + token
r = requests.get(url2)

total_levels = r.json()['total_levels']
levels_completed = r.json()['levels_completed']	
	
# Defining possible moves
up = {'action' : 'UP'}
down = {'action' : 'DOWN'}
left = {'action' : 'LEFT'}
right = {'action' : 'RIGHT'}

# Solve all levels
while (levels_completed < total_levels):
	r = requests.get(url2)
	print("Working on level ", levels_completed + 1)
	
	#obtaining size of matrix
	cols = r.json()['maze_size'][0]
	rows = r.json()['maze_size'][1]

	#obtaining current position
	xCoord = r.json()['current_location'][0]
	yCoord = r.json()['current_location'][1]

	# Initializing visited matrix to mark as visited
	visited = [[False for j in range(cols)] for i in range(rows)]
		
	# Solves the maze and returns whether or not a path to the end has been found
	def solve(x, y):
		visited[y][x] = True

		# If moving out of bounds, to a visited point, or into a wall, do not recurse down that path
		# Stop and continue to next level when a level is solved

		# UP
		if ((y - 1 >= 0) and not (visited[y - 1][x])):
			moving = move(up, url2, headers)
			if (moving == 'END'):
				return True
			elif (moving == 'SUCCESS'):
				# Recursing
				solved = solve(x, y - 1)
				if (solved):
					return True
				# Backtracking
				move(down, url2, headers)
			elif (moving == 'WALL'):
				visited[y - 1][x] = True

		# DOWN
		if ((y + 1 < rows) and not (visited[y + 1][x])):
			moving = move(down, url2, headers)
			if (moving == 'END'):
				return True
			elif (moving == 'SUCCESS'):
				# Recursing
				solved = solve(x, y + 1)
				if (solved):
					return True
				# Backtracking
				move(up, url2, headers)
			elif (moving == 'WALL'):
				visited[y + 1][x] = True

		# LEFT
		if ((x - 1 >= 0) and not (visited[y][x - 1])):
			moving = move(left, url2, headers)
			if (moving == 'END'):
				return True
			elif (moving == 'SUCCESS'):
				# Recursing
				solved = solve(x - 1, y)
				if (solved):
					return True
				# Backtracking
				move(right, url2, headers)
			elif (moving == 'WALL'):
				visited[y][x - 1] = True

		# RIGHT
		if ((x + 1 < cols) and not (visited[y][x + 1])):
			moving = move(right, url2, headers)
			if (moving == 'END'):
				return True
			elif (moving == 'SUCCESS'):
				# Recursing
				solved = solve(x + 1, y)
				if (solved):
					return True
				# Backtracking
				move(left, url2, headers)
			elif (moving == 'WALL'):
				visited[y][x + 1] = True

		return False

	# Recursively solve current maze
	solve(xCoord, yCoord)
	levels_completed += 1
	print("Completed level ", levels_completed)

print ("Completed all mazes!")
