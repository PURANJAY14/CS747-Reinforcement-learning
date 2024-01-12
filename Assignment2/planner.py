import argparse
import numpy as np
import pulp 
#https://thispointer.com/python-dictionary-with-multiple-values-per-key/


def output(V,pi):
 	for i in range(len(V)):
 		print(V[i],"\t",int(pi[i]))

def value_iteration(reward,prob,nxt_state,num_states,num_actions,gamma,tol):

    V=np.zeros(num_states )
    #print(num_states)
    V_new=np.zeros(num_states )
    pi=np.zeros(num_states )
    error=tol+1

    while error>tol:
        for s in range( num_states ):
            Q=np.zeros(num_actions )
            for a in range( num_actions ):
                for j in range(len(prob[s][a])):
                    Q[a]+=prob[s][a][j]*(reward[s][a][j]+gamma*V[nxt_state[s][a][j]])

            #print(Q,V,"Here")	
            V_new[s] = max(Q)
            pi[s]=np.argmax(Q)

        #print(V_new,V)
        error = np.linalg.norm(V_new-V,np.inf)
        
        for s in range( num_states ):
            V[s] = V_new[s]

    output(V,pi)
	
def policy_evaluation(reward,prob,nxt_state,num_states,num_actions,gamma,tol,V,pi):
	
    error=tol+1
    
    while error>tol:
        V_new=np.zeros(num_states)
        for s in range( num_states ):
            a=pi[s]
            #print(a)
            for j in range(len(prob[s][a])):
                V_new[s]+=prob[s][a][j]*(reward[s][a][j]+gamma*V[nxt_state[s][a][j]])

        error = np.linalg.norm(V_new-V,np.inf)
        #print(V_new,V)
        for s in range( num_states ):
            V[s] = V_new[s]		

    return V

def policy_improvement(reward,prob,nxt_state,num_states,num_actions,gamma,tol,V,pi):

	
	unstable=False
	for s in range( num_states):
		action_old=pi[s]
		Q=np.zeros(num_actions)
		for a in range( num_actions ):
				for j in range(len(prob[s][a])):
					Q[a]+=prob[s][a][j]*(reward[s][a][j]+gamma*V[nxt_state[s][a][j]])
		pi[s]=np.argmax(Q)
		if(pi[s]!=action_old):
			unstable=True;

	#print(unstable)
	return unstable


def howards_policy_iteration(reward,prob,nxt_state,num_states,num_actions,gamma,tol):
    V=np.zeros(num_states )
    pi=np.int32(np.zeros(num_states))

    unstable=True
    while unstable:
        V=policy_evaluation(reward,prob,nxt_state,num_states,num_actions,gamma,tol,V,pi)
        unstable=policy_improvement(reward,prob,nxt_state,num_states,num_actions,gamma,tol,V,pi)
	
    output(V,pi)	


#https://benalexkeen.com/linear-programming-with-python-and-pulp-part-4/
def linear_programming(reward,prob,nxt_state,num_states,num_actions,gamma):
    v=pulp.LpVariable.dicts("s", (range(num_states))) 
    problem=pulp.LpProblem("Problem",pulp.LpMinimize) 
    problem+=sum([v[i] for i in range( num_states )]) 
    for s in range( num_states ):
        for a in range( num_actions ):
                problem+=v[s]-gamma*pulp.lpSum([prob[s][a][j]*v[nxt_state[s][a][j]] for j in range(len(prob[s][a]))])>=sum([prob[s][a][j]*reward[s][a][j] for j in range(len(prob[s][a]))])
    #print(problem,"Hi")
    problem.solve(pulp.apis.PULP_CBC_CMD(msg=0))
    V = np.zeros(num_states) 
    for i in range(num_states):
        V[i] = v[i].varValue

	    
    pi_star = np.zeros((num_states), dtype=np.int32)
    vdual = np.zeros((num_states, num_actions))
    s = 0
    a = 0
    for name, c in list(problem.constraints.items()):
        vdual[s,a] = c.pi
        if a < num_actions-1 :
            a = a + 1
        else:
            a = 0
            if s < num_states-1:
                s = s + 1
            else:
                s = 0
    for s in range( num_states ):
        pi_star[s] = np.argmax(vdual[s, :])


    output(V,pi_star)
			

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--mdp',type=str,required=False,help='check')
    parser.add_argument('--algorithm', type=str, required=False)
    parser.add_argument('--policy', type=str, required=False)
    args = parser.parse_args()
    
    #print(args.mdp)
    with open(args.mdp, 'r') as f:
    	lines = f.readlines()


    temp = lines[0].strip().split()
    num_states=int(temp[1])

    temp=lines[1].strip().split()
    num_actions=int(temp[1])

    temp=lines[2].strip().split()
    end_states=[int(x) for x in temp[1:]]

    i=3
    prob={};reward={};nxt_state={};
    prob=[[[] for y in range(num_actions )] for x in range(num_states )]
    reward=[[[] for y in range(num_actions )] for x in range(num_states )]
    nxt_state=[[[] for y in range(num_actions )] for x in range(num_states )]
    while True:
    	#print(temp)
    	temp=lines[i].strip().split()
    	if temp[0]!="transition":
    		break;

    	s1=int(temp[1])
    	ac=int(temp[2])
    	s2=int(temp[3])
    	r=float(temp[4])
    	p=float(temp[5])

    	prob[s1][ac].append(p)
    	reward[s1][ac].append(r)
    	nxt_state[s1][ac].append(s2)
    	#print(reward,"\n\n")
    	i=i+1

    temp=lines[i].strip().split()
    mdptype=temp[1]

    temp=lines[i+1].strip().split()
    gamma=float(temp[1])

    tol=1e-12

    if args.policy is not None:
        pi=[];V=np.zeros(num_states )
        with open(args.policy,'r') as f:
            for line in f:
                #print(line)
                temp=line.strip().split()
                pi.append(int(temp[0]))

        pi=np.array(pi)
        #print(pi,num_states,num_actions)
        V=policy_evaluation(reward,prob,nxt_state,num_states,num_actions,gamma,tol,V,pi)
        output(V,pi)

        #TODO
        
        f.close()

    elif args.algorithm is None:
        value_iteration(reward,prob,nxt_state,num_states,num_actions,gamma,tol)
        #howards_policy_iteration(reward,prob,nxt_state,num_states,num_actions,gamma,tol)
        #linear_programming(reward,prob,nxt_state,num_states,num_actions,gamma)

    elif args.algorithm == "vi":
        value_iteration(reward,prob,nxt_state,num_states,num_actions,gamma,tol)

    elif args.algorithm == "hpi":
        howards_policy_iteration(reward,prob,nxt_state,num_states,num_actions,gamma,tol)

    elif args.algorithm == "lp":
        linear_programming(reward,prob,nxt_state,num_states,num_actions,gamma)
	

    
#python planner.py --mdp /host/Assignment2/code/data/mdp/continuing-mdp-10-5.txt --policy /host/Assignment2/code/data/mdp/rand-continuing-mdp-10-5.txt