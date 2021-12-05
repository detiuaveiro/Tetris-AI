import time
original_pieces={
	"S":[[4,2],[4,3],[5,3],[5,4]], 
	"Z":[[4,2],[3,3],[4,3],[3,4]], 
	"I":[[2,2],[3,2],[4,2],[5,2]], 
	"O":[[3,3],[4,3],[3,4],[4,4]], 
 	"J":[[4,2],[5,2],[4,3],[4,4]], 
 	"L":[[4,2],[4,3],[4,4],[5,4]], 
 	"T":[[4,2],[4,3],[5,3],[4,4]] 
}
rotacoes = {
    "S": [[[4,2],[4,3],[5,3],[5,4]], [[4,3],[5,3],[3,4],[4,4]]],
    "Z": [[[4,2],[3,3],[4,3],[3,4]], [[3,3],[4,3],[4,4],[5,4]]],
    "I": [[[2,2],[3,2],[4,2],[5,2]], [[4,1],[4,2],[4,3],[4,4]]],
    "O": [[[3,3],[4,3],[3,4],[4,4]]],
    "J": [[[4,2],[5,2],[4,3],[4,4]], [[3,3],[4,3],[5,3],[5,4]], [[4,2],[4,3],[3,4],[4,4]], [[3,2],[3,3],[4,3],[5,3]]],
	"L": [[[4,2],[4,3],[4,4],[5,4]], [[3,3],[4,3],[5,3],[3,4]], [[3,2],[4,2],[4,3],[4,4]], [[5,2],[3,3],[4,3],[5,3]]],
    "T": [[[4,2],[4,3],[5,3],[4,4]], [[3,3],[4,3],[5,3],[4,4]], [[4,2],[3,3],[4,3],[4,4]], [[4,2],[3,3],[4,3],[5,3]]]
}
num1=-0.510066 #original
#num1=-0.610066 
num2=0.760666 #original
#num2=1
num3=-0.35663 #original
num4=-0.184483 #original
def run_ai(game,piece,x,y):
	piece_name=""
	for p in original_pieces:
		if(original_pieces[p]==piece):
			piece_name=p	
	if piece_name!="":
		position,rotation =best(game,piece_name,x,y) 
		#TO DO:change rotations to not hardcoded
		ret=[] #return all actions
		for i in range(rotation):
			ret.append("w")
		while position<0: 
			ret.append("a") 
			position+=1
		while position>0:
			ret.append("d") 
			position-=1
		ret.append("s")
		return ret
	else:
		return [""]
	
def intersect(piece,i,j,game,width,height):
	res=False
	for x,y in piece:
		if(x+i<1 or x+i>=width-1 or y+j>=height or [x+i,y+j] in game):
			res=True
	return res

def simulate(piece,i,j,game,width,height): #i=col j=linha
		while not intersect(piece,i,j,game,width,height):
			j+=1
		j-=1
		filled=[(a,b) for a,b in game]
		for (x,y) in piece: #x=col y=linha
			filled.append((x+i,y+j))
			
		
		comp_lines = check_complete_lines(filled,height) #MAXIMIZE
		#start=time.time()
		# ag_height = aggregate_height(filled,height) #MINIMIZE
		# num_holes = count_holes(filled,width,height) #MINIMIZE
		# bumpiness = calc_bumpiness(filled,width,height) #MINIMIZE
		# print("old: ",time.time()-start)
		# print("old ag,holes,bump:",ag_height," ",num_holes," ",bumpiness)
		# start=time.time()
		ag_height,num_holes,bumpiness= height_holes(filled,width,height) #MINIMIZE BOTH
		# print("new: ",time.time()-start)
		#print("new ag,holes,bump:",ag_height," ",num_holes," ",bumpiness)
		#print(num1*ag_height + num2*comp_lines + num3*num_holes + num4*bumpiness)
		#print(piece,i,j,"old f:",ag_height,"new f:",sum,"\nold holes:",num_holes,"new holes:",holes)
		# num1=-0.510066 #original
		# #num1=-0.610066 
		# num2=0.760666 #original
		# #num2=1
		# num3=-0.35663 #original
		# num4=-0.184483 #original

		#Acording to paper
		return num1*ag_height + num2*comp_lines + num3*num_holes + num4*bumpiness
		
def best(game,piece_name,width,height):
	best_heuristic = -900
	num_rotacoes=0
	best_position = None
	best_rotation=0
	for r in rotacoes[piece_name]:
		for i in range(-width,width,1): #iterate over the field
			if not intersect(r,i,0,game,width,height): #r is the rotated piece
				heuristic = simulate(r,i,0,game,width,height) 
				if heuristic > best_heuristic:
					best_heuristic=heuristic
					best_position=i
					best_rotation=num_rotacoes			
		num_rotacoes+=1
	return best_position,best_rotation
counter=0

# def aggregate_height(filled,height):
# 	global counter
# 	piece_by_column = {}
# 	for c,l in filled:
# 		if c not in piece_by_column:
# 			piece_by_column[c]=[height-l]
# 		else:
# 			piece_by_column[c].append(height-l)
# 	sum = 0
# 	for elem in piece_by_column:
# 		sum+=max(piece_by_column[elem])
# 	return sum

def height_holes(filled,width,height):
	sum=0
	holes=0
	bumpiness=0
	piece_by_column = {}
	for y in range(1,width-1):
		piece_by_column[y]=0
		for x in range(1,height):
			if (y,x) in filled:
				sum+=(height-x)
				piece_by_column[y]=height-x
				for k in range(x,height):
					if (y,k) not in filled:
						holes+=1
				break
	#print(abs(piece_by_column[hei]-piece_by_column[hei+1]) for hei in range(1,len(piece_by_column)-1))
	for hei in range(1,len(piece_by_column)-1):
		bumpiness+=abs(piece_by_column[hei]-piece_by_column[hei+1])
	return sum,holes,bumpiness

def check_complete_lines(filled,height):
	pieces_by_line={}
	for c,l in filled:
		if height-l not in pieces_by_line:
			pieces_by_line[height-l]=1
		else:
			pieces_by_line[height-l]+=1
	return sum(value == 8 for value in pieces_by_line.values())

# def count_holes(filled,width,height):
# 	holes=0
# 	for y in range(1,width):
# 		for x in range(1,height):
# 			if (y,x) in filled:
# 				for k in range(x,height):
# 					if (y,k) not in filled:
# 						holes+=1
# 				break
# 	return holes

# def count_holes(filled,width,height,i,j):
# 	holes=0
# 	for y in range(1,width):
# 		for x in range(1,height):
# 			if (y,x) in filled:
# 				for k in range(x,height):
# 					if (y,k) not in filled:
# 						holes+=1
# 				break
# 	return holes

# def count_holes(filled,width,height,i,j):
# 	holes=0
# 	if (i,j) in filled:
# 		for k in range(j,height):
# 			if (i,k) not in filled:
# 				holes+=1
# 	return holes
	
# def calc_bumpiness(filled,width,height):
# 	piece_by_column = {}
# 	for wid in range(1,width-1):
# 			piece_by_column[wid]=0
# 	for c,l in filled:
# 		if height-l>piece_by_column[c]:
# 			piece_by_column[c]=height-l
# 	return sum(abs(piece_by_column[hei]-piece_by_column[hei+1]) for hei in range(1,len(piece_by_column)-1))

